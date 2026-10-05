# 切片 B：璇玑同伴系统 — 设计与开发方案

> 日期：2026-06-28　状态：待用户复核
> 上游：`2026-06-27-excellence-roadmap-and-slice-A-design.md`（卓越化四切片 §0）、`2026-06-20-narrative-and-presentation-design.md`（§1.2 璇玑设定）。
> 切片 A（战斗手感&教育可读性）已完成入主线，本文为 **#2 切片 B**。

---

## 0. 定位与用户拍板（2026-06-28）

璇玑（Xuanji，昵称玑玑/Jiji）= 非人型星图守护兽萌宠同伴，贯穿全程陪伴/引导 Astraea，是叙事情感锚点 + 教学之声 + 喜剧调剂。审查指出"璇玑仅有 6 张表情立绘、0 代码实现"是离设计差距最大的一项。

**用户三项决策**：
1. **视觉形态**：2D 漂浮萌宠**现做全**（用已有 6 表情立绘），接入系统预留"可插拔 3D"。
2. **教学之声**：璇玑**接管首战引导口吻 + 关键时刻旁白**（数据驱动外置 JSON）。
3. **觉醒 CG（真·守护兽形态）**：**本切片不做**，后置切片 C/终局。

**现成可复用资产**：6 张表情立绘 `Resources/Portraits/xuanji_{happy,neutral,panic,smug,surprised,worried}.png`；`BattleEvents.OnAnswerResolved/OnBattleStarted/OnBattleEnded`；`Effects/Billboard`（朝相机）；`SceneFlowManager.OnMapEntered`、`CollectionManager.OnItemCollected`、`MemoryProgress.OnMemoryChanged/Full`；`BattleTutorialCoach`（切片 A）；`ScreenBanner`/Overlay UI 范式。

---

## 1. 设计总览：身体 / 声音 / 大脑 三分离

为可读、可测、可独立替换，把同伴拆成三个单一职责单元 + 数据：

| 单元 | 职责 | 形态 |
|------|------|------|
| **CompanionController（身体）** | 探索期世界中的 2D 漂浮萌宠：跟随玩家、朝相机、悬浮起伏、按情绪切表情 | 世界 `SpriteRenderer` + Billboard |
| **CompanionSpeaker（声音）** | 统一的"璇玑说话"UI：左下角小头像 + 一句台词（打字机、自动消失、队列） | 屏幕空间小 UI（自建 Canvas） |
| **CompanionDirector（大脑）** | 唯一事件订阅者：把游戏事件→情绪 + 选台词，驱动 Body 切表情、Voice 说话 | 自启动单例，无可视 |
| **数据**：`CompanionLines.json` + `CompanionLines.cs` | 双语台词按触发器分组、每组多变体随机；纯选词函数可单测 | 外置 JSON |

> **要点**：身体=陪伴/魅力（纯表现），声音=表达（探索+战斗统一一个 UI），大脑=唯一接事件处，台词外置。这样 Body/Voice 是"哑视图"，Director 是薄逻辑，台词与代码解耦——契合项目数据驱动 + 事件驱动 + 接口解耦的工程论证。

---

## 2. 情绪与触发映射（教育/喜剧落点）

`CompanionMood`：`Idle / Happy / Panic / Smug / Surprised / Worried` → 1:1 映射 6 张表情。

| 触发器（trigger key） | 情绪 | 声音（示例语气，实际多变体外置） | 来源事件 |
|----------------------|------|----------------------------------|----------|
| `enter_hub` | Smug | "欢迎回到星引宫，旅者。" | OnMapEntered(hub) |
| `enter_era` | Surprised | "华夏的记忆…蒙尘得厉害，走，去修复它！" | OnMapEntered(非hub) |
| `collect_fragment` | Happy | "又一片记忆归位！" | OnItemCollected |
| `memory_progress` | Idle/Happy | （进度过半时）"长河渐渐清亮了。" | OnMemoryChanged 阈值 |
| `gate_open` | Surprised | "封印松动了——大错乱要醒了，准备！" | OnMemoryFull / 门解封 |
| `battle_start` | Smug | "用你所学的真知，驱散它！" | OnBattleStarted |
| `battle_correct` | Happy | "答得好！这一击很漂亮！" | OnAnswerResolved(true) |
| `battle_wrong` | Panic | "呜…答错了，别慌，看清属性再来！" | OnAnswerResolved(false) |
| `battle_win` | Happy | "净化成功！记忆回来了。" | OnBattleEnded(win) |
| `battle_lose` | Worried | "撑住…我们去出生点重整旗鼓。" | OnBattleEnded(lose) |

