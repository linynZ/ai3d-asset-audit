"""Minimal GLB reader: JSON chunk, binary chunk, accessors, node world matrices.

Only what the audit needs. No third-party glTF library, so the numbers come
straight from the bytes the engine importer also reads.
"""
import json
import struct
from pathlib import Path

import numpy as np

COMP = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16,
        5125: np.uint32, 5126: np.float32}
NCOMP = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


class GLB:
    def __init__(self, path):
        self.path = Path(path)
        data = self.path.read_bytes()
        magic, version, length = struct.unpack_from("<III", data, 0)
        assert magic == 0x46546C67, "not a GLB"
        off = 12
        self.json, self.bin = None, b""
        while off < length:
            clen, ctype = struct.unpack_from("<II", data, off)
            chunk = data[off + 8: off + 8 + clen]
            if ctype == 0x4E4F534A:
                self.json = json.loads(chunk)
            elif ctype == 0x004E4942:
                self.bin = chunk
            off += 8 + clen
        self.version = version
        self.total_bytes = length

    def accessor(self, idx):
        a = self.json["accessors"][idx]
        bv = self.json["bufferViews"][a["bufferView"]]
        dtype = COMP[a["componentType"]]
        n = NCOMP[a["type"]]
        start = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        stride = bv.get("byteStride")
        itemsize = np.dtype(dtype).itemsize * n
        if stride and stride != itemsize:
            raw = np.frombuffer(self.bin, np.uint8, count=stride * a["count"], offset=start)
            raw = raw.reshape(a["count"], stride)[:, :itemsize].copy()
            arr = raw.view(dtype).reshape(a["count"], n)
        else:
            arr = np.frombuffer(self.bin, dtype, count=a["count"] * n, offset=start).reshape(a["count"], n)
        return arr

    def accessor_bytes(self, idx):
        a = self.json["accessors"][idx]
        return a["count"] * NCOMP[a["type"]] * np.dtype(COMP[a["componentType"]]).itemsize

    @staticmethod
    def local_matrix(node):
        if "matrix" in node:
            return np.array(node["matrix"], dtype=np.float64).reshape(4, 4).T
        t = np.array(node.get("translation", [0, 0, 0]), dtype=np.float64)
        x, y, z, w = node.get("rotation", [0, 0, 0, 1])
        s = np.array(node.get("scale", [1, 1, 1]), dtype=np.float64)
        r = np.array([
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ])
        m = np.eye(4)
        m[:3, :3] = r * s
        m[:3, 3] = t
        return m

    def mesh_instances(self):
        """Yield (node_index, mesh_index, world_matrix, chain) for every mesh node in the default scene."""
        nodes = self.json.get("nodes", [])
        scene = self.json["scenes"][self.json.get("scene", 0)]

        def walk(i, parent, chain):
            m = parent @ self.local_matrix(nodes[i])
            chain = chain + [i]
            if "mesh" in nodes[i]:
                yield i, nodes[i]["mesh"], m, chain
            for c in nodes[i].get("children", []):
                yield from walk(c, m, chain)

        for root in scene["nodes"]:
            yield from walk(root, np.eye(4), [])

    def primitives(self):
        """Yield dicts with world-space positions, raw positions, indices, uvs, material index."""
        for node_i, mesh_i, world, chain in self.mesh_instances():
            for prim in self.json["meshes"][mesh_i]["primitives"]:
                attrs = prim["attributes"]
                pos = self.accessor(attrs["POSITION"]).astype(np.float64)
                wpos = (np.c_[pos, np.ones(len(pos))] @ world.T)[:, :3]
                idx = self.accessor(prim["indices"]).reshape(-1, 3).astype(np.int64) if "indices" in prim \
                    else np.arange(len(pos)).reshape(-1, 3)
                yield {
                    "node": node_i, "chain": chain, "world": world,
                    "pos": pos, "wpos": wpos, "idx": idx,
                    "uv": self.accessor(attrs["TEXCOORD_0"]).astype(np.float64) if "TEXCOORD_0" in attrs else None,
                    "attrs": attrs, "indices_acc": prim.get("indices"),
                    "material": prim.get("material"), "mode": prim.get("mode", 4),
                }

    def image_info(self):
        """Per image: mime, bytes in container, pixel size read from the PNG/JPEG header."""
        out = []
        for im in self.json.get("images", []):
            bv = self.json["bufferViews"][im["bufferView"]]
            start = bv.get("byteOffset", 0)
            blob = self.bin[start: start + bv["byteLength"]]
            w = h = None
            if blob[:8] == b"\x89PNG\r\n\x1a\n":
                w, h = struct.unpack(">II", blob[16:24])
                fmt = "png"
            elif blob[:2] == b"\xff\xd8":
                fmt = "jpeg"
                i = 2
                while i < len(blob):
                    if blob[i] != 0xFF:
                        i += 1
                        continue
                    marker = blob[i + 1]
                    if marker in (0xC0, 0xC1, 0xC2):
                        h, w = struct.unpack(">HH", blob[i + 5:i + 9])
                        break
                    seglen = struct.unpack(">H", blob[i + 2:i + 4])[0]
                    i += 2 + seglen
            else:
                fmt = "other"
            out.append({"name": im.get("name"), "mime": im.get("mimeType"), "format": fmt,
                        "bytes": bv["byteLength"], "width": w, "height": h})
        return out
