#!/usr/bin/env python3
"""Generate original transparent Chinese variety-show caption PNGs for Jianying."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PRESETS = {
    "comic": {"ink": "#292438", "main": "#FFCB63", "accent": "#F47B94", "description": "喜剧反差"},
    "organic": {"ink": "#446454", "main": "#EEF0CF", "accent": "#D68E68", "description": "自然手作"},
    "editorial": {"ink": "#202C43", "main": "#F4D16C", "accent": "#8DB2BC", "description": "观点字体"}
}
FONT_PATHS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/msyh.ttc"
]

def load_font(size, custom=None):
    for path in ([custom] if custom else []) + FONT_PATHS:
        if path and Path(path).exists():
            try:
                return ImageFont.truetype(str(path), size)
            except OSError:
                pass
    raise SystemExit("没有检测到中文字体：请安装 Noto Sans CJK 或传入 --font 路径")

def wrap_lines(text, font, max_width, draw):
    result = []
    for paragraph in text.split("\n"):
        line = ""
        for ch in paragraph:
            candidate = line + ch
            bounds = draw.textbbox((0, 0), candidate, font=font, stroke_width=0)
            if line and bounds[2] - bounds[0] > max_width:
                result.append(line)
                line = ch
            else:
                line = candidate
        result.append(line)
    return result

def make(text, preset, out, size, custom_font=None):
    width, height = size
    colors = PRESETS[preset]
    im = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font_size = max(26, int(min(width / 10, height / 6)))
    font = load_font(font_size, custom_font)
    max_width = int(width * 0.8)
    lines = wrap_lines(text, font, max_width, d)
    while (len(lines) > 3 or len(lines) * font_size * 1.28 > height * 0.58) and font_size > 26:
        font_size -= 4
        font = load_font(font_size, custom_font)
        lines = wrap_lines(text, font, max_width, d)
    line_height = int(font_size * 1.28)
    top = int((height - len(lines) * line_height) / 2)
    base_stroke = max(3, font_size // 14)
    for i, line in enumerate(lines):
        bounds = d.textbbox((0, 0), line, font=font, stroke_width=0)
        text_width = bounds[2] - bounds[0]
        x = int((width - text_width) / 2)
        y = top + i * line_height
        if preset == "comic":
            d.rounded_rectangle((x - 22, y - 12, x + text_width + 22, y + font_size + 24), radius=22, fill=colors["accent"])
            d.text((x, y), line, font=font, fill=colors["main"], stroke_width=base_stroke + 2, stroke_fill=colors["ink"])
        elif preset == "organic":
            d.rounded_rectangle((x - 30, y - 20, x + text_width + 30, y + font_size + 18), radius=26, fill=colors["main"])
            d.text((x, y), line, font=font, fill=colors["ink"], stroke_width=1, stroke_fill=colors["ink"])
            d.ellipse((x - 28, y - 14, x - 8, y + 6), fill=colors["accent"])
        else:
            d.rounded_rectangle((x - 24, y - 8, x + text_width + 24, y + font_size + 18), radius=9, fill=colors["ink"])
            d.text((x, y), line, font=font, fill=colors["main"])
            d.rectangle((x, y + font_size + 10, x + min(text_width, 160), y + font_size + 17), fill=colors["accent"])
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    manifest = {
        "text": text,
        "preset": preset,
        "canvas": {"width": width, "height": height},
        "transparent": True,
        "format": "PNG",
        "usage": "剪映中导入 PNG，拖放到主视频上层轨道；调整位置和持续时间。"
    }
    out.with_suffix(".json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Created:", out, "and", out.with_suffix(".json"))

def main():
    p = argparse.ArgumentParser(description="原创综艺花字 PNG 生成工具")
    p.add_argument("--text", default="")
    p.add_argument("--preset", choices=list(PRESETS), default="comic")
    p.add_argument("--out", default="outputs/caption.png")
    p.add_argument("--size", default="1600x900", help="e.g. 1080x1920")
    p.add_argument("--font", default=None)
    p.add_argument("--list-presets", action="store_true")
    args = p.parse_args()
    if args.list_presets:
        for name, cfg in PRESETS.items():
            print(name, cfg["description"])
        return
    if not args.text.strip():
        p.error("请指定 --text")
    try:
        size = tuple(map(int, args.size.lower().split("x")))
        if len(size) != 2 or min(size) <= 0:
            raise ValueError()
    except ValueError:
        p.error("--size 格式应为宽x高，例如 1600x900")
    make(args.text, args.preset, args.out, size, args.font)

if __name__ == "__main__":
    main()
