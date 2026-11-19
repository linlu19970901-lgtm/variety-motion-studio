---
name: variety-motion-studio
description: 为中文综艺、访谈、活动短视频设计原创高审美花字、笑点文案、趣味贴片与剪映可用素材。先理解内容和创意提案，再做静态美术、动效规划和剪映交付。适用于用户要求综艺花字、视频包装、趣味字幕、后期包装、剪映贴片、综艺感短视频时。
license: MIT
metadata:
  version: 0.1.0
  language: zh-CN
---

# Variety Motion Studio — 综艺视觉创意与剪映交付 Skill

## 核心原则
不是给所有台词加粗描边字，而是像专业综艺后期美术团队一样：理解笑点 → 发现视觉隐喻 → 提案 → 设计静态关键帧 → 审稿 → 制定动效 → 剪映交付。**静态设计不够好看，不进入动态制作。**

## 任务路由
- 只有台词：构思 3 个创意机制不同的方案（不是简单换字体和颜色）。每个包含后期文案、视觉隐喻、字形、构图、配色、插画、出入场动效与音效。
- 有视频：先观察台词、人物反应、空间和不可遮挡区域；没有实际分析画面就不能声称拥有准确时间码或表情识别。
- 有参考节目：从研究库提取设计原则，创作原创视觉，不照搬商标、现有花字、人物形象或节目素材。
- 明确用于剪映：默认优先透明 PNG + 使用说明；动画格式须按用户剪映版本验证。

## 专业工作流
1. 阅读 `references/visual-bible.md` 确定节目气质、字体系统、色彩、材质与图形母题。
2. 阅读 `references/creative-director.md` 分析喜剧机制、人物关系及后期文案人格。
3. 阅读 `references/chinese-casebook.md` 并参考确切来源。旧季案例不得冒充新季。
4. 每个重要笑点设计三套创意机制不同的美术方案；说明各自为什么有趣、为什么适合画面。
5. 优先生成静态关键帧并按 `references/quality-gate.md` 进行美术审查。文字可读、构图美观、场景融合、文案有价值。
6. 通过审核后设计动画入场、停留、退场、声音和出现时机；保证不提前剧透包袱。
7. 向剪映小白交付透明 PNG、配置 JSON、预览和具体导入方法；参考 `references/jianying-beginner.md`。
8. 如果不具备视频渲染工具，明确说明只输出静态素材或动效脚本，不声称已生成视频。

## 可运行的静态花字脚本
需要 Python 3.9+、Pillow 及系统中文字体：

```bash
pip install -r requirements.txt
python scripts/make_caption.py --list-presets
python scripts/make_caption.py --text "事情开始不对劲了" --preset comic --out outputs/huazi.png
python scripts/make_caption.py --text "今天也要慢慢来" --preset organic --out outputs/organic.png
python scripts/make_caption.py --text "压力山大" --preset editorial --out outputs/editorial.png
```

三个原创静态样式：comic（喜剧反差）、organic（手作自然）、editorial（观点强调）。可使用 --size 1080x1920 生成竖屏素材，使用 --font 指定本机字体。生成透明 PNG 和同名 JSON。

## 交付规则
- 对剪映新手优先无背景 PNG；放在视频轨道上方，直接调整位置、尺寸和时长。
- 动效素材未来可以提供经目标剪映版本测试的 Alpha 视频和绿幕 MP4；不可假设透明 MOV 在所有剪映版本都兼容。
- 关键表情、手势、原字幕和重要场景信息属于安全区，不能遮挡。
- 参考节目案例必须记录来源、季度与验证状态，不伪造逐帧分析。

## 版本边界
V0.1.0 实现原创静态花字渲染、可复用设计 JSON、创意工作流、案例来源索引及剪映教程；不包含自动视频理解、人物跟踪、动态视频渲染、剪映草稿写入或 30 款成品模板。
后续路线见 `ROADMAP.md`。
