#!/usr/bin/env python3
"""Render the front page for 20 November 2026 as a 1024x1024 PNG.

Run: python3 render.py  ->  writes entry.png next to this file.
Only Pillow + DejaVu/Liberation fonts on this machine are used; the
submitted entry itself (main.py) is stdlib-only and just copies entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (179, 32, 44)
BLUE = (29, 78, 137)
GOLD = (176, 132, 52)
GREY = (90, 86, 78)
LIGHT = (232, 226, 212)
NAVY_BG = (24, 42, 68)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill=INK, leading=None, spacing=0):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading + spacing
    return y


def centre(draw, y, text, fnt, fill=INK, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.3)


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 30                      # margin
CW = W - 2 * M              # content width

# ---- top dateline bar ----
small = font(SANS_B, 17)
d.text((M, 22), "FRIDAY", font=small, fill=RED)
centre(d, 22, "ONE DAY  ·  ONE IMAGE  ·  THE WHOLE WORLD", small, GREY)
w = d.textlength("No. 324", font=small)
d.text((W - M - w, 22), "No. 324", font=small, fill=GREY)
rule(d, M, W - M, 48, INK, 2)

# ---- masthead ----
y = 56
mast = font(SERIF_B, 64)
while d.textlength("THE WORLD IN ONE DAY", font=mast) > 940:
    mast = font(SERIF_B, mast.size - 2)
centre(d, y, "THE WORLD IN ONE DAY", mast, INK)
y = 56 + int(mast.size * 1.28)
centre(d, y, "Friday, 20 November 2026", font(SERIF, 26), RED)
y += 40
rule(d, M, W - M, y, INK, 4)
rule(d, M, W - M, y + 6, INK, 1)
y += 16

# ---- lead story ----
kick = font(SANS_B, 19)
d.text((M, y), "SHENZHEN  ·  THE SUMMIT AFTERMATH", font=kick, fill=RED)
y += 30
head = font(SERIF_B, 46)
y = text_block(d, M, y, "Peace on paper, missiles by night", head, 620, INK, leading=52)
y += 4
deck = font(SERIF, 21)
y = text_block(d, M, y,
               "Trump, Xi and Putin sign a joint \u201cpeace declaration\u201d "
               "in Shenzhen \u2014 no deal on Ukraine, Iran or nuclear arms. "
               "Hours later, Russia fires its biggest missile attack of "
               "the year at Kyiv: 110 missiles, nine killed.", deck, 620, INK, leading=27)

# globe illustration, right of the lead
gx, gy, gr = 790, 262, 88
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=NAVY_BG, width=4, fill=(214, 228, 240))
for rx in (32, 60, 84):
    d.ellipse([gx - rx, gy - gr, gx + rx, gy + gr], outline=NAVY_BG, width=2)
d.line([(gx - gr, gy), (gx + gr, gy)], fill=NAVY_BG, width=2)
d.line([(gx, gy - gr), (gx, gy + gr)], fill=NAVY_BG, width=2)
for (dx, dy, col) in [(-36, -28, RED), (40, -16, GOLD), (28, 42, BLUE)]:
    d.ellipse([gx + dx - 9, gy + dy - 9, gx + dx + 9, gy + dy + 9], fill=col)
d.text((gx - 62, gy + gr + 10), "Three nuclear powers,",
       font=font(SANS, 17), fill=GREY)
d.text((gx - 62, gy + gr + 32), "one declaration.",
       font=font(SANS, 17), fill=GREY)
lx = gx - 62
for (col, lab) in [(RED, "US"), (GOLD, "China"), (BLUE, "Russia")]:
    d.ellipse([lx, gy + gr + 58, lx + 12, gy + gr + 70], fill=col)
    d.text((lx + 17, gy + gr + 56), lab, font=font(SANS_B, 15), fill=INK)
    lx += 17 + d.textlength(lab, font=font(SANS_B, 15)) + 16

y = 448
rule(d, M, W - M, y, INK, 2)

# ---- story grid: 2 columns x 3 rows ----
stories = [
    ("KYIV", RED, "110 missiles over Kyiv",
     "Nine killed as Russia\u2019s overnight barrage hits the capital "
     "hours after the Shenzhen summit; debris sets a block of flats ablaze."),
    ("POLAND", RED, "Missiles come down in Poland",
     "Warsaw calls it a deliberate provocation; NATO calls the "
     "airspace breach grave."),
    ("THE HAGUE", BLUE, "Myanmar guilty of genocide",
     "The world court rules 9\u20136 that Myanmar\u2019s forces committed "
     "genocide against the Rohingya."),
    ("MARKETS", GOLD, "Stocks slide into correction",
     "The S&P 500 falls 3.7% and the Nikkei 5.06% as the AI "
     "sell-off spreads worldwide."),
    ("RIYADH", RED, "Missile hits Riyadh tower",
     "Houthis strike the PIF Tower; a tanker burns in the "
     "Strait of Hormuz."),
    ("BRUSSELS", BLUE, "EU and UK strike new deals",
     "Food trade, carbon markets and youth mobility agreed; "
     "Merz rejects a new Yalta over Europe."),
]
col_w = (CW - 24) // 2
row_h = 136
gy0 = y + 12
for i, (kicker, colour, headline, deck_text) in enumerate(stories):
    col, row = i % 2, i // 2
    x = M + col * (col_w + 24)
    yy = gy0 + row * row_h
    d.text((x, yy), kicker, font=font(SANS_B, 16), fill=colour)
    yy += 24
    yy = text_block(d, x, yy, headline, font(SERIF_B, 25), col_w, INK, leading=30)
    yy += 2
    text_block(d, x, yy, deck_text, font(SERIF, 18), col_w, INK, leading=23)
    if col == 0:
        d.line([(x + col_w + 12, gy0 + row * row_h + 4),
                (x + col_w + 12, gy0 + (row + 1) * row_h - 12)], fill=LIGHT, width=1)

y = gy0 + 3 * row_h + 4
rule(d, M, W - M, y, INK, 2)
y += 10

# ---- also today strip ----
d.text((M, y), "ALSO TODAY", font=font(SANS_B, 17), fill=RED)
y += 26
y = text_block(d, M, y,
               "Cyclone Akvan makes landfall on India\u2019s east coast  ·  "
               "BepiColombo reaches Mercury after eight years  ·  "
               "US loses measles elimination status  ·  "
               "Magnitude 6.7 quake hits central Peru",
               font(SERIF, 20), CW, INK, leading=26)
y += 8
rule(d, M, W - M, y, INK, 4)
y += 10
centre(d, y, "THE WORLD IN ONE DAY  ·  20 NOVEMBER 2026  ·  Sources: Reuters, CNN, Dawn, The Times",
       font(SANS, 15), GREY)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes", img.size)
