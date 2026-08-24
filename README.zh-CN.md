# 即梦 Seedance 2.5 提示词优化 Agent Skill

将粗略创意或失败的 Seedance 2.5 生成结果转化为经过验证、可直接复制的提示词。

[English](README.md) | [简体中文](README.zh-CN.md)

[![CI](https://github.com/silentbuilds/seedance-prompt-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/silentbuilds/seedance-prompt-forge/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/silentbuilds/seedance-prompt-forge)](https://github.com/silentbuilds/seedance-prompt-forge/releases/latest)
[![License: MIT](https://img.shields.io/github/license/silentbuilds/seedance-prompt-forge)](LICENSE)

[安装](#安装) · [查看转换对比](#前后对比) · [下载最新版 Skill ZIP][latest-zip] · [更多示例](#更多示例)

Seedance Prompt Forge 是一个开放的 [Agent Skill](https://agentskills.io)，用于编写、审计和修复即梦 Seedance 2.5 视频提示词。它为每个参考素材命名并绑定角色，组织多阶段事件，把模糊的创作方向转化为可见和可听的线索，并在生成前运行确定性检查。

它支持 Claude Code 与 Cowork、Codex CLI、Cursor、Cline、GitHub Copilot、Gemini CLI，以及其他兼容 Agent Skills 的工具。可在浏览器上传的 ZIP 和单文件构建版本覆盖仅聊天的使用场景。

## 前后对比

同一个创意在明确参考素材、时间安排、连续性、表演和音频后，会更容易被模型遵循。

### 原始提示词

下方代码块保留原文，避免改变可复制提示词的字面语义。

```text
Create a 30-second vertical video in 9:16 format using the uploaded image, image1.jpg, as the visual reference for the main character. Keep the woman’s face, hairstyle, clothing, and overall appearance consistent throughout the video. Use audio.mp3 as the reference for her voice whenever she speaks.

The video begins on a rainy night, with the woman walking alone along a neon-lit city street. She appears sad, lost, and deep in thought. Alternate between wider shots of her walking and close-up shots of her face, falling raindrops, reflections on the wet street, and the surrounding city lights. Near the end, the rain gradually stops and the sky begins to brighten. She looks up, pauses, and gives a subtle smile, suggesting a renewed sense of hope.

Use a realistic, beautiful, and cinematic visual style. Keep camera movements and scene transitions smooth, and avoid changes or distortions to the character’s appearance.
```

### 由 Seedance Prompt Forge 优化后

下方代码块同样保留原始可执行语法。

```text
[Generation Goal]
Generate a photorealistic cinematic story of a solitary woman moving from quiet sadness to restrained hope on a rainy neon-lit city street.

[References]
@Image 1 defines the woman's face, hairstyle, clothing, and overall appearance. Use only those identity and wardrobe features; do not use the image background, composition, or any other people.
@Audio 1 defines the woman's speaking voice for her final line. Do not use it as music or as the city ambience.

[Stage 1 — 0-10 seconds]
Initial state: exactly one woman walks alone along a rain-soaked city street at night; cool blue and magenta neon signs reflect in the puddles. Her shoulders are slightly drawn in, her gaze stays low, and her pace is slow and thoughtful.
Primary event: a smooth wide follow shot tracks beside and slightly behind her as she walks through the rain.
End state: she reaches a brighter pool of reflected neon light, still walking alone in the same clothing.

[Stage 2 — 10-20 seconds]
Continue from the previous stage: keep the same continuous woman, face, hairstyle, clothing, street direction, rain intensity, and night setting.
Primary event: use smooth match cuts between close-ups of her pensive face, raindrops striking the wet pavement, rippling neon reflections, and blurred city lights; her eyes briefly scan the empty street and her lips press together.
End state: she slows to a stop beneath the fading rain, her face in close-up and her eyes beginning to lift.

[Stage 3 — 20-30 seconds]
Continue from the previous stage: the same woman remains alone and unchanged in the same spot. The rain gradually stops and the dark sky begins to brighten with soft warm dawn light.
Primary event: begin in a medium-wide view, then gently push in as she raises her head, takes a small steadying breath, and gives a subtle, believable smile. Dialogue language: English. In a quiet, reflective delivery using @Audio 1, the woman says: {Maybe there's still a way forward.}
End state: finish on a close-up of her calm face turned toward the brighter sky, with only a few residual drops on her hair and clothing.

[Maintain Consistency]
Keep exactly one continuous woman throughout; do not duplicate, split, replace, or distort her. Preserve her face, hairstyle, clothing, age, and overall appearance from @Image 1 across every shot. Maintain realistic rain physics, natural walking and facial motion, smooth camera movement, smooth match-cut transitions, and a coherent progression from cool neon night to softly warming dawn. No subtitles or on-screen text.

[Audio]
Ambience: steady rain, distant traffic, and a subdued nighttime city bed through the first two stages; the rain ambience thins naturally in the final stage.
Sound effects: soft footsteps on wet pavement and raindrops striking puddles.
Music: none.
```

### Skill 做了哪些改变

| 改进 | 作用 |
|---|---|
| **明确的参考角色** | 将文件名转为 `@Image 1` 和 `@Audio 1`，说明每个参考控制什么，并排除不需要的背景、人物、构图、音乐和环境声。 |
| **阶段时间安排** | 将宽泛的 30 秒叙事弧拆为三个事件预算，每个阶段只有一个主要变化。 |
| **连续性与结束状态** | 将同一人物、服装、方向、天气、地点和情绪推进从一个阶段带到下一个阶段。 |
| **可观察的表演** | 用低垂视线、收紧肩膀、缓慢步伐、扫视、调整呼吸和克制的微笑替换“悲伤、迷失、沉思”。 |
| **镜头意图** | 指定具体的跟拍、匹配剪辑、特写、中广景和最终推近，而不只要求镜头平滑。 |
| **身份护栏** | 锁定唯一且连续的女性角色，并明确禁止复制、分裂、替换和失真。 |
| **音频计划** | 分离声音、环境声、音效和音乐；为声音参考提供实际台词，并声明语言和表达方式。 |
| **生成参数** | 将 9:16 留在生成控件中而不是写进提示词，同时让时间戳分配 30 秒的事件预算。 |

此对比展示提示词结构，不代表保证的视觉结果。输出仍取决于模型、输入素材、生成设置和随机性。

## 支持的工作流

| 工作流 | Skill 提供的结构 |
|---|---|
| 文生视频 | 主体、事件、场景、风格、镜头和音频结构 |
| 图像/视频/音频参考 | 单独绑定、包含项、排除项和按场景选择 |
| 30 秒多阶段视频 | 带时间的阶段、连续性声明和明确结束状态 |
| 失败的生成 | 症状到原因的诊断与最小修正 |
| 视频编辑 | 唯一编辑母版、编辑范围、数量锁和时间线继承 |
| 前向/后向延展 | 边界帧、动作、空间和音频连续性 |
| 首尾帧与关键帧 | 每张图一个角色和有序状态转换 |
| 分镜与块状预演 | 明确的结构、动作、素材和风格继承 |
| 对话与表演 | 语言、声音、表达、情绪、环境声、音乐和音效 |

## 安装

### Skills CLI

使用开放的 Skills CLI 将公共包安装到当前项目：

```bash
npx skills add silentbuilds/seedance-prompt-forge
```

该命令已针对公共仓库验证：它会发现标准的 `skills/seedance-prompt-forge/` 包，并为已检测到的兼容 Agent 将 `SKILL.md`、参考文件和可选 linter 安装至 `.agents/skills/seedance-prompt-forge/`。

### GitHub CLI — 推荐

安装前先预览包：

```bash
gh skill preview silentbuilds/seedance-prompt-forge seedance-prompt-forge
gh skill install silentbuilds/seedance-prompt-forge seedance-prompt-forge
```

安装后请新开一个 Agent 会话；Skill 会在启动时被发现。

### 浏览器上传 — ChatGPT 与 Claude

1. [下载最新版 Skill ZIP][latest-zip]。
2. 在 ChatGPT 中打开 **Settings → Plugins → Browse plugins → Skills**，然后选择 **Upload from your computer**。也可以打开 <https://chatgpt.com/skills>。
3. 在 Claude 中打开 **Settings → Skills** 或 **Customize → Skills**，然后选择 **Create skill → Upload a skill**。
4. 选择 ZIP 并启用此 Skill。

![在 chatgpt.com 上传 Seedance Prompt Forge](docs/chatgpt-com-upload-skill.png)

### 手动备用方式

可分发包位于 `skills/seedance-prompt-forge/`：

```bash
git clone https://github.com/silentbuilds/seedance-prompt-forge
cp -R seedance-prompt-forge/skills/seedance-prompt-forge \
  ~/.claude/skills/
```

按所用 Agent 替换目标目录：

| Agent | 个人目录 | 项目目录 |
|---|---|---|
| Claude Code / Cowork | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` |
| Cursor | — | `.cursor/skills/` |
| GitHub Copilot | — | `.github/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| Cline、Amp、OpenCode、Warp、Antigravity | — | `.agents/skills/` |

安装到多个已检测 Agent 或指定项目：

```bash
./scripts/install.sh
./scripts/install.sh claude codex
./scripts/install.sh --project /path/to/your-project
./scripts/install.sh --list
```

备用安装器拒绝覆盖现有安装。添加 `--force` 会先创建带时间戳的备份，再替换：

```bash
./scripts/install.sh --force --project /path/to/your-project
```

## 使用方式

自然提出请求即可——Skill 会选择撰写、审计或诊断路线：

```text
Use Seedance Prompt Forge to turn this idea and my three references into a copy-ready prompt.

Audit this Seedance prompt before I generate it.

These two characters swapped faces and the prop duplicated. Diagnose the failure and repair
only what caused it.
```

## 确定性提示词检查

可选 Python linter 会发现可机械验证的问题：

- 被引用但从未分配角色的参考素材；
- 参考编号缺口或集合式映射；
- 未填充的 `<placeholders>`；
- 倒序、重叠或无效的时间范围；
- 每秒频率要求；
- 写在提示词中或为锁定任务请求的参数；
- 未含排除项或 `only …` 范围的场景参考；
- 缺少目标数量或时间线继承的替换编辑；
- 不平衡的对话/字幕标记；以及
- 未声明语言的非中文对话。

```bash
python3 skills/seedance-prompt-forge/scripts/lint_prompt.py \
  my-prompt.txt --task edit
```

该 linter 没有第三方依赖，支持 Python 3.8+。

## 质量与来源

```bash
python3 scripts/run_tests.py
python3 scripts/run_tests.py --guide /path/to/authorized-guide-export.md
```

已提交的测试套件为每项公开的 lint 规则提供正向和负向覆盖。提供经授权的指南导出后，回归运行器会检查 linter 不拒绝指南中任何已填充的示例。

准确的指南版本、验证日期、平台边界，以及“已记录指导”“经测试实现”和“工作推断”的区分，记录在[来源溯源](SOURCES.md)中。

本仓库面向即梦 Dreamina Seedance 2.5。在把模板用于其他 Seedance 版本、提供商、产品界面或 API 前，请先验证行为。

生成结果因输入素材、任务复杂度、设置和随机性而异。

## 更多示例

- [多阶段角色一致性](docs/examples/seedance-character-consistency.md)
- [多模态参考绑定与排除](docs/examples/seedance-multimodal-reference-prompt.md)
- [修复身份漂移、重复或分裂](docs/examples/fix-identity-drift-and-duplication.md)

## 贡献

修改 Skill 指导或 linter 规则前请阅读 `AGENTS.md`。每当运行时 Skill 发生变化，都必须重新生成 `dist/` 中的文件。

## 独立项目

Seedance Prompt Forge 是独立的非官方项目。它与 ByteDance、BytePlus 或 Dreamina 没有关联，也未获得其授权或认可。Seedance 和 Dreamina 是各自权利人的商标。

采用 MIT 许可证——参见 [LICENSE](LICENSE)。

[latest-zip]: https://github.com/silentbuilds/seedance-prompt-forge/releases/latest/download/seedance-prompt-forge.zip
