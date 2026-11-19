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
