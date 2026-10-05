# 最终决战设计 spec（Finale Battle）

> 2026-07-09 头脑风暴定稿。形态 B（半可玩：困境演出 → 觉醒变身 → 真实翻盘战）＋ CG 驱动过场 ＋ 双人声曲。
> 本 spec 是游戏收官的最后一块拱顶石：完成后解锁视频录制与论文写作（用户铁律：游戏完成才开工）。
> 论文截止 2026-07-22；代码轨预算 2–3 天，美术/音乐轨用户并行。

## 0. 一句话设计

五星归位后，星引宫浮现深渊之门；旅者踏入「之海深渊」，直面五时代错乱的本源——**时之扭曲·本源／The Unwritten（未被书写者）**。困境段攻击尽数被「不确定性」消解（Unyielding 无敌相位）；剧情节点璇玑挺身、**觉醒九尾天狐**，以「确定的知识之锚」将本源**钉进确定态**（它被迫显出真形，才变得可被击败）；玩家以觉醒强化态 + 五域融合题库完成翻盘，迎来真结局。

**哲学-机制-视觉三层同构**：时间使非当下的过去/未来不确定 → 错乱之源；知识与记忆是对抗不确定性的锚 → 答题=钉住它；无定形异常体 → 被钉进确定态的实体真形。

## 1. 决战流程（六拍）

1. **入口**：现有 `finale_demo` 预告过场播完后（AllBuiltErasComplete），Hub 星引宫中心浮现**深渊之门**（程序化暗色裂隙，PropVisuals 风格），交互（可配 `cg_gate`）→ `TravelToMap("70_Finale", "finaleSpawn")`。
2. **入场过场 `finale_enter`**：之海深渊，本源现身（`cg_boss_reveal`）。璇玑：五时代的错乱皆源于它；时间让过去与未来不确定，正因有它。
3. **困境战（Unyielding 段）**：同一场战斗的第一阶段。Boss 处于「时间扭曲·无敌相位」——对 Boss 的最终伤害钳制为 0，UI 飘「被时间消解…」（`battle.unyielding` 键）而非数字。玩家照常选技能答题——**答题体验保留，结果被叙事否定**。
4. **觉醒节点**：第 3 回合结束 或 玩家 HP 首次 <50%（先到为准，纯谓词）→ 战斗暂停（等待 CutsceneManager）→ 播 `finale_awaken`（`cg_xuanji_shield` → `cg_awaken` → `cg_empower`）→ 回到**同一场战斗**：解除 Unyielding、施加觉醒增益、（可选）Boss 换真形模型。
5. **翻盘战**：Boss 五元素相位轮转（HP 每降 20% 切相），玩家以觉醒态+融合技能+五域全池题库击破。战败 → DefeatPanel 重试，**直接以觉醒态重开翻盘段**（跳过困境戏）。
6. **胜利**：`finale_victory`（`cg_seal` → `cg_ending`），真结局；回 Hub。`finaleCompleted` 存档；结局过场 PlayOnce，Boss 战可重复挑战。

## 2. 战斗机制

### 2.1 Boss 资产 `finale_boss`（新建 EnemyDefinition，`_Content/Finale/Enemies/`）

- 名：中「时之扭曲·本源」／英 "The Unwritten"（ui_strings `enemy.finale_boss`）。
- 数值：**HP 700 / atk 36 / def 19**（trade_boss 560/32/17 再上一档 ~+15–25%；觉醒增益下约 8–10 回合，实机可调）。
- `phaseElements = [history, architecture, culture, philosophy, geography]` 五相轮转（现有 UpdateBossPhases 零改动）。
- `isBoss=true` → Bloom understand+ 抽题（现有机制）。
- 立绘：`Art/Portraits/Enemies/finale_boss.png`（用户生成，BossPortraitSetupTool 管线）。

### 2.2 Unyielding 无敌相位（BattleSystem 最小侵入）

- BattleSystem 增 `unyielding` 标志（由 BattleTrigger/encounterId==`finale_boss` 时激活）。
- 激活期间：对 Boss 的最终伤害钳制 0；IBattleView 增一条消息路径显示「被时间消解…」；敌方照常攻击玩家。
- 觉醒谓词（纯函数 `Battle/Logic/FinaleScript.cs`）：`ShouldAwaken(roundIndex, playerHpNormalized) => roundIndex >= 3 || playerHpNormalized < 0.5f`。触发后：battle 协程等待 `CutsceneManager.IsPlaying==false`（CutsceneManager 快照/恢复 prevState=InBattle，现有机制兼容）→ 解除 unyielding → 施加觉醒。

