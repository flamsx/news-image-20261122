"""Drawing helpers for the 22 November 2026 front page.

Fresh code, written for this entry only. Uses PIL + the Lexend variable
font committed under fonts/ (Google Fonts, OFL).
"""
import math
from PIL import Image, ImageDraw, ImageFont

PAPER = (246, 241, 231)
INK = (25, 25, 25)
MUTED = (107, 100, 90)
RED = (180, 35, 24)
BLUE = (30, 78, 140)
TEAL = (15, 118, 110)
GOLD = (183, 121, 31)
CARD = (255, 255, 255)
BORDER = (216, 208, 190)
BAND = (239, 231, 214)
SKY = (214, 232, 240)
GREEN = (46, 125, 50)
ORANGE = (214, 110, 30)

_FONT_CACHE = {}


def font(size, weight=400):
    key = (size, weight)
    if key not in _FONT_CACHE:
        f = ImageFont.truetype("fonts/Lexend-Variable.ttf", size)
        f.set_variation_by_axes([weight])
        _FONT_CACHE[key] = f
    return _FONT_CACHE[key]


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, text, fnt, x, y, max_w, fill=INK, leading=None, max_lines=None):
    lines = wrap(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading if leading else int(fnt.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def trunc(d, text, fnt, max_w):
    """Truncate with ellipsis to fit max_w."""
    if d.textlength(text, font=fnt) <= max_w:
        return text
    while text and d.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


def rrect(d, box, fill=None, outline=None, width=1, radius=6):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def card_frame(d, box):
    rrect(d, box, fill=CARD, outline=BORDER, width=1, radius=5)


def label_band(d, x, y, w, text, color=RED):
    """Red label banner with white text, returns height used."""
    f = font(11, 700)
    tw = d.textlength(text, font=f)
    bw = min(w, tw + 14)
    d.rectangle([x, y, x + bw, y + 17], fill=color)
    d.text((x + 7, y + 2), text, font=f, fill=(255, 255, 255))
    return 17


def source_tag(d, x, y, text):
    f = font(10, 600)
    d.text((x, y), "SOURCE: " + text.upper(), font=f, fill=MUTED)


# ---------------------------------------------------------------- illustrations
# Each takes (d, x, y, w, h) and draws a simple flat pictogram in the box.

def ill_cop(d, x, y, w, h):
    # big sunrise over a summit skyline + leaf
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w * 0.30, y + h * 0.06, x + w * 0.70, y + h * 0.58], fill=(255, 196, 66))
    d.ellipse([x + w * 0.08, y + h * 0.16, x + w * 0.28, y + h * 0.30], fill=(255, 255, 255))
    d.ellipse([x + w * 0.72, y + h * 0.22, x + w * 0.92, y + h * 0.34], fill=(255, 255, 255))
    d.polygon([(x, y + h), (x + w * 0.16, y + h * 0.34), (x + w * 0.34, y + h)], fill=(90, 120, 90))
    d.polygon([(x + w * 0.28, y + h), (x + w * 0.52, y + h * 0.26), (x + w * 0.76, y + h)], fill=(70, 100, 70))
    d.polygon([(x + w * 0.60, y + h), (x + w * 0.80, y + h * 0.42), (x + w, y + h)], fill=(90, 120, 90))
    d.ellipse([x + w * 0.74, y + h * 0.58, x + w * 0.96, y + h * 0.96], fill=GREEN)
    d.arc([x + w * 0.74, y + h * 0.58, x + w * 0.96, y + h * 0.96], 200, 340, fill=(255, 255, 255), width=2)


