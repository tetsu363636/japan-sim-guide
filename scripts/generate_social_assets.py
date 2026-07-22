#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "social-card.png"
WIDTH = 1200
HEIGHT = 630


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def vertical_gradient(width: int, height: int, start: tuple[int, int, int], end: tuple[int, int, int]) -> Image.Image:
    image = Image.new("RGB", (width, height), start)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        ratio = y / max(height - 1, 1)
        color = tuple(int(start[i] + (end[i] - start[i]) * ratio) for i in range(3))
        draw.line((0, y, width, y), fill=color)
    return image


def draw_badge(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str, ink: str, font: ImageFont.ImageFont) -> None:
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0] + 34
    height = bbox[3] - bbox[1] + 20
    draw.rounded_rectangle((x, y, x + width, y + height), radius=height // 2, fill=fill)
    draw.text((x + 17, y + 10), text, fill=ink, font=font)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    canvas = vertical_gradient(WIDTH, HEIGHT, (244, 243, 240), (219, 236, 255))
    draw = ImageDraw.Draw(canvas)

    blue = "#2a78d6"
    blue_dark = "#1c5cab"
    blue_light = "#cde2fb"
    surface = "#fcfcfb"
    ink = "#0b0b0b"
    secondary = "#52514e"
    green_bg = "#d4f0d4"
    green = "#006300"
    warn_bg = "#fef3cd"
    warn = "#7a4f00"

    title_font = load_font(56, bold=True)
    sub_font = load_font(28)
    brand_font = load_font(26, bold=True)
    badge_font = load_font(22, bold=True)
    stat_label = load_font(28)
    stat_value = load_font(58, bold=True)
    small_font = load_font(22, bold=True)
    card_font = load_font(30, bold=True)

    draw.rounded_rectangle((64, 64, 788, 566), radius=28, fill=surface, outline="#d7d7d1", width=2)
    draw.rounded_rectangle((820, 64, 1136, 566), radius=28, fill=blue)

    draw.text((108, 102), "JapanSIMGuide", fill=blue, font=brand_font)
    draw.text((108, 176), "Best SIM Card for", fill=ink, font=title_font)
    draw.text((108, 244), "Foreigners in Japan", fill=ink, font=title_font)
    draw.text((108, 326), "Rakuten vs docomo, au, and SoftBank", fill=secondary, font=sub_font)

    draw_badge(draw, (108, 386), "11 languages", blue_light, blue_dark, badge_font)
    draw_badge(draw, (340, 386), "eSIM ready", green_bg, green, badge_font)
    draw_badge(draw, (548, 386), "No JP card needed", warn_bg, warn, badge_font)

    draw.rounded_rectangle((108, 462, 712, 540), radius=22, fill="#eef5ff")
    draw.text((142, 494), "Calculator + checklist + disclosure", fill=blue_dark, font=card_font)

    draw.text((858, 102), "Updated Jul 2026", fill="white", font=small_font)
    draw.text((858, 224), "Save up to", fill="white", font=stat_label)
    draw.text((858, 280), "JPY 230k", fill="white", font=load_font(54, bold=True))
    draw.text((858, 334), "per year for a family", fill="#d9eaff", font=load_font(23))
    draw.text((858, 364), "switching carriers", fill="#d9eaff", font=load_font(23))

    draw.rounded_rectangle((858, 412, 1098, 522), radius=22, fill=(255, 255, 255, 38), outline=(255, 255, 255, 90), width=1)
    draw.text((892, 438), "Built for:", fill=blue_dark, font=small_font)
    draw.text((892, 472), "expats", fill=blue_dark, font=load_font(20))
    draw.text((966, 472), "students", fill=blue_dark, font=load_font(20))
    draw.text((892, 500), "new residents", fill=blue_dark, font=load_font(20))

    canvas.save(OUTPUT, format="PNG", optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