### 2.3 觉醒态（玩家侧战力跃升）

1. 增益：atk +50%、专注每回合恢复 +2（CombatStats 现有字段临时修正，战斗结束还原）。
2. 融合技能「星芒之契／Starlit Covenant」：新 SkillDefinition（power 40 / cost 4），新增 `wildcardElement` 布尔——使用时元素在五域中随机 roll（决定抽题域与克制计算）。终局赌克制 vs 稳打的决策点。
3. 五域融合题库：70_Finale 的 MapDescriptor.regionId 留空 → QuizPool 走「无地区跨抽但仍按类目」路径（已有 QuizPoolTests 覆盖，零新逻辑）——500 题全池终局大考。
4. `SaveData.finaleAwakened`：重试/读档跳过困境段直接觉醒态。

### 2.4 Boss 视觉（双轨）

- **保底（默认）**：放大版 AnomalyVisual——体积 3–4×、五色元素环绕轨随相位切色、扭曲脉冲加强。
- **实验轨**：用户走混元图生 3D（概念图建议「碎裂编年碑巨像」——五文明残碑/星盘/沙漏碎块聚合的雕塑感实体，混元擅长区）。若出品合格 → 觉醒后「被钉进确定态」时换真形模型（ModelSwapper 钩子，`Resources/CharacterModels/finale_boss_trueform` 存在即换，缺失走保底）。设计不依赖实验轨。

## 3. 场景 `70_Finale`「之海深渊」

- 新编辑器工具 `Editor/FinaleSetupTool.cs`，菜单 `ChronoTraveler/Content/Build Finale (Abyss)`：
  - 天空盒：`aiasset/final screen.png`（7680×3840，已验证 2:1 equirect）导入 `Assets/Resources/Skyboxes/sky_finale.png` → Panoramic Skybox 材质；
  - 星石圆形平台（程序化，直径 ~40m，EraBuildEngine 制件复用），边缘星尘粒子；
  - `finaleSpawn` 出生点 + 中央 `finale_boss` BattleTrigger + 战后回 Hub 传送阵（fromFinale 落点）+ FallRescue + 深蓝紫雾氛围；
  - MapDescriptor（regionId 留空、memoryTarget=0）；场景加入 Build Settings。
- Hub 深渊之门：`FinaleTrigger` 扩展——`finale_demo` 已播 && AllBuilt → 在星引宫中心生成可交互暗裂隙（IInteractable → 可选 cg_gate → TravelToMap）。运行时程序化生成，不改 Hub 场景文件。

## 4. 过场与 CG

### 4.1 过场系统扩展：`cg` 步骤类型

- `CutsceneStepKind` 增 `Cg`（纯函数解析 + CutsceneStepKindTests 同步）。
- `CutscenePlayerUI` 增全屏 CG 层：`Resources/CG/<id>.png` 淡入显示，配底部文本；**资产缺失静默跳过**（VideoGate 哲学——CG 未生成时过场退化为纯对白，不阻塞）。

### 4.2 新过场序列（CutsceneData.json，全双语）

- `finale_enter`：入渊 + 本源现身（cg_boss_reveal）+ 璇玑解题「错乱的本源」。
- `finale_awaken`：璇玑挺身（cg_xuanji_shield）→ 九尾觉醒（cg_awaken，全场最高光）→ 灌注（cg_empower）→「以确定之锚，钉住不确定的时间」。
- `finale_victory`：封缄（cg_seal）→ 真结局（cg_ending）——收束「旅者与璇玑同行／人与 AI 同行」立意，呼应旅者手记。
- 深渊之门交互线 + `cg_gate`（可选）。

### 4.3 CG 清单（用户生成；★=必配 4 张；16:9 ≥1920×1080；含璇玑必带 `aiasset/璇玑.png` 参考）

★cg_boss_reveal ／ ★cg_xuanji_shield ／ ★cg_awaken ／ ★cg_ending ／ cg_gate ／ cg_struggle ／ cg_empower ／ cg_trueform（兼作建模概念图）／ cg_seal ／ 基础璇玑立绘刷新（反哺全局）。
（每张的中英提示词另行提供——生成时逐张给，含风格锚定：深蓝紫星云+金星光+冰蓝，光之堆叠，禁纯色平涂。）

## 5. 音频

