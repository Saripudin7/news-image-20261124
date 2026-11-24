#!/usr/bin/env python3
"""Render entry.png: one-day world news infographic for 24 Nov 2026.

Draws a 1024x1024 infographic with PIL only. All text and shapes are
drawn fresh in this script; no external images are used.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

F_TITLE = font("DejaVuSans-Bold.ttf", 54)
F_SUB = font("DejaVuSans.ttf", 24)
F_KICK = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 21)
F_DATE = font("DejaVuSans-Bold.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 17)

NAVY = (13, 34, 64)
NAVY2 = (24, 58, 102)
INK = (22, 28, 36)
MUTED = (90, 98, 110)
PAPER = (247, 245, 239)
CARD = (255, 255, 255)
GOLD = (212, 160, 32)
LINE = (214, 210, 198)

# (kicker, accent, headline, body, date tag, icon key)
STORIES = [
    ("ASIA  ·  MARKETS", (16, 122, 62),
     "Asian stocks surge on Nvidia's AI rally",
     "Nikkei +4.5%, Kospi +7.5%, Taiwan +9.1% on Tuesday after Nvidia jumped 31.5% on Huang's return as CEO.",
     "24 Nov 2026", "chart"),
    ("LIBYA  ·  WAR AT SEA", (150, 40, 40),
     "Ukraine 'sinks' Russian warship off Libya",
     "Seven sea drones hit the corvette Merkury in Benghazi, Kyiv says; cargo ship MV Angara was also struck.",
     "Attack 22 Nov, reported 23 Nov", "ship"),
    ("TURKEY  ·  CLIMATE", (18, 110, 110),
     "COP31 climate talks collapse with no deal",
     "UN talks in Antalya ended after governments rejected a draft deal with no mention of fossil fuels.",
     "23 Nov 2026", "globe"),
    ("ENGLAND  ·  SAFETY", (120, 70, 150),
     "12,000 evacuated from Manchester concert",
     "Fans left the Don Toliver show at Co-op Live after an unknown substance was released into the crowd.",
     "22 Nov 2026", "note"),
    ("CHINA  ·  JUSTICE", (140, 90, 10),
     "China sentences leaker to death",
     "A state official was sentenced to death for passing state secrets to a foreign country, media reported.",
     "Reported 24 Nov 2026", "scales"),
    ("SPORT  ·  FOOTBALL", (20, 80, 160),
     "CAS rules on Senegal's Africa Cup title",
     "Sport's top court decides on Tuesday whether Senegal keeps its Africa Cup of Nations title.",
     "24 Nov 2026", "ball"),
]


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, key, cx, cy, r, color):
    """Simple geometric icon inside a circle of radius r at (cx, cy)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(238, 240, 244),
              outline=color, width=3)
    if key == "chart":
        base = cy + r * 0.45
        bars = [(-0.5, 0.35), (-0.17, 0.6), (0.17, 0.8), (0.5, 1.0)]
        for bx, bh in bars:
            x0 = cx + bx * r - 7
            d.rectangle([x0, base - bh * r, x0 + 14, base], fill=color)
        d.line([(cx - r * 0.7, base - r * 0.95), (cx + r * 0.7, base - r * 0.15)],
               fill=color, width=5)
    elif key == "ship":
        d.polygon([(cx - r * 0.7, cy + r * 0.1), (cx + r * 0.7, cy + r * 0.1),
                   (cx + r * 0.45, cy + r * 0.5), (cx - r * 0.45, cy + r * 0.5)],
                  fill=color)
        d.rectangle([cx - 3, cy - r * 0.55, cx + 3, cy + r * 0.1], fill=color)
        d.polygon([(cx + 3, cy - r * 0.55), (cx + r * 0.45, cy - r * 0.25),
                   (cx + 3, cy - r * 0.25)], fill=color)
        for i, wx in enumerate([-0.7, -0.2, 0.3, 0.7]):
            d.arc([cx + wx * r - 14, cy + r * 0.55, cx + wx * r + 14,
                   cy + r * 0.85], 0, 180, fill=color, width=3)
    elif key == "globe":
        d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
                  outline=color, width=4)
        d.ellipse([cx - r * 0.2, cy - r * 0.55, cx + r * 0.2, cy + r * 0.55],
                  outline=color, width=3)
        d.line([(cx - r * 0.55, cy), (cx + r * 0.55, cy)], fill=color, width=3)
        d.arc([cx - r * 0.55, cy - r * 0.3, cx + r * 0.55, cy + r * 0.3],
              180, 360, fill=color, width=3)
    elif key == "note":
        d.ellipse([cx - r * 0.35, cy + r * 0.15, cx - r * 0.05, cy + r * 0.45],
                  fill=color)
        d.rectangle([cx - r * 0.08, cy - r * 0.55, cx - r * 0.02, cy + r * 0.3],
                    fill=color)
        d.line([(cx - r * 0.05, cy - r * 0.55), (cx + r * 0.5, cy - r * 0.35)],
               fill=color, width=5)
        d.line([(cx + r * 0.5, cy - r * 0.35), (cx + r * 0.5, cy + r * 0.1)],
               fill=color, width=5)
    elif key == "scales":
        d.line([(cx, cy - r * 0.6), (cx, cy + r * 0.55)], fill=color, width=4)
        d.line([(cx - r * 0.6, cy - r * 0.4), (cx + r * 0.6, cy - r * 0.4)],
               fill=color, width=4)
        d.polygon([(cx - r * 0.6, cy - r * 0.4), (cx - r * 0.85, cy + r * 0.1),
                   (cx - r * 0.35, cy + r * 0.1)], outline=color, width=3)
        d.polygon([(cx + r * 0.6, cy - r * 0.4), (cx + r * 0.85, cy + r * 0.1),
                   (cx + r * 0.35, cy + r * 0.1)], outline=color, width=3)
        d.ellipse([cx - 6, cy - r * 0.72, cx + 6, cy - r * 0.55], fill=color)
    elif key == "ball":
        d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
                  outline=color, width=4)
        pts = []
        for i in range(5):
            import math
            a = -math.pi / 2 + i * 2 * math.pi / 5
            pts.append((cx + r * 0.28 * math.cos(a), cy + r * 0.28 * math.sin(a)))
        d.polygon(pts, fill=color)
        for (px, py) in pts:
            d.line([(px, py), (cx + (px - cx) * 1.9, cy + (py - cy) * 1.9)],
                   fill=color, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 158], fill=NAVY)
    d.rectangle([0, 158, W, 164], fill=GOLD)
    d.text((32, 22), "THE WORLD IN ONE DAY", font=F_KICK, fill=(212, 190, 120))
    d.text((32, 48), "Tuesday 24 November 2026", font=F_TITLE, fill=(255, 255, 255))
    d.text((32, 116), "Six stories from around the world \u2014 as reported on Tuesday 24 November 2026",
           font=F_SUB, fill=(200, 212, 228))

    # ---- grid of 6 panels ----
    mx, my, gap = 24, 180, 16
    pw = (W - 2 * mx - gap) // 2
    ph = 248
    for i, (kicker, accent, head, body, date, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = mx + col * (pw + gap)
        y0 = my + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD,
                            outline=LINE, width=2)
        d.rounded_rectangle([x0, y0, x1, y0 + 8], radius=4, fill=accent)
        # icon
        icx, icy, ir = x0 + 52, y0 + 56, 36
        draw_icon(d, icon, icx, icy, ir, accent)
        # kicker + headline
        tx = x0 + 104
        d.text((tx, y0 + 20), kicker, font=F_KICK, fill=accent)
        head_lines = wrap(d, head, F_HEAD, pw - 120)
        hy = y0 + 46
        for ln in head_lines[:2]:
            d.text((tx, hy), ln, font=F_HEAD, fill=INK)
            hy += 32
        # body (wrapped to the panel width)
        by = y0 + 122
        for ln in wrap(d, body, F_BODY, pw - 48)[:3]:
            d.text((x0 + 24, by), ln, font=F_BODY, fill=(52, 60, 72))
            by += 27
        # date tag
        d.text((x0 + 24, y1 - 30), date, font=F_DATE, fill=MUTED)

    # ---- footer ----
    fy = my + 3 * ph + 2 * gap + 12
    d.text((32, fy), "Sources: Reuters, Associated Press, CNN, The Times of India \u2014 24 Nov 2026",
           font=F_FOOT, fill=MUTED)
    d.text((32, fy + 24), "Each panel shows the date its event happened or was first reported.",
           font=F_FOOT, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