def ill_g20(d, x, y, w, h):
    # African continent silhouette + rising sun
    d.rectangle([x, y, x + w, y + h], fill=(253, 230, 180))
    d.ellipse([x + w * 0.64, y + h * 0.06, x + w * 0.90, y + h * 0.40], fill=(255, 170, 60))
    africa = [(0.26, 0.16), (0.48, 0.12), (0.64, 0.20), (0.68, 0.30), (0.58, 0.38),
              (0.54, 0.56), (0.48, 0.82), (0.42, 0.86), (0.38, 0.62), (0.30, 0.46),
              (0.20, 0.34), (0.18, 0.22)]
    pts = [(x + px * w, y + py * h) for px, py in africa]
    d.polygon(pts, fill=(150, 90, 40))
    d.rectangle([x + w * 0.10, y + h * 0.78, x + w * 0.90, y + h * 0.86], fill=TEAL)


def ill_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 46))
    cx, cy, r = x + w * 0.5, y + h * 0.52, min(w, h) * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 147, 26))
    d.ellipse([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82], outline=(255, 255, 255), width=2)
    f = font(int(r * 0.95), 700)
    d.text((cx, cy - r * 0.42), "B", font=f, fill=(255, 255, 255), anchor="ma")
    d.polygon([(x + w * 0.08, y + h * 0.88), (x + w * 0.30, y + h * 0.62), (x + w * 0.52, y + h * 0.74),
               (x + w * 0.74, y + h * 0.44), (x + w * 0.94, y + h * 0.58)],
              fill=(46, 160, 90))


def ill_card(d, x, y, w, h):
    # credit card with a big 10%
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 245))
    d.rounded_rectangle([x + w * 0.12, y + h * 0.22, x + w * 0.88, y + h * 0.82], radius=8, fill=BLUE)
    d.rectangle([x + w * 0.12, y + h * 0.34, x + w * 0.88, y + h * 0.46], fill=(25, 25, 25))
    f = font(int(h * 0.34), 700)
    d.text((x + w * 0.5, y + h * 0.50), "10%", font=f, fill=(255, 255, 255), anchor="ma")


def ill_pentagon(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 228, 232))
    cx, cy, r = x + w * 0.5, y + h * 0.55, min(w, h) * 0.42
    pts = []
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.92))
    d.polygon(pts, fill=(90, 100, 112))
    d.polygon([(cx - r * 0.45, cy - r * 0.1), (cx + r * 0.45, cy - r * 0.1),
               (cx + r * 0.28, cy + r * 0.42), (cx - r * 0.28, cy + r * 0.42)], fill=(200, 205, 212))


def ill_vote(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 232, 250))
    d.rounded_rectangle([x + w * 0.22, y + h * 0.42, x + w * 0.78, y + h * 0.86], radius=4, fill=BLUE)
    d.rectangle([x + w * 0.42, y + h * 0.36, x + w * 0.58, y + h * 0.44], fill=(25, 25, 25))
    d.polygon([(x + w * 0.30, y + h * 0.34), (x + w * 0.46, y + h * 0.10), (x + w * 0.60, y + h * 0.16),
               (x + w * 0.74, y + h * 0.02), (x + w * 0.52, y + h * 0.38)],
              fill=(255, 255, 255), outline=INK)
    d.line([(x + w * 0.36, y + h * 0.62), (x + w * 0.46, y + h * 0.72), (x + w * 0.66, y + h * 0.52)],
           fill=(255, 255, 255), width=4)


def ill_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # plane silhouette
    d.ellipse([x + w * 0.20, y + h * 0.42, x + w * 0.80, y + h * 0.58], fill=(255, 255, 255))
    d.polygon([(x + w * 0.72, y + h * 0.44), (x + w * 0.95, y + h * 0.30), (x + w * 0.88, y + h * 0.52)], fill=(255, 255, 255))
    d.polygon([(x + w * 0.30, y + h * 0.56), (x + w * 0.45, y + h * 0.78), (x + w * 0.55, y + h * 0.56)], fill=(255, 255, 255))
    # no-entry ring
    cx, cy, r = x + w * 0.82, y + h * 0.24, min(w, h) * 0.20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=3)
    d.line([cx - r * 0.7, cy + r * 0.7, cx + r * 0.7, cy - r * 0.7], fill=RED, width=3)