- **两首人声曲**（词与生成手册已入库 `docs/pipelines/finale_vocal_songs.md`，PR #167）：
  - 主题曲《星夜同渡／Across the Starlit Sea》→ 标题界面 + cg_ending；
  - 决战曲《书写者／We Write the Light》→ 翻盘段 BGM（觉醒过场后切入，歌曲 Bridge 情绪正对觉醒节拍）。
  - 双语版本随游戏语言切换（AudioManager 按 `_en/_zh` 后缀选，小逻辑）。
  - 命名：`bgm_theme_vocal_{en,zh}`、`bgm_finale_battle_{en,zh}`，放 `Resources/Audio/BGM/`。
- 困境段：复用现有 boss 战曲（压抑感够用）；胜利 stinger 复用。
- 合规：定稿版必须付费订阅期内生成；旅者手记页脚署名。

## 6. 本地化与测试

- 全部新文本走 ui_strings / LocalizedText 双语：`enemy.finale_boss`、`battle.unyielding`、深渊之门提示、过场全文、（若有）journal 条目 `battle_finale_boss`。
- 纯函数 + NUnit：`FinaleScript.ShouldAwaken`（边界：round 2/3、hp 0.5±）、`CutsceneStepKind` cg 解析、（若抽出）wildcard roll 的域覆盖。
- 红线：China/Egypt/希腊/罗马/丝路场景与工具零改动；现有敌人/任务资产只读；`finale_boss` 是唯一新敌人资产。

## 7. 分工与工期

| 轨 | 内容 | 谁 | 估时 |
|----|------|----|----|
| 代码 | FinaleSetupTool、Unyielding/觉醒/wildcard、finale_boss 资产、cg 步骤、三段过场、门与接线、双曲接线、测试 | AI | 2–3 天 |
| 美术 | ★4 CG（+加分项）、finale_boss 立绘、Boss 建模实验、璇玑立绘刷新 | 用户（并行） | 并行 |
| 音乐 | 双平台 A/B → 付费定稿 4 版本 | 用户（并行） | 并行 |
| 验证 | Unity 导入编译 → Build Finale 菜单 → Play 全流程走查 | 用户 | 半天 |

## 8. 明确不做（YAGNI）

- 不重写战斗为多单位（璇玑不作为战斗实体入场，觉醒=过场+玩家增益）。
- 不做真败重开的困境段（软锁与挫败风险）。
- 不做新题库内容（500 题全池已够终局大考）。
- 不做 HunyuanWorld 高斯泼溅决战场（已定案：8K 全景天空盒为正选）。
- 不做困难模式/多结局。

## 9. 二段式决战重构（2026-07-09 用户拍板 → **同日实施完成** ✅）

> 实施记录：觉醒 4 帧 CG 序列（PR#181）与 Boss 真形烘焙就绪后当日落地。
> BattleSystem 脚本化收场（`EndBattle(interrupted)`：无胜负结算、标记 FinaleAwakened、
> `IBattleView.OnBattleInterrupted` 收 UI）→ FinaleTrigger 导演（播 finale_awaken →
> `FinaleEmbodiment.Apply` 舞台切换：巨物消散、真形 prefab 立于平台 (0,0,8) 面向出生点）→
> 二阶段=平台上 E 交互开战（FinaleAutoStart 已觉醒即跳过；StartBattle 觉醒路径切人声决战曲）。
> 入图按存档恢复舞台（重试/通关后重访均为实体形态）。全部运行时实现，零场景重建。

**二段式决战（替代现行"同一场战斗内觉醒"）：**
1. 一阶段（Unyielding 困境战）打满节拍后**直接结束战斗**（非胜非败的脚本化收场）；
2. 回到探索态，璇玑过场说明情况（"打不中"的揭晓挪到这里）→ 接觉醒 CG/动画；
3. **Boss 从无形巨物「被钉进确定态」→ 以有具体建模的生物形态生成于平台之上**（用户 Boss 建模实验轨的 GLB 落点；巨物消失/坠落演出）；
4. 主角走向实体 Boss **主动交互触发二阶段战**——此时可被击中（觉醒增益+融合技照旧）。

动机：把"无形→有形"做成可见的舞台变化而非仅数值开关；给觉醒 CG 一个专属演出窗口；实体 Boss 战在平台上对峙更有决斗感。
实施要点：BattleSystem 需支持"脚本化收场"（不判胜负不发结算）；SaveData.finaleAwakened 语义不变（跳一阶段）；FinaleAutoStart 只触发一阶段；二阶段是平台上的新 BattleTrigger（正常 E 交互）。