- **防刷屏**：同一 trigger 有最小冷却（如 collect/correct/wrong 各设冷却，避免连续触发轰炸）；Director 维护 per-trigger 冷却时间戳。
- **战斗内**：身体（世界萌宠）隐藏，声音（左下 UI）照常——战斗的情绪反馈即"答对欢呼/答错抱头"，正是教学正反馈。

---

## 3. 各单元设计

### B0. 数据层：CompanionLines（`Companion/CompanionLines.cs` + `Resources/CompanionLines.json`）

**丰富化内容模型（三类）** —— 不只反应式单句，支持碎碎念与多句小故事，且全数据驱动、可无限扩写（作者/AI 续写只改 JSON）：
```
{
  "barks":   [ { "trigger":"battle_wrong", "lines":[ {"zh","en","mood"}, ... ] } ],   // 事件触发·单句·多变体轮换
  "chatter": [ { "id","era":"china|any", "mood", "zh","en" } ],                         // 探索 idle 池·随机·可重复
  "stories": [ { "id","era":"china|any", "oneShot":true,
                 "steps":[ {"zh","en","mood"}, ... ] } ]                                // 多句小故事/趣事·讲一次·持久
}
```
- `CompanionMood` 枚举（Idle/Happy/Panic/Smug/Surprised/Worried）+ `MoodSprite(mood)`→`xuanji_*`。
- 复用 `LocalizedText` 双语。运行时 `CompanionLines.Load()` 读 Resources。
- **纯选词逻辑入 Logic 程序集可单测**（镜像 QuizPool 范式）：`Companion/CompanionPool.cs` 定义极小接口 `IEraScoped { string Era }` + 纯静态 `ForEra<T>` / `PickByCounter<T>`（按 era 过滤 + 计数轮换，无引擎依赖）；运行时 DTO 实现该接口。stories 的"讲过一次"用 `SaveData.toldCompanionStories`（持久，镜像 playedCutscenes）。

**璇玑语音圣经（写台词时遵循）**：北斗枢机·璇玑 = 古老星界守护巨兽寄身圆滚傻萌小形态；宏大 ↔ 团子的反差即魅力。俏皮温暖带点得意/调侃，给主角起昵称（玑玑亦自称）；多数插科打诨，偶尔闪过古老智慧/哀伤（埋真身与错乱起源钩子）；口头禅"星辰告诉我…（先不说）"。情绪曲线：轻松为主 + 周期性真诚/沉桥段，随记忆修复推进钩子加重，导向切片 C/终局觉醒。

**内容覆盖（China 起步，可扩）**：① barks 覆盖 §2 全触发器，每触发 3–5 变体；② chatter 池 ~12–20 条（团子吐槽 + 华夏轻知识彩蛋 + 观察）；③ stories 3–5 段（璇玑远古记忆 / 星图往事 / 错乱起源伏笔 / 一段真华夏史趣闻），每段 3–5 句、oneShot。后续四时代各自扩 chatter/stories 即可。

### B1. CompanionSpeaker（声音 UI，`Companion/CompanionSpeaker.cs`）
- 自启动单例 + 自建屏幕空间 Canvas（镜像 `ScreenBanner`/`MemoryHUD` 范式）。左下角：小圆框头像（按 mood 切图）+ 台词条（打字机）+ 说话者名"璇玑"。
- API：`Say(CompanionMood mood, string line, float hold = 3f)`；内部队列，逐条播放，自动淡出。空 line 则只切头像不弹字。
- 显隐：始终可用（探索 + 战斗都在左下；战斗 UI 在右侧/中央，不冲突）；Paused/主菜单隐藏。

### B2. CompanionController（身体，世界萌宠，`Companion/CompanionController.cs`）
- 自启动单例（DontDestroyOnLoad）。运行时生成 `SpriteRenderer`（xuanji 当前情绪图）+ 软光晕 + `Billboard`。
- 跟随：每帧平滑 lerp 到玩家身后上方偏移位（over-shoulder hover），叠加正弦悬浮起伏；找不到玩家则隐藏。
- 显隐门槛：`GameState.Exploring` 显示；`InBattle/InCutscene/Paused/GameOver` 隐藏（镜像现有 HUD 门槛）。
- 表情：`SetMood(mood)` 切 sprite（由 Director 调）。
- ⚠️ 立绘是半身像，作世界漂浮萌宠为 MVP 取舍（软光晕 + 小尺寸弱化违和）；后续可换真 3D 漂浮模型（接入点：`SetModel`/类 NPCController.TrySwapModel，预留不实现）。

