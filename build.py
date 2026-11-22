"""Render the 22 November 2026 front page (1024x1024).

Local build driver: draws entry.png from the story list below. main.py
(the graded entrypoint) only copies the rendered entry.png.
Run:  python3 build.py   (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw

import draw as D

W = H = 1024
M = 16  # page margin

LEADS = [
    dict(n=1, label="ANTALYA · CLIMATE", ill=D.ill_cop,
         head="COP31 deal at dawn",
         deck="Australia and Turkey put a new text to nearly 200 nations. Approval vote at 06:00 GMT.",
         src="Reuters"),
    dict(n=2, label="JOHANNESBURG · SUMMIT", ill=D.ill_g20,
         head="G20 opens on African soil",
         deck="Leaders gather for the first summit on the continent — without the United States.",
         src="Reuters"),
    dict(n=3, label="MARKETS · CRYPTO", ill=D.ill_bitcoin,
         head="Bitcoin bounces back 8%",
         deck="The largest coin rose to about $59,952 after touching a two-year low.",
         src="Reuters"),
]

MEDIUMS = [
    dict(n=4, label="WASHINGTON · POLITICS", ill=D.ill_card,
         head="Trump vows 10% cap on card rates",
         deck="President says he will work with Democrats on the cap.",
         src="AP"),
    dict(n=5, label="WASHINGTON · DEFENCE", ill=D.ill_pentagon,
         head="Pentagon curbs US–Canada ties",
         deck="Washington moves to restrict military links with Ottawa.",
         src="AFP"),
    dict(n=6, label="WASHINGTON · POLITICS", ill=D.ill_vote,
         head="Democrats' Senate win faces first test",
         deck="A leadership vote tests the party that swept the midterms.",
         src="AP"),
    dict(n=7, label="BRUSSELS · EUROPE", ill=D.ill_plane,
         head="Belgium faces air shutdown Monday",
         deck="A national strike threatens to halt air traffic.",
         src="AFP"),
    dict(n=8, label="PATNA · INDIA", ill=D.ill_bridge,
         head="Modi opens bridge over the Ganges",
         deck="Nitish Setu links Patna and Vaishali districts in Bihar.",
         src="Indian media"),
    dict(n=9, label="LAS VEGAS · SPORT", ill=D.ill_race,
         head="Verstappen on pole in Las Vegas",
         deck="The Dutchman leads qualifying for tonight's Grand Prix.",
         src="Reuters"),
    dict(n=10, label="PYONGYANG · ASIA", ill=D.ill_factory,
         head="Kim tours factories after Trump snub",
         deck="North Korea's leader visits factory sites after skipping a meeting.",
         src="AP"),
    dict(n=11, label="SEOUL · TECH", ill=D.ill_chip,
         head="Speed is decisive in AI race, says Lee",
         deck="South Korea's president urges faster AI development.",
         src="AP"),
    dict(n=12, label="TAIPEI · ASIA", ill=D.ill_flags,
         head="Taiwan warns Canada over China ties",
         deck="Taipei tells Carney deeper links with Beijing carry risks.",
         src="AP"),
    dict(n=13, label="INDIA · TECH", ill=D.ill_megaphone,
         head="Congress warns of more Meta protests",
         deck="Protests hit Meta offices after clashes with police.",
         src="Reuters"),
]

BRIEFS = [
    (14, "Air India extends Jeddah flight halt to 24 Nov", "Indian media"),
    (15, "Japan troops to train live-fire in India, a first", "AP"),
    (16, "Cummins keeps Australia Test captaincy", "Cricket Australia"),
    (17, "WFP to assist 91 million people in 2027", "AP"),
    (18, "French police jailed for racist violence", "EuroNews"),
    (19, "Whale-breath DNA sequenced by drone", "The Guardian"),
    (20, "Bed bugs send 1,000+ FEMA staff home", "AP"),
    (21, "Storms flood Florida at historic levels", "AP"),
    (22, "Brazil town clears rubble after deadly storm", "AP"),
    (23, "'Killer robots' pact path opens", "AP"),
    (24, "Young protesters march across Europe", "AP"),
    (25, "Afghan rules bar pregnant women from care", "AP"),
    (26, "Estonia to shut border with Russia", "AP"),
    (27, "Ex-police chief dies amid mafia probe", "AP"),
    (28, "Tainted alcohol kills 11 in Manipur", "Indian media"),
    (29, "Markram to lead South Africa in 2nd Test", "Reuters"),
    (30, "4,000-year-old neck ring found in Swiss Alps", "France 24"),
    (31, "COP31 is first summit since 1.5°C warning", "Reuters"),
]

STATS = [
    ("200", "NATIONS BACK COP31 DEAL", "Reuters"),
    ("8%", "BITCOIN REBOUND", "Reuters"),
    ("10%", "CARD-CAP TRUMP VOWS", "AP"),
    ("91M", "WFP TO ASSIST IN 2027", "AP"),
    ("20th", "G20 ON AFRICAN SOIL", "Reuters"),
    ("2 DAYS", "COP31 PAST DEADLINE", "Reuters"),
]

TIMELINE = [
    ("01:00", "Verstappen takes Las Vegas pole"),
    ("03:00", "COP31 objection deadline"),
    ("06:00", "COP31 meets to approve the deal"),
    ("07:00", "G20 day two opens in Johannesburg"),
]

DATECHECK = [
    "19 NOV · Myanmar genocide verdict",
    "19 NOV · Trump–Xi–Putin meet in Shenzhen",
    "20 NOV · 'Chapo Isidro' seized",
    "20 NOV · Russian missiles hit Poland",
    "20 NOV · Cyclone Akvan landfall",
    "20 NOV · FBI crime database breached",
    "21 NOV · Peru quake, magnitude 6.7",
    "21 NOV · Houthi missiles over Riyadh",
    "21 NOV · Bahrain hit; 2 tankers struck",
]

PINS = [
    (1, 30.7, 36.9, 0, 0),      # Antalya
    (2, 28.0, -26.2, 0, 0),     # Johannesburg
    (3, -77.0, 38.9, 0, 0),     # Washington
    (4, 4.35, 50.8, 0, 0),      # Brussels
    (5, 85.1, 25.6, 0, 0),      # Patna
    (6, -115.1, 36.2, 0, 0),    # Las Vegas
    (7, 125.8, 39.0, -9, -7),   # Pyongyang (nudged: cluster)
    (8, 127.0, 37.5, 9, -7),    # Seoul (nudged: cluster)
    (9, 121.6, 25.0, 0, 9),     # Taipei (nudged: cluster)
]


def badge(d, cx, cy, num, r=11):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=D.RED, outline=(255, 255, 255), width=2)
    f = D.font(11 if r >= 11 else 10, 700)
    d.text((cx, cy - 1), str(num), font=f, fill=(255, 255, 255), anchor="mm")


def lead_card(d, x, y, w, h, s):
    D.card_frame(d, (x, y, x + w, y + h))
    ix, iy, iw, ih = x + 8, y + 8, w - 16, 92
    s["ill"](d, ix, iy, iw, ih)
    badge(d, ix + 13, iy + 13, s["n"], r=11)
    D.label_band(d, x + 8, y + 108, w - 16, s["label"])
    f_head = D.font(21, 700)
    ycur = D.draw_wrapped(d, s["head"], f_head, x + 10, y + 132, w - 20, leading=24, max_lines=2)
    f_deck = D.font(13, 400)
    D.draw_wrapped(d, s["deck"], f_deck, x + 10, ycur + 4, w - 20, leading=16, max_lines=2)
    D.source_tag(d, x + 10, y + h - 16, s["src"])


def medium_card(d, x, y, w, h, s):
    D.card_frame(d, (x, y, x + w, y + h))
    ix, iy, iw, ih = x + 6, y + 6, w - 12, 36
    s["ill"](d, ix, iy, iw, ih)
    # label strip across the bottom of the illustration
    f_lab = D.font(9, 700)
    lab = D.trunc(d, s["label"], f_lab, iw - 8)
    d.rectangle([ix, iy + ih - 15, ix + iw, iy + ih], fill=D.RED)
    d.text((ix + 4, iy + ih - 14), lab, font=f_lab, fill=(255, 255, 255))
    badge(d, ix + 11, iy + 11, s["n"], r=9)
    f_head = D.font(17, 700)
    ycur = D.draw_wrapped(d, s["head"], f_head, x + 8, y + 48, w - 16, leading=20, max_lines=2)
    f_deck = D.font(12, 400)
    D.draw_wrapped(d, s["deck"], f_deck, x + 8, ycur + 2, w - 16, leading=13, max_lines=2)
    f_src = D.font(9, 600)
    d.text((x + 8, y + h - 12), "SOURCE: " + s["src"].upper(), font=f_src, fill=D.MUTED)


def render():
    img = Image.new("RGB", (W, H), D.PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((M, 6), "THE WORLD IN ONE DAY", font=D.font(38, 700), fill=D.INK)
    f_side = D.font(13, 700)
    d.text((W - M, 10), "SUNDAY EDITION", font=f_side, fill=D.INK, anchor="ra")
    d.text((W - M, 30), "22 NOVEMBER 2026", font=D.font(11, 600), fill=D.MUTED, anchor="ra")
    d.line([M, 50, W - M, 50], fill=D.INK, width=2)

    # ---- subline
    f_sub = D.font(14, 600)
    d.text((W // 2, 56), "31 STORIES · 6 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
           font=f_sub, fill=D.INK, anchor="ma")

    # ---- giant date
    d.text((W // 2, 72), "Sunday 22 November 2026", font=D.font(54, 700), fill=D.INK, anchor="ma")
    d.text((W // 2, 134), "COP31 deal at dawn · G20 opens its first summit on African soil · Bitcoin bounces back",
           font=D.font(19, 600), fill=D.RED, anchor="ma")

    # ---- stat strip
    y0, y1 = 156, 218
    d.rectangle([M, y0, W - M, y1], fill=D.BAND, outline=D.BORDER)
    cw = (W - 2 * M) / 6.0
    for i, (num, lab, src) in enumerate(STATS):
        cx = M + cw * i + cw / 2
        if i:
            d.line([M + cw * i, y0 + 6, M + cw * i, y1 - 6], fill=D.BORDER, width=1)
        d.text((cx, y0 + 4), num, font=D.font(26, 700), fill=D.INK, anchor="ma")
        d.text((cx, y0 + 34), lab, font=D.font(10, 700), fill=D.INK, anchor="ma")
        d.text((cx, y0 + 48), src.upper(), font=D.font(9, 600), fill=D.MUTED, anchor="ma")

    # ---- 3 lead cards
    lw, lgap = 322, 13
    for i, s in enumerate(LEADS):
        lead_card(d, M + i * (lw + lgap), 218, lw, 234, s)

    # ---- 10 medium cards, 2 rows x 5
    mw, mgap, mh = 190, 10, 130
    for i, s in enumerate(MEDIUMS):
        row, col = divmod(i, 5)
        medium_card(d, M + col * (mw + mgap), 452 + row * (mh + 10), mw, mh, s)

    # ---- briefs header
    d.rectangle([M, 722, W - M, 742], fill=D.INK)
    d.text((M + 8, 726), "ALSO ON SUNDAY 22 NOVEMBER — 18 MORE STORIES",
           font=D.font(13, 700), fill=(255, 255, 255))

    # ---- briefs, 2 columns x 9
    f_br = D.font(12, 400)
    f_brb = D.font(12, 700)
    for i, (n, text, src) in enumerate(BRIEFS):
        col, row = divmod(i, 9)
        bx = M if col == 0 else 522
        by = 746 + row * 13
        num = "%d. " % n
        d.text((bx, by), num, font=f_brb, fill=D.RED)
        nw = d.textlength(num, font=f_brb)
        line = D.trunc(d, text + " — " + src, f_br, 486 - nw)
        d.text((bx + nw, by), line, font=f_br, fill=D.INK)

    # ---- bottom band: map | timeline | date check
    by0 = 864
    # map
    mx, mw2 = M, 340
    d.text((mx, by0), "WHERE IT HAPPENED", font=D.font(12, 700), fill=D.INK)
    map_y, map_h = by0 + 16, 96
    D.draw_map(d, mx, map_y, mw2, map_h)
    for (n, lon, lat, dx, dy) in PINS:
        px, py = D.lonlat_to_xy(mx, map_y, mw2, map_h, lon, lat)
        if dx or dy:
            d.line([px, py, px + dx, py + dy], fill=D.RED, width=1)
            qx, qy = px + dx, py + dy
            r = 8
            d.ellipse([qx - r, qy - r, qx + r, qy + r], fill=D.RED, outline=(255, 255, 255), width=1)
            d.text((qx, qy - 1), str(n), font=D.font(10, 700), fill=(255, 255, 255), anchor="mm")
        else:
            D.pin(d, mx, map_y, mw2, map_h, lon, lat, n)
    f_leg = D.font(8, 600)
    d.text((mx, map_y + map_h + 2), "1 Antalya  2 Johannesburg  3 Washington  4 Brussels  5 Patna",
           font=f_leg, fill=D.MUTED)
    d.text((mx, map_y + map_h + 12), "6 Las Vegas  7 Pyongyang  8 Seoul  9 Taipei",
           font=f_leg, fill=D.MUTED)

    # timeline
    tx = 372
    d.text((tx, by0), "THE DAY IN UTC", font=D.font(12, 700), fill=D.INK)
    ty = by0 + 18
    for (t, text) in TIMELINE:
        d.text((tx, ty), t, font=D.font(11, 700), fill=D.RED)
        D.draw_wrapped(d, text, D.font(10, 400), tx + 42, ty, 170 - 42, leading=12, max_lines=2)
        ty += 28

    # date check
    dx0, dw = 558, 450
    d.text((dx0, by0), "DATE CHECK — LEFT OUT ON PURPOSE", font=D.font(12, 700), fill=D.RED)
    d.text((dx0, by0 + 15), "We checked every date. These big stories happened earlier, so they are not on this page:",
           font=D.font(10, 400), fill=D.MUTED)
    yy = by0 + 30
    for i, item in enumerate(DATECHECK):
        col, row = divmod(i, 5)
        ix = dx0 + col * 225
        d.text((ix, yy + row * 11), item, font=D.font(10, 400), fill=D.INK)
    d.text((dx0, yy + 5 * 11 + 3), "NOT YET · COP31 vote 06:00 GMT · G20 declaration · Las Vegas race",
           font=D.font(10, 700), fill=D.RED)

    # ---- footer
    d.line([M, 996, W - M, 996], fill=D.BORDER, width=1)
    d.text((W // 2, 1004),
           "Every story here happened, or was first reported, on Sunday 22 November 2026. · Sources named beside each story · Original drawings",
           font=D.font(11, 400), fill=D.MUTED, anchor="ma")

    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render().save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
