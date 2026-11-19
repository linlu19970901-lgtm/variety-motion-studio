# Variety Motion Studio v0.1.0

**面向剪映新手的原创综艺花字与视频包装设计 Skill。**

聚焦三件事：有创意的花字文案、统一的专业美术设计，以及能被剪映直接使用的透明 PNG 素材。

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