### B3. CompanionDirector（大脑，`Companion/CompanionDirector.cs`）
- 自启动单例。**唯一**订阅以下事件，映射 trigger→(mood,line)，调用 Controller.SetMood + Speaker.Say：
  - `SceneFlowManager.OnMapEntered` → enter_hub / enter_era
  - `CollectionManager.OnItemCollected` → collect_fragment（冷却）
  - `MemoryProgress.OnMemoryChanged`（过阈值）/ `OnMemoryFull` → memory_progress / gate_open
  - `BattleEvents.OnBattleStarted/OnAnswerResolved/OnBattleEnded` → battle_*（correct/wrong 冷却）
- 订阅/退订配平（BattleEvents 静态总线域重载已自重置；Director 持久单例订阅一次，OnDestroy 退订）。
- 选词：`CompanionLines.Pick(trigger, counter++)`，counter 递增实现"轮换变体"（无需随机源）。

### B4. 璇玑接管首战引导（改 `Battle/BattleTutorialCoach.cs`）
- 教练卡加**璇玑头像槽**（左侧）+ 说话者名"璇玑"，3 步台词改为璇玑的口吻（亲和、点出"知识=战力"）。
- 头像按步切表情：step1 smug（出招讲解）/ step2 neutral（答题）/ step3 happy（克制）。
- 复用切片 A 的 coach 流程与 `SaveData.tutorialBattleDone`，非首战零开销不变。

### B5. 本地化与命名
- `ui_strings.json` 加 `companion.name`（璇玑/Xuanji）、`companion.nickname`（玑玑/Jiji）；首战引导 tut.battle.* 调整为璇玑口吻（双语）。
- 台词正文在 `CompanionLines.json`（双语）。

### B6. 测试（EditMode）
- `CompanionLines.Pick`：trigger 命中/缺组回退空/变体轮换/空输入。纯函数，放 Tests/Editor。

---

## 4. 影响面（新增 / 改动 / 复用）
- **新增**：`Companion/CompanionController.cs`、`Companion/CompanionSpeaker.cs`、`Companion/CompanionDirector.cs`、`Companion/CompanionLines.cs`（含 CompanionMood）、`Resources/CompanionLines.json`、`Tests/Editor/CompanionLinesTests.cs`。
- **改动**：`Battle/BattleTutorialCoach.cs`（加璇玑头像/口吻）、`Resources/Localization/ui_strings.json`（companion.* + tut 口吻）。
- **复用**：6 xuanji 立绘、Billboard、ScreenBanner/MemoryHUD 自建 Canvas 范式、BattleEvents/SceneFlow/Collection/MemoryProgress 事件、LocalizedText、切片 A 的 BattleTutorialCoach + SaveData。
- **隔离/可测**：Director 是唯一事件耦合点；Controller/Speaker 为哑视图；CompanionLines 纯选词可单测；台词外置。各单元可独立理解/替换（3D 模型、星图、觉醒 CG 都是后续可加点，不在本切片）。

## 5. 不在本切片范围（YAGNI / 后置）
- **3D 漂浮萌宠模型**（混元图生3D，需外部生成，预留 SetModel 接入点不实现）。
- **觉醒 CG / 真·守护兽形态**（切片 C/终局）。
- **枢纽记忆星图可视化**（独立小任务，宏进度 viz，可单独做）。
- **配音**、**Live2D 动态立绘**、其余四时代专属台词（先 China + 通用）。

## 6. 风险
- **半身立绘作世界萌宠违和** → 软光晕 + 小尺寸缓解；接入点预留 3D 替换。MVP 可接受。
- **台词刷屏** → per-trigger 冷却 + 队列。
- **事件泄漏** → Director 单点订阅 + OnDestroy 退订；BattleEvents 静态总线已域重载自重置。
- **离线无法编译/实机验证** → 严格代码审查 + CompanionLines 纯函数单测；新脚本需 Unity 导入生成 .meta + Play 验证（同切片 A）。

## 7. 开发顺序（实施时）
B0 数据层(枚举/Lines/JSON/测试) → B1 Speaker(声音 UI) → B2 Controller(世界身体) → B3 Director(接事件驱动二者) → B4 改 BattleTutorialCoach 接璇玑 → B5 本地化命名。每步小、可独立提交；Director 完成后即可整体体验。

## 8. 论文取材
- 又一个"数据驱动(台词外置) + 事件驱动(Director 单点订阅) + 接口解耦(哑视图)"可复用系统，强化 Design&Implementation 工程论证。
- 同伴的"答对欢呼/答错抱头"是 Malone 内在动机框架中"情感支架 + 即时正反馈"的具体落地，呼应教育有效性章节。
- AI 资产管线证据：6 表情立绘的生成 + 预留的混元 3D 接入点（后续填）。
