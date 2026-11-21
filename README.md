# Variety Motion Studio v0.6.0

**面向剪映新手的原创综艺花字与视频包装设计 Skill。**

聚焦三件事：有创意的花字文案、统一的专业美术设计，以及能被剪映直接使用的透明 PNG 素材。

## v0.6 真人动态表情包与肖像贴纸（新增）
新增 [真人肖像动态贴纸工作流](references/realistic-portrait-sticker-motion.md)，面向参考照片制作 **身份一致、头部 die-cut 抠图、统一白边浅投影、三段情绪转折、真实透明 GIF/APNG/剪映分层动画**。规范覆盖分镜节拍、眉眼嘴微表情、头部锚点、蓝色发愁符号与黄色灯泡等贴纸特效、帧间一致性及 Alpha 检查。强调只有透明精灵表时不能宣称已有 GIF。工作流属于制作规范，尚未内置人像生成/重演 API。

## v0.5 剪映原生动效优先
更新核心工作流：**AI 生图设计原创贴片 + 剪映原生关键帧实现基础运动 + 复杂动效才预渲染**。相比把所有成品导出 GIF，这种方式能显著降低对视频透明编码的依赖，也更便于新手调整。

- [剪映能力与五类综艺制作配方](references/jianying-native-first.md)
- [关键帧时间线 JSON 示例](templates/jianying-recipe.example.json)

默认三档：Level 1 一张透明 PNG + 入场动画；Level 2 分层 PNG + 关键帧（推荐）；Level 3 复杂逐帧动画 + 兼容性兜底。已验证的是**规范、配方文件在仓库中存在**，尚未实测特定用户剪映客户端的全部菜单或导入格式，也尚未实现自动写入剪映原生草稿。

## v0.4 — 透明动态贴片：目前主设计路线

经过实际视觉测试，**整屏海报式花字虽然热闹，却不适合叠加到综艺正片**。用户认可的是紧凑、独立、透明底、有语义动作变化的动效贴片。当前的最高优先级文档是：[透明动态贴片设计与交付规范](references/transparent-motion-stickers.md)。

新增分帧导出脚本，将**真正带 RGBA alpha** 的等尺寸精灵表转为 APNG 和 GIF；可选生成 VP9-alpha WebM。此脚本不生成原创美术图，需由宿主生图工具先生成素材：

```bash
python scripts/export_animated_overlay.py spritesheet.png --rows 2 --columns 3 --frames 6 --duration-ms 180 --out outputs/animated-sticker
```

注意：GIF 透明度和边缘表现有限；剪映/CapCut 的版本对 GIF、APNG、WebM 兼容性可能不同。没有经过目标环境实测的格式不得声称能直接导入；最可靠的兜底方案仍是 PNG 分帧或静态透明 PNG + 剪映内置动画。本仓库目前尚无自动生成全部设计并一键成片的服务。

## 当前可用功能
- Agent Skill 工作流：理解台词 → 三案创意 → 美术审核 → 剪映交付
- 三种原创静态花字预设：`comic`、`organic`、`editorial`
- Python + Pillow 生成透明 PNG 和对应 JSON 描述
- 横屏、竖屏可调；支持本地中文字体
- 综艺案例来源索引、剪映小白操作手册、质量检查规则

## 快速开始
需要 Python 3.9+、Pillow 及中文字体。

```bash
pip install -r requirements.txt
python scripts/make_caption.py --list-presets
python scripts/make_caption.py --text "事情开始不对劲了" --preset comic --out outputs/huazi.png
python scripts/make_caption.py --text "今天也要慢慢来" --preset organic --out outputs/organic.png
python scripts/make_caption.py --text "压力山大" --preset editorial --size 1080x1920 --out outputs/editorial.png
```

生成的透明 PNG 可直接叠放在剪映视频的上层轨道。详见 [剪映新手指南](references/jianying-beginner.md)。

## 作为 Skill 使用
将此仓库克隆到支持自定义 Agent Skills 的工具的 Skills 目录，让 Agent 读取根目录的 `SKILL.md`。不同产品的 Skills 安装路径不同；普通 ChatGPT 聊天界面不保证能直接安装 GitHub 仓库。

## 参考研究
- [视觉世界观](references/visual-bible.md)
- [创意导演规则](references/creative-director.md)
- [中国综艺研究索引](references/chinese-casebook.md)
- [质量关卡](references/quality-gate.md)
- [剪映新手教程](references/jianying-beginner.md)

## 当前边界
v0.1.0 为**可运行的静态花字工具和 Agent 工作流初版**，不具备自动分析原视频、自动制作动态透明视频、追踪人物和自动写入剪映草稿的完整能力。这些属于 [路线图](ROADMAP.md)。

所有节目名及公开案例仅供分析设计方法。未分发节目原片、受版权保护的截图或第三方代码。仓库原创代码和文档采用 MIT 许可。


## V0.2 艺术化花字升级（新）
新脚本不替代旧脚本，新增更明确的字体舞台与图形语言：喜剧爆点 / 自然手作 / 观点碰撞。输出透明 PNG + 同名可复用 JSON，支持副标题与自定义字体。它们是可工作的入门美术组件，不等于电视台级定制花字，也不是动态视频。

```bash
python scripts/art_caption.py --list-presets
python scripts/art_caption.py --text "这下玩大了！" --preset comic-punch --out outputs/comic.png
python scripts/art_caption.py --text "慢一点，也很好" --preset field-notes --out outputs/organic.png
python scripts/art_caption.py --text "我不服！" --subtitle "观点正在交锋" --preset type-clash --out outputs/editorial.png
```

设计原则：[原创美术策略](references/v02-art-direction.md)。已在本地以 Pillow 生成三张透明 PNG 原型，GitHub 中的脚本已提交，建议按 README 环境安装后在本机运行验证。

## 重要设计方向修订：AI 生图优先
此前 Python Pillow 预设产生了明显 PPT / 模板感，也不能依据台词独立创作。该路线不再作为主美术输出。新的 [生图美术工作流](references/imagegen-art-direction.md) 要求使用支持图像生成的 Agent/环境，先构思语义相关视觉隐喻，再用图像模型创作插画和字体美术；使用可编辑准确文字层校正中文，最后提供剪映透明 PNG 素材。当前仓库仅提供 Agent 工作流规范，**尚未接入自动调用图像生成 API**。原有 Python 脚本保留为基础排版测试工具，不作为专业成品示例。


## V0.3 新增：综艺剪辑语言与可运行视频执行器
新增 [综艺剪辑导演](references/editing-director.md) 和 [剪映零基础操作卡](references/jianying-shotbook.md)，将**铺垫→反转→反应→花字→音效**串成一条逻辑，而不只是单独做字卡。

安装 FFmpeg/ffprobe 和 Python Pillow 后，在仓库根目录执行：
```bash
python scripts/generate_test_media.py
python scripts/variety_edit.py examples/clip-plan.example.json --out outputs/variety_edit.mp4
python scripts/mix_sfx.py outputs/variety_edit.mp4 examples/sfx-plan.example.json --out outputs/with-sfx.mp4
```

现在可以按 JSON 时间码组合正常播放、变速、定格、重复回放、透明 PNG 叠加以及定点音效。测试媒体由 `generate_test_media.py` 生成，不上传节目版权素材。

**功能边界：** 需人工提供剪辑时间码，不能自动看懂表情和梗；AI 图像模型依赖宿主环境，还没有作为独立 API 服务集成；并未实现剪映工程文件写入。真实项目仍需专业审稿与素材授权。