def ill_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 236, 222))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(120, 170, 200))
    d.arc([x - w * 0.1, y + h * 0.18, x + w * 1.1, y + h * 1.05], 180, 360, fill=ORANGE, width=5)
    d.line([x, y + h * 0.62, x + w, y + h * 0.62], fill=INK, width=3)
    for fx in (0.2, 0.4, 0.6, 0.8):
        d.line([x + w * fx, y + h * 0.62, x + w * fx, y + h * 0.30], fill=INK, width=2)


def ill_race(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(25, 25, 35))
    # checkered flag
    for i in range(4):
        for j in range(2):
            if (i + j) % 2 == 0:
                d.rectangle([x + w * 0.10 + i * w * 0.09, y + h * 0.14 + j * h * 0.16,
                             x + w * 0.19 + i * w * 0.09, y + h * 0.30 + j * h * 0.16], fill=(255, 255, 255))
    d.line([x + w * 0.12, y + h * 0.14, x + w * 0.12, y + h * 0.86], fill=(255, 255, 255), width=3)
    # race car
    d.rounded_rectangle([x + w * 0.42, y + h * 0.58, x + w * 0.92, y + h * 0.76], radius=6, fill=RED)
    d.polygon([(x + w * 0.58, y + h * 0.58), (x + w * 0.66, y + h * 0.42), (x + w * 0.80, y + h * 0.42),
               (x + w * 0.86, y + h * 0.58)], fill=RED)
    d.ellipse([x + w * 0.48, y + h * 0.72, x + w * 0.58, y + h * 0.84], fill=(25, 25, 25))
    d.ellipse([x + w * 0.78, y + h * 0.72, x + w * 0.88, y + h * 0.84], fill=(25, 25, 25))


def ill_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 228, 228))
    d.rectangle([x + w * 0.10, y + h * 0.50, x + w * 0.90, y + h * 0.88], fill=(120, 120, 120))
    d.polygon([(x + w * 0.10, y + h * 0.50), (x + w * 0.25, y + h * 0.30), (x + w * 0.40, y + h * 0.50)],
              fill=(90, 90, 90))
    d.polygon([(x + w * 0.40, y + h * 0.50), (x + w * 0.55, y + h * 0.30), (x + w * 0.70, y + h * 0.50)],
              fill=(90, 90, 90))
    d.rectangle([x + w * 0.76, y + h * 0.22, x + w * 0.84, y + h * 0.88], fill=(90, 90, 90))
    d.ellipse([x + w * 0.72, y + h * 0.08, x + w * 0.88, y + h * 0.24], fill=(255, 255, 255))
    for wx in (0.16, 0.32, 0.48, 0.64):
        d.rectangle([x + w * wx, y + h * 0.60, x + w * (wx + 0.08), y + h * 0.74], fill=(255, 220, 100))


def ill_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 40, 60))
    cx, cy = x + w * 0.5, y + h * 0.5
    s = min(w, h) * 0.30
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=TEAL, outline=(255, 255, 255), width=2)
    d.rectangle([cx - s * 0.45, cy - s * 0.45, cx + s * 0.45, cy + s * 0.45], fill=(255, 220, 100))
    for dx in (-1, 0, 1):
        d.line([cx + dx * s * 0.6, cy - s, cx + dx * s * 0.6, cy - s * 1.35], fill=(255, 255, 255), width=2)
        d.line([cx + dx * s * 0.6, cy + s, cx + dx * s * 0.6, cy + s * 1.35], fill=(255, 255, 255), width=2)
        d.line([cx - s, cy + dx * s * 0.6, cx - s * 1.35, cy + dx * s * 0.6], fill=(255, 255, 255), width=2)
        d.line([cx + s, cy + dx * s * 0.6, cx + s * 1.35, cy + dx * s * 0.6], fill=(255, 255, 255), width=2)


