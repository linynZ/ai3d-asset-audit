# 璇玑 3D 化 · 设计规格（方案 A：减面静态模型 + 派蒙式悬浮）

> 日期：2026-07-15（设计于 07-12 会话 brainstorming 呈现，07-15 用户批准实施）
> 状态：已批准 → 实施
> 关联：CompanionController（现 2D billboard 贴图）、[[xuanji-canonical-design]]（正典=小白狐）

## 1. 目标与非目标

**目标**：把探索期跟随玩家的璇玑从 2D 贴图 billboard 升级为真 3D 模型，参考派蒙（原神）的
悬浮同伴形态——全程漂浮、不落地、无移动动画需求。3D 化直接提升游戏每一个探索镜头的观感
（璇玑全程在画面里），也服务 07-16 起录制的宣传/演示视频。

**非目标**（明确不做，保工期）：
- 不做绑骨/骨骼动画（源模型无绑骨，蜷卧姿不可事后绑骨做走路——上限=静态+程序化运动）；
- 不做觉醒真身（九尾天狐）3D；
- 不改 CompanionSpeaker（左下角说话卡）与 CompanionDirector（大脑）；
- 不改战斗内表现（战斗用说话卡，不显示身体）。

## 2. 源资产与技术验证（07-12 已完成）

| 项 | 值 |
|---|---|
| 源模型 | `C:\Users\linyu\CLionProjects\final project\asset model\AI model\player\0cf1d3308afdc6f06885627043fc98c0.glb`（54 MB，仓库外） |
| 几何 | 497,850 面 / 无绑骨 / 零动画 / 蜷卧姿小狐狸（尾环绕身体），bounds 0.87×0.53×1.10 m |
| 贴图 | PBR 三张：basecolor 4096² + normal + metallic-roughness |
| 正典符合 | 高（白毛/耳内星空蓝/金瞳/额头星纹/尾蓝渐变全在，对照定妆图 `aiasset/璇玑.png`） |
| 减面验证 | pymeshlab（pip 全局）保 UV QEM，每轮 `targetfacenum=max(50000, n*0.55)` 迭代 3 轮**收敛于 105,820 面**（混元自动 UV 碎接缝岛是硬约束，到不了 50k）。105k 单 draw call 可接受（全项目 350~500 FPS 余量大） |
| 导出验证 | OBJ 导出 OK；pymeshlab `save_textures` 会报错 → 贴图需从 GLB 单独提取（PIL） |

**姿态正典化**：蜷卧姿不是缺陷——定调为「卧在星光上的小狐狸」，与星光坐垫（§4.3）
组成完整视觉语言：璇玑卧在一小片星光上漂浮同行。

## 3. 资产管线（`tools/decimate_xuanji.py`，AI 侧一次性跑）

1. **减面**：pymeshlab 载入 GLB → 保 UV QEM 迭代（同验证参数）→ ~105k 面；
2. **贴图提取**：直接解析 GLB（JSON chunk + BIN chunk）用 PIL 提取——
   basecolor 降采样到 **2048**、normal 到 **1024**、**弃 MR**（材质统一 metallic=0，
   smoothness≈0.35，卡通渲染语境下 MR 贴图无收益且省 21 MB 级贴图内存）；
3. **产物**（入库，Unity 原生 OBJ 导入，绕开 UniGLTF）：
   - `ChronoTraveler/Assets/Art/Characters/Companion/xuanji_body.obj`
   - `ChronoTraveler/Assets/Art/Characters/Companion/xuanji_basecolor.png`
   - `ChronoTraveler/Assets/Art/Characters/Companion/xuanji_normal.png`
   - .obj 的 ModelImporter .meta 由 Unity 首次导入生成（烘焙工具按路径载入，GUID 稳定性无依赖）。

## 4. Unity 侧设计

### 4.1 烘焙工具 `Editor/XuanjiModelTool.cs`

菜单 `ChronoTraveler/Content/Build Xuanji 3D Body`，镜像 NPCModelSetupTool 范式但按悬浮体定制：

- 按路径载入 OBJ 模型资产 → 实例化 → 解包；
- 生成 URP/Lit 材质（basecolor→`_BaseMap`，normal→`_BumpMap` 标记法线，metallic=0，
  smoothness 0.35），存 `Resources/CharacterModels/xuanji_Mats/`；
- **归一化**：体长（水平最长轴）≈ **0.6 m**（派蒙级体量，NPC 工具按身高归一不适用卧姿）；
- **枢轴 = 渲染包围盒中心**（悬浮体挂在锚点上，非 NPC 的脚底接地枢轴）；
- **Face Yaw 常量**字段可调（默认 180，混元正视导出朝 -Z 的既有经验），预期 Play 后微调 1 轮；
- 产物 `Resources/CharacterModels/xuanji.prefab`。

### 4.2 CompanionController 改造（资产缺失免疫）

`BuildBody()` 优先 `Resources.Load<GameObject>("CharacterModels/xuanji")`：

- **命中 → 3D 路径**：实例化模型（无 Billboard/SpriteRenderer），跟随逻辑复用现有右肩锚点+
  正弦悬浮；新增程序化生命感——缓慢**俯仰摇摆**（漂浮呼吸感）+ 按玩家移动方向**倾斜**
  （跟随时身体前倾/转向），朝向=水平面向移动方向、静止时缓转朝相机侧；
- **未命中 → 现有 2D 贴图路径原样保留**（免疫哲学，同 VideoGate/键 art：资产没进库游戏照跑）。

### 4.3 星光坐垫（3D 路径专属）

模型下方挂一个小型粒子系统：半径 ~0.5 m、低亮度金/冰蓝软点（复用
`PropVisuals.SoftDotTexture()` + `AdditiveMaterial()` 现成配方），缓慢上飘消散——
「卧在星光上」的字面落地。亮度刻意压低（同伴不能抢主角/场景的视觉焦点）。

### 4.4 情绪气泡（3D 路径下 SetMood 的去处）

2D 路径的 SetMood 换表情贴图；3D 模型静态无表情，改为**头顶情绪气泡**：
现有 6 张 mood 贴图（`Portraits/xuanji_*`）缩小挂头顶 billboard（SpriteRenderer +
Billboard），`SetMood(非 Idle)` 时显示 ~3 s 后淡出；Idle 不弹泡。
CompanionDirector 零改动（仍只调 `SetMood`）。

## 5. 性能兜底与升级轨

- **兜底**：若 105k 面在目标机实测有压力（预期不会），混元资产库对该模型一键重导 50k 版
  覆盖 OBJ 重跑烘焙即可，代码零改动；
- **升级轨（方案 B，封版后可选）**：混元绑骨动画版做好后按同 prefab 路径覆盖即升级。

## 6. 验收

1. 离线 csc 编译 0 错误（`tools/verify_compile.sh`）；
2. 【用户】开 Unity 导入新资产（生成 .meta）→ 跑 `Build Xuanji 3D Body` 菜单 → 提交产物；
3. 【用户】Play 走查：枢纽/时代图跟随、主菜单/暂停/战斗/过场正确隐藏、答对答错情绪气泡、
   星光坐垫观感、faceYaw 朝向（预期迭代 1~2 轮微调）。