def ill_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 238, 238))
    # two overlapping circles: island + maple leaf hint
    d.ellipse([x + w * 0.14, y + h * 0.20, x + w * 0.52, y + h * 0.80], fill=RED)
    d.ellipse([x + w * 0.48, y + h * 0.20, x + w * 0.86, y + h * 0.80], fill=(255, 255, 255), outline=RED, width=2)
    f = font(int(h * 0.30), 700)
    d.text((x + w * 0.33, y + h * 0.28), "TW", font=f, fill=(255, 255, 255), anchor="ma")
    d.text((x + w * 0.67, y + h * 0.28), "CA", font=f, fill=RED, anchor="ma")


def ill_megaphone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 235, 220))
    d.polygon([(x + w * 0.18, y + h * 0.45), (x + w * 0.72, y + h * 0.22), (x + w * 0.72, y + h * 0.78),
               (x + w * 0.18, y + h * 0.58)], fill=ORANGE)
    d.rectangle([x + w * 0.10, y + h * 0.42, x + w * 0.20, y + h * 0.62], fill=INK)
    for i, yy in enumerate((0.20, 0.38, 0.56)):
        d.arc([x + w * 0.74, y + h * yy, x + w * 0.92, y + h * (yy + 0.24)], -60, 60, fill=INK, width=2)
    for cx in (0.30, 0.50, 0.70):
        d.ellipse([x + w * cx, y + h * 0.86, x + w * (cx + 0.08), y + h * 0.96], fill=INK)


# ---------------------------------------------------------------- world map
def draw_map(d, x, y, w, h):
    """Rough equirectangular world map with numbered pins."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 235, 240))
    # continents as rough polygons in 0..1 space
    na = [(0.03, 0.10), (0.10, 0.04), (0.20, 0.06), (0.26, 0.14), (0.22, 0.26),
          (0.16, 0.34), (0.10, 0.30), (0.04, 0.20)]
    sa = [(0.24, 0.44), (0.30, 0.42), (0.34, 0.50), (0.31, 0.64), (0.27, 0.72), (0.24, 0.58)]
    eu = [(0.44, 0.08), (0.52, 0.06), (0.56, 0.12), (0.52, 0.20), (0.46, 0.18), (0.42, 0.12)]
    af = [(0.46, 0.28), (0.54, 0.26), (0.60, 0.32), (0.58, 0.48), (0.53, 0.62),
          (0.49, 0.58), (0.46, 0.44), (0.43, 0.34)]
    asia = [(0.56, 0.06), (0.70, 0.04), (0.86, 0.08), (0.94, 0.16), (0.88, 0.28),
            (0.78, 0.34), (0.70, 0.30), (0.64, 0.22), (0.58, 0.16)]
    au = [(0.80, 0.60), (0.88, 0.58), (0.93, 0.64), (0.88, 0.72), (0.81, 0.70)]
    for poly in (na, sa, eu, af, asia, au):
        pts = [(x + px * w, y + py * h) for px, py in poly]
        d.polygon(pts, fill=(190, 205, 170), outline=(120, 140, 110))
    d.line([x, y + h * 0.36, x + w, y + h * 0.36], fill=(255, 255, 255), width=1)
    return


def lonlat_to_xy(x, y, w, h, lon, lat):
    # equirectangular: lon -180..180 -> 0..w ; lat 85..-60 -> 0..h
    px = x + (lon + 180.0) / 360.0 * w
    py = y + (85.0 - lat) / 145.0 * h
    return px, py


def pin(d, x, y, w, h, lon, lat, num):
    px, py = lonlat_to_xy(x, y, w, h, lon, lat)
    r = 8
    d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
    f = font(10, 700)
    d.text((px, py - 1), str(num), font=f, fill=(255, 255, 255), anchor="mm")
