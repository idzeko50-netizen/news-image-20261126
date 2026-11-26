#!/usr/bin/env python3
"""Draw the news-image-20261126 front page: one image summing up
Thursday 26 November 2026 in world news. Every illustration is drawn
in code with PIL; no photographs, no downloaded images.

Run: python3 compose.py   (writes entry/entry.png, 1024x1024)
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 227)
INK = (26, 26, 26)
RED = (163, 22, 33)
BLUE = (38, 84, 124)
GREY = (110, 104, 92)
LIGHT = (232, 222, 200)
SEA = (198, 214, 222)
LAND = (216, 201, 163)
GOLD = (176, 132, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s) \
    if os.path.exists(os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf")) \
    else font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(text, fnt, max_w, max_lines):
    """Greedy-wrap text to fit max_w; assert it fits in max_lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw_ctx.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    assert len(lines) <= max_lines, \
        f"overflow ({len(lines)}>{max_lines}): {text!r}"
    return lines


def text_block(x, y, lines, fnt, fill=INK, leading=None, align="left",
               box_w=None):
    """Draw lines starting at (x, y); returns bottom y."""
    lh = leading or int(fnt.size * 1.25)
    for ln in lines:
        if align == "center":
            tw = draw_ctx.textlength(ln, font=fnt)
            draw_ctx.text((x + (box_w - tw) / 2, y), ln, font=fnt, fill=fill)
        else:
            draw_ctx.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def tag_line(x, y, text, fnt, fill=RED):
    draw_ctx.text((x, y), text, font=fnt, fill=fill)


def hrule(y, x0=10, x1=1014, width=2, fill=INK):
    draw_ctx.line([(x0, y), (x1, y)], fill=fill, width=width)


def panel_frame(x, y, w, h):
    draw_ctx.rectangle([x, y, x + w - 1, y + h - 1], outline=GREY, width=1)


def scene_bg(x, y, w, h, colour):
    draw_ctx.rectangle([x, y, x + w - 1, y + h - 1], fill=colour)


# ---------------------------------------------------------------- scenes
# Each scene draws inside (x, y, w, h) in flat vector style.

def scene_tariffs(x, y, w, h):
    scene_bg(x, y, w, h, (222, 226, 232))
    # harbour sky, sea, container ship
    draw_ctx.rectangle([x, y, x + w, y + int(h * 0.42)], fill=(168, 196, 216))
    draw_ctx.rectangle([x, y + int(h * 0.42), x + w, y + h], fill=(96, 138, 168))
    draw_ctx.rectangle([x + 8, y + h - 26, x + w - 8, y + h - 12],
                       fill=(52, 58, 66))  # hull
    for i, c in enumerate([(163, 22, 33), (38, 84, 124), (176, 132, 40)]):
        cx = x + 16 + i * 52
        draw_ctx.rectangle([cx, y + h - 62, cx + 46, y + h - 28], fill=c)
        draw_ctx.line([(cx, y + h - 45), (cx + 46, y + h - 45)],
                      fill=(255, 255, 255), width=2)
    draw_ctx.rectangle([x + w - 88, y + 8, x + w - 12, y + 40], fill=RED)
    draw_ctx.text((x + w - 80, y + 12), "25%", font=SANS_B(20), fill=(255, 255, 255))


def scene_parade(x, y, w, h):
    scene_bg(x, y, w, h, (196, 214, 228))
    # storm clouds, rain, one big balloon
    for cx, cy in [(30, 18), (120, 8), (210, 20)]:
        draw_ctx.ellipse([x + cx, y + cy, x + cx + 70, y + cy + 26],
                         fill=(120, 130, 145))
    draw_ctx.ellipse([x + w // 2 - 46, y + 26, x + w // 2 + 46, y + 108],
                     fill=(214, 90, 60))
    draw_ctx.ellipse([x + w // 2 - 46, y + 26, x + w // 2 + 46, y + 60],
                     fill=(226, 120, 88))
    for dx in (-30, -10, 10, 30):
        draw_ctx.line([(x + w // 2 + dx, y + 104),
                       (x + w // 2 + dx // 2, y + h - 6)],
                      fill=(90, 90, 90), width=2)
    for rx in range(0, w, 26):
        draw_ctx.line([(x + rx, y + 52), (x + rx - 6, y + 68)],
                      fill=(140, 160, 180), width=2)
    draw_ctx.rectangle([x + 10, y + h - 24, x + 96, y + h - 6], fill=INK)
    draw_ctx.text((x + 16, y + h - 22), "SAT 28", font=SANS_B(12),
                  fill=(255, 255, 255))


def scene_space(x, y, w, h):
    scene_bg(x, y, w, h, (24, 32, 54))
    for sx, sy in [(20, 14), (70, 40), (130, 10), (200, 30), (260, 16),
                   (40, 90), (300, 70), (180, 96)]:
        draw_ctx.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                         fill=(255, 255, 255))
    cx, cy = x + w // 2, y + h // 2 + 8
    draw_ctx.ellipse([cx - 78, cy - 52, cx + 78, cy + 52], outline=(90, 120, 160),
                     width=2)
    for ang in range(0, 360, 45):
        import math
        px = cx + 78 * math.cos(math.radians(ang))
        py = cy + 52 * math.sin(math.radians(ang))
        draw_ctx.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GOLD)
    # rocket
    draw_ctx.polygon([(cx, cy - 44), (cx - 12, cy - 6), (cx + 12, cy - 6)],
                     fill=RED)
    draw_ctx.rectangle([cx - 12, cy - 6, cx + 12, cy + 22], fill=(230, 230, 230))
    draw_ctx.polygon([(cx - 12, cy + 22), (cx - 22, cy + 34), (cx - 12, cy + 26)],
                     fill=RED)
    draw_ctx.polygon([(cx + 12, cy + 22), (cx + 22, cy + 34), (cx + 12, cy + 26)],
                     fill=RED)
    draw_ctx.ellipse([cx - 5, cy - 2, cx + 5, cy + 8], fill=BLUE)


def scene_refinery(x, y, w, h):
    scene_bg(x, y, w, h, (238, 214, 178))
    draw_ctx.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(120, 96, 66))
    for tx in (18, 62, 106):
        draw_ctx.rectangle([x + tx, y + int(h * 0.30), x + tx + 22,
                            y + int(h * 0.55)], fill=(90, 90, 96))
        draw_ctx.rectangle([x + tx + 4, y + int(h * 0.18), x + tx + 18,
                            y + int(h * 0.30)], fill=(120, 120, 126))
    draw_ctx.ellipse([x + w - 62, y + 6, x + w - 10, y + int(h * 0.50)],
                     fill=(230, 120, 40))
    for dx, dy in [(0, 0), (14, -8), (-12, -10)]:
        draw_ctx.polygon([(x + w - 36 + dx, y + int(h * 0.20) + dy),
                          (x + w - 52 + dx, y + int(h * 0.40) + dy),
                          (x + w - 20 + dx, y + int(h * 0.40) + dy)],
                         fill=(245, 180, 60))
    # small drone
    draw_ctx.ellipse([x + 150, y + 14, x + 168, y + 26], fill=INK)
    draw_ctx.line([(x + 140, y + 12), (x + 178, y + 12)], fill=INK, width=2)
    draw_ctx.line([(x + 140, y + 28), (x + 178, y + 28)], fill=INK, width=2)


def scene_fire(x, y, w, h):
    scene_bg(x, y, w, h, (60, 60, 66))
    draw_ctx.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(40, 40, 44))
    draw_ctx.line([(x + 10, y + int(h * 0.62)), (x + w - 10, y + int(h * 0.62))],
                  fill=(240, 200, 60), width=4)
    # tanker truck
    draw_ctx.rectangle([x + 20, y + int(h * 0.30), x + 130, y + int(h * 0.58)],
                       fill=(200, 200, 205))
    draw_ctx.rectangle([x + 130, y + int(h * 0.38), x + 168, y + int(h * 0.58)],
                       fill=(163, 22, 33))
    for wx in (26, 90, 150):
        draw_ctx.ellipse([x + wx, y + int(h * 0.56), x + wx + 18, y + int(h * 0.56) + 18],
                         fill=INK)
    # flames
    for fx, fh in [(40, 0.30), (80, 0.42), (120, 0.26)]:
        fh_px = int(h * fh)
        draw_ctx.polygon([(x + fx, y + int(h * 0.30) - fh_px),
                          (x + fx - 16, y + int(h * 0.30)),
                          (x + fx + 16, y + int(h * 0.30))],
                         fill=(245, 140, 40))
    draw_ctx.ellipse([x + w - 46, y + 10, x + w - 14, y + 42], fill=(120, 120, 126))


def scene_mine(x, y, w, h):
    scene_bg(x, y, w, h, (214, 190, 150))
    draw_ctx.polygon([(x, y + h), (x, y + 30), (x + w // 2, y + 6),
                      (x + w, y + 30), (x + w, y + h)], fill=(110, 84, 56))
    draw_ctx.polygon([(x + w // 2 - 34, y + h), (x + w // 2 - 34, y + 52),
                      (x + w // 2 + 34, y + 52), (x + w // 2 + 34, y + h)],
                     fill=(20, 16, 12))
    draw_ctx.arc([x + w // 2 - 34, y + 18, x + w // 2 + 34, y + 86],
                 180, 360, fill=(20, 16, 12), width=4)
    # helmet
    draw_ctx.pieslice([x + 16, y + h - 34, x + 56, y + h - 4], 180, 360,
                      fill=(245, 180, 40))
    draw_ctx.rectangle([x + 12, y + h - 20, x + 60, y + h - 14], fill=(245, 180, 40))
    draw_ctx.ellipse([x + w - 52, y + h - 30, x + w - 20, y + h - 6],
                     fill=(245, 220, 90))


def scene_bank(x, y, w, h):
    scene_bg(x, y, w, h, (226, 232, 238))
    draw_ctx.polygon([(x + w // 2 - 60, y + int(h * 0.12)), (x + w // 2, y - 2),
                      (x + w // 2 + 60, y + int(h * 0.12))], fill=(120, 40, 48))
    for i in range(4):
        cx = x + 24 + i * 34
        draw_ctx.rectangle([cx, y + int(h * 0.20), cx + 16,
                            y + h - int(h * 0.20)], fill=(240, 240, 240))
    draw_ctx.rectangle([x + 12, y + h - int(h * 0.20), x + w - 12,
                        y + h - int(h * 0.11)], fill=(120, 40, 48))
    # rising arrow
    draw_ctx.line([(x + w - 62, y + h - int(h * 0.30)),
                   (x + w - 22, y + int(h * 0.23))], fill=RED, width=4)
    draw_ctx.polygon([(x + w - 22, y + int(h * 0.23)),
                      (x + w - 38, y + int(h * 0.25)),
                      (x + w - 24, y + int(h * 0.37))], fill=RED)
    draw_ctx.text((x + 12, y + int(h * 0.07)), "3.25%", font=SANS_B(16),
                  fill=RED)


def scene_gdp(x, y, w, h):
    scene_bg(x, y, w, h, (222, 232, 222))
    base = y + h - 18
    bars = [(20, 34), (52, 52), (84, 44), (116, 70), (148, 88)]
    for bx, bh in bars:
        bh = int(bh * h / 112)
        draw_ctx.rectangle([x + bx, base - bh, x + bx + 24, base],
                           fill=(38, 84, 124))
    draw_ctx.rectangle([x + 148, base - int(88 * h / 112), x + 172, base],
                       fill=RED)
    draw_ctx.line([(x + 12, base - int(30 * h / 112)),
                   (x + w - 20, base - int(92 * h / 112))], fill=RED, width=3)
    draw_ctx.text((x + 10, y + 6), "4.3%", font=SANS_B(20), fill=RED)


def scene_wave(x, y, w, h):
    scene_bg(x, y, w, h, (168, 200, 222))
    draw_ctx.ellipse([x + w - 52, y + int(h * 0.07), x + w - 14,
                      y + int(h * 0.41)], fill=(245, 220, 120))
    draw_ctx.ellipse([x - 30, y + int(h * 0.16), x + 150, y + int(h * 0.98)],
                     fill=(52, 110, 150))
    draw_ctx.ellipse([x + 60, y + int(h * 0.04), x + 230, y + int(h * 0.86)],
                     fill=(96, 150, 185))
    draw_ctx.rectangle([x, y + h - int(h * 0.27), x + w, y + h],
                       fill=(232, 222, 200))
    for hx in (16, 66, 116):
        draw_ctx.rectangle([x + hx, y + h - int(h * 0.47), x + hx + 34,
                            y + h - int(h * 0.27)], fill=(163, 90, 60))
        draw_ctx.polygon([(x + hx, y + h - int(h * 0.47)),
                          (x + hx + 17, y + h - int(h * 0.59)),
                          (x + hx + 34, y + h - int(h * 0.47))],
                         fill=(120, 60, 40))
    draw_ctx.ellipse([x + w - 40, y + h - int(h * 0.23), x + w - 16,
                      y + h - int(h * 0.07)], fill=(255, 255, 255))


def scene_flags(x, y, w, h):
    scene_bg(x, y, w, h, (216, 226, 232))
    # mountains
    draw_ctx.polygon([(x, y + h), (x + 60, y + int(h * 0.23)), (x + 120, y + h)],
                     fill=(120, 130, 140))
    draw_ctx.polygon([(x + 90, y + h), (x + 150, y + int(h * 0.11)),
                      (x + 210, y + h)], fill=(90, 100, 112))
    draw_ctx.polygon([(x + 138, y + int(h * 0.20)), (x + 150, y + int(h * 0.11)),
                      (x + 162, y + int(h * 0.20))], fill=(255, 255, 255))
    # India flag
    draw_ctx.line([(x + 26, y + int(h * 0.30)), (x + 26, y + h - int(h * 0.09))],
                  fill=INK, width=3)
    for i, c in enumerate([(230, 120, 40), (255, 255, 255), (30, 120, 60)]):
        draw_ctx.rectangle([x + 28, y + int(h * 0.30) + i * int(h * 0.11),
                            x + 84, y + int(h * 0.30) + (i + 1) * int(h * 0.11)],
                           fill=c)
    # China flag
    draw_ctx.line([(x + w - 28, y + int(h * 0.30)),
                   (x + w - 28, y + h - int(h * 0.09))], fill=INK, width=3)
    draw_ctx.rectangle([x + w - 86, y + int(h * 0.30), x + w - 30,
                        y + int(h * 0.62)], fill=(200, 30, 30))
    for sx, sy in [(x + w - 76, y + int(h * 0.36)), (x + w - 62, y + int(h * 0.34)),
                   (x + w - 66, y + int(h * 0.46)), (x + w - 56, y + int(h * 0.52))]:
        draw_ctx.ellipse([sx, sy, sx + 5, sy + 5], fill=(245, 220, 60))


def scene_medal(x, y, w, h):
    scene_bg(x, y, w, h, (238, 228, 200))
    cx = x + w // 2
    draw_ctx.polygon([(cx - 26, y + int(h * 0.09)), (cx - 8, y + int(h * 0.46)),
                      (cx + 8, y + int(h * 0.46)), (cx + 26, y + int(h * 0.09))],
                     fill=(163, 22, 33))
    draw_ctx.polygon([(cx - 8, y + int(h * 0.46)), (cx + 8, y + int(h * 0.46)),
                      (cx, y + int(h * 0.55))], fill=(120, 16, 24))
    r = int(h * 0.27)
    cy = y + int(h * 0.68)
    draw_ctx.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD,
                     outline=(140, 100, 20), width=3)
    r2 = int(h * 0.17)
    draw_ctx.ellipse([cx - r2, cy - r2, cx + r2, cy + r2],
                     outline=(140, 100, 20), width=2)
    draw_ctx.text((cx - 7, cy - 11), "*", font=SANS_B(22), fill=(140, 100, 20))


def scene_market(x, y, w, h):
    scene_bg(x, y, w, h, (232, 236, 228))
    base = y + h - 16
    pts = [(10, 62), (40, 54), (70, 58), (100, 40), (130, 44), (160, 24),
           (190, 18)]
    pts = [(px, int(py * h / 112)) for px, py in pts]
    for (px1, py1), (px2, py2) in zip(pts, pts[1:]):
        draw_ctx.line([(x + px1, y + py1), (x + px2, y + py2)],
                      fill=(30, 120, 60), width=3)
    draw_ctx.line([(x + 190, y + pts[-1][1]), (x + 176, y + pts[-1][1]),
                   (x + 190, y + pts[-1][1] - 14)], fill=(30, 120, 60), width=3)
    draw_ctx.text((x + 8, y + 4), "+1.6%", font=SANS_B(15), fill=(30, 120, 60))
    draw_ctx.text((x + w - 62, y + h - 26), "NIKKEI", font=SANS_B(10), fill=GREY)


def scene_meerkat(x, y, w, h):
    scene_bg(x, y, w, h, (228, 214, 176))
    s = h / 112
    draw_ctx.rectangle([x, y + h - int(22 * s), x + w, y + h],
                       fill=(150, 120, 70))
    for mx, mh, mw in [(52, 62, 34), (128, 74, 40)]:
        mh = int(mh * s)
        mw = int(mw * s)
        top = y + h - int(22 * s) - mh
        draw_ctx.ellipse([x + mx - mw // 2, top,
                          x + mx + mw // 2, y + h - int(22 * s)],
                         fill=(178, 138, 88))
        draw_ctx.ellipse([x + mx - mw // 2 - 2, top - int(26 * s),
                          x + mx + mw // 2 + 2, top + int(6 * s)],
                         fill=(178, 138, 88))
        draw_ctx.ellipse([x + mx - mw // 2 - 2, top - int(30 * s),
                          x + mx - mw // 2 + 8, top - int(20 * s)],
                         fill=(150, 112, 66))
        draw_ctx.ellipse([x + mx + mw // 2 - 8, top - int(30 * s),
                          x + mx + mw // 2 + 2, top - int(20 * s)],
                         fill=(150, 112, 66))
        draw_ctx.ellipse([x + mx - 9, top - int(18 * s),
                          x + mx - 2, top - int(11 * s)], fill=INK)
        draw_ctx.ellipse([x + mx + 2, top - int(18 * s),
                          x + mx + 9, top - int(11 * s)], fill=INK)
        draw_ctx.ellipse([x + mx - 4, top - int(8 * s),
                          x + mx + 4, top - int(2 * s)], fill=(60, 40, 24))
    draw_ctx.ellipse([x + w - 30, y + int(8 * s), x + w - 8, y + int(30 * s)],
                     fill=(245, 220, 120))


SCENES = {
    "tariffs": scene_tariffs, "parade": scene_parade, "space": scene_space,
    "refinery": scene_refinery, "fire": scene_fire, "mine": scene_mine,
    "bank": scene_bank, "gdp": scene_gdp, "wave": scene_wave,
    "flags": scene_flags, "medal": scene_medal, "market": scene_market,
    "meerkat": scene_meerkat,
}

# ---------------------------------------------------------------- data

LARGE = [
    ("tariffs", "TARIFFS · WASHINGTON",
     "Trump hits 14 partners with new tariffs",
     "Duties aimed at China, India and the EU; India faces 25% "
     "without a deal."),
    ("parade", "THANKSGIVING · NEW YORK",
     "Macy's parade put off to Saturday",
     "The 100th parade is postponed for the first time ever as a "
     "nor'easter brings gales."),
    ("space", "SPACE · WASHINGTON",
     "FCC clears 1m satellites for space data centres",
     "SpaceX's 'Starmind' network gets the first US licence for "
     "orbital AI computing."),
]

SMALL = [
    ("refinery", "MIDDLE EAST",
     "Houthis claim Saudi refinery strike",
     "Rebels claim refinery hits; four drones intercepted."),
    ("fire", "AFRICA",
     "30 killed in Cairo tanker fire",
     "A fuel-truck crash sets cars ablaze on Cairo's Ring Road."),
    ("mine", "ASIA",
     "13 dead in Indonesia gold mine",
     "Rescuers hunt for 13 more trapped in the West Java mine."),
    ("bank", "ASIA",
     "Seoul raises rates to 3.25%",
     "Seoul resumes tightening as a chip boom lifts prices."),
    ("gdp", "AMERICAS",
     "US growth revised up to 4.3%",
     "GDP beats hopes; the Fed's core inflation hits 3.3%."),
    ("wave", "AMERICAS",
     "King tides batter California",
     "Huge surf floods homes as storms hit Thanksgiving travel."),
    ("flags", "ASIA",
     "India and China talk borders",
     "Generals meet in Arunachal over the disputed border."),
    ("medal", "AMERICAS",
     "Giuliani gets Medal of Freedom",
     "The ex-mayor is honoured by Trump in Washington."),
    ("market", "MARKETS",
     "Asian shares bounce back",
     "Nikkei +1.6%, Kospi +1.9%; Nvidia fell 3.9% on Wednesday."),
    ("meerkat", "CULTURE",
     "Twin meerkats make their debut",
     "Two baby meerkats step out at a Peruvian zoo."),
]

INDEX = [
    ("14", "Jobless claims fall to 189,000 in the US"),
    ("15", "US intel flags possible surveillance of Alice Huang"),
    ("16", "Vance serves Thanksgiving meal to troops in Ohio"),
    ("17", "Shirley testifies on Minnesota daycare fraud claims"),
    ("18", "Uber names Rakesh Ranjan to lead India, South Asia"),
    ("19", "JETRO: Chinese firms press Japanese rivals abroad"),
    ("20", "India–Nepal joint army exercise opens in Rupandehi"),
    ("21", "India, Singapore to work on aircraft repair hubs"),
    ("22", "India cabinet clears ₹2,632 cr postal revamp"),
    ("23", "Chess Game 3 today: Gukesh–Sindarov level at 1–1"),
    ("24", "UN: world HIV fight under pressure despite gains"),
    ("25", "China and Cambodia stage joint military drills"),
    ("26", "Colombia troops storm shop, free hostages"),
    ("27", "UK to put its EU deal before parliament"),
    ("28", "Thanksgiving travel: long lines and bad weather"),
    ("29", "India silent on Hasina's reported return plan"),
    ("30", "RNZ probes suspected cyber breach"),
]

NUMBERS = [
    ("14", "trade partners face tariffs"),
    ("30", "killed in Cairo tanker fire"),
    ("13", "dead in Indonesia gold mine"),
    ("3.25%", "Bank of Korea rate after hike"),
    ("189,000", "US jobless claims, falling"),
    ("1m", "SpaceX satellites cleared"),
]

REGIONS = [("Americas", 13, (163, 22, 33)), ("Asia", 10, (38, 84, 124)),
           ("Middle East", 1, (176, 132, 40)), ("Africa", 1, (30, 120, 60)),
           ("Europe", 1, (110, 104, 92)), ("Global", 3, (90, 60, 110)),
           ("Oceania", 1, (30, 140, 140))]


# ---------------------------------------------------------------- map
# Rough equirectangular continents; pins carry the 13 featured stories.

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60),
     (-158, 58), (-168, 66)],
    # South America
    [(-80, 9), (-62, 10), (-52, 5), (-40, -5), (-35, -9), (-40, -22),
     (-48, -28), (-58, -38), (-65, -45), (-70, -54), (-73, -37),
     (-72, -20), (-80, -3), (-80, 9)],
    # Africa
    [(-17, 15), (-10, 31), (10, 37), (20, 32), (32, 31), (43, 12),
     (51, 11), (40, -5), (40, -20), (33, -29), (20, -35), (12, -18),
     (9, -1), (-8, 4), (-17, 15)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 49), (0, 51), (5, 58), (10, 59), (18, 56),
     (21, 55), (24, 60), (30, 60), (28, 45), (23, 40), (19, 42), (12, 44),
     (8, 38), (0, 36), (-10, 36)],
    # Asia
    [(30, 60), (40, 68), (60, 69), (80, 73), (110, 74), (140, 72),
     (160, 66), (162, 60), (142, 50), (140, 40), (127, 35), (122, 30),
     (110, 20), (105, 9), (100, 8), (97, 16), (90, 22), (80, 13),
     (77, 8), (73, 20), (66, 25), (57, 26), (50, 29), (44, 29),
     (35, 28), (36, 36), (30, 45), (30, 60)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (142, -11), (146, -19),
     (153, -27), (150, -37), (140, -38), (130, -32), (122, -34),
     (115, -35), (114, -22)],
]

# (number, lon, lat, display dx, dy) — dx/dy spread crowded US-east pins.
PINS = [
    (1, -77, 39, 0, 0), (2, -74, 41, 16, -14), (3, -80, 28, -2, 14),
    (4, 47, 25, 0, 0), (5, 31, 30, -8, 14), (6, 107, -7, 0, 0),
    (7, 127, 37, 0, 0), (8, -100, 39, 0, 0), (9, -122, 37, 0, 0),
    (10, 95, 28, 0, 0), (11, -77, 39, 14, 10), (12, 139, 36, 12, -12),
    (13, -77, -12, 0, 0),
]


def draw_map(x, y, w, h):
    draw_ctx.rectangle([x, y, x + w - 1, y + h - 1], fill=SEA)
    for cont in CONTINENTS:
        pts = [(x + (lon + 170) / 360 * w, y + (85 - lat) / 145 * h)
               for lon, lat in cont]
        draw_ctx.polygon(pts, fill=LAND, outline=(160, 140, 100))
    draw_ctx.text((x + 6, y + 4), "WHERE IT HAPPENED", font=SANS_B(10),
                  fill=INK)
    for num, lon, lat, dx, dy in PINS:
        px = x + (lon + 170) / 360 * w
        py = y + (85 - lat) / 145 * h
        qx, qy = px + dx, py + dy
        if dx or dy:
            draw_ctx.line([(px, py), (qx, qy)], fill=INK, width=1)
        draw_ctx.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=RED,
                         outline=(255, 255, 255), width=1)
        tw = draw_ctx.textlength(str(num), font=SANS_B(10))
        draw_ctx.text((qx - tw / 2, qy - 7), str(num), font=SANS_B(10),
                      fill=(255, 255, 255))


# ---------------------------------------------------------------- panels

def draw_large_panel(x, y, w, h, scene, tag, headline, deck):
    panel_frame(x, y, w, h)
    SCENES[scene](x + 1, y + 1, w - 2, 112)
    tag_line(x + 8, y + 120, tag, SANS_B(10))
    hl = wrap(headline, SANS_B(15), w - 16, 2)
    text_block(x + 8, y + 136, hl, SANS_B(15), leading=18)
    dl = wrap(deck, SANS(12), w - 16, 2)
    text_block(x + 8, y + 174, dl, SANS(12), leading=15)


def draw_small_panel(x, y, w, h, scene, tag, headline, deck):
    panel_frame(x, y, w, h)
    SCENES[scene](x + 1, y + 1, w - 2, 64)
    tag_line(x + 7, y + 70, tag, SANS_B(9))
    hl = wrap(headline, SANS_B(12), w - 14, 2)
    text_block(x + 7, y + 84, hl, SANS_B(12), leading=14)
    dl = wrap(deck, SANS(11), w - 14, 2)
    text_block(x + 7, y + 114, dl, SANS(11), leading=13)


# ---------------------------------------------------------------- build

def build():
    global draw_ctx
    img = Image.new("RGB", (W, H), CREAM)
    draw_ctx = ImageDraw.Draw(img)

    # masthead
    hrule(10, width=3)
    hrule(15, width=1)
    title = "Thursday 26 November 2026"
    tw = draw_ctx.textlength(title, font=SERIF_B(44))
    draw_ctx.text(((W - tw) / 2, 22), title, font=SERIF_B(44), fill=INK)
    strap = ("Every story below happened, or was first reported, "
             "on this day.")
    sw = draw_ctx.textlength(strap, font=SERIF_I(15))
    draw_ctx.text(((W - sw) / 2, 76), strap, font=SERIF_I(15), fill=INK)
    hrule(96, width=1)

    # number strip: six cells
    cell_w = (1014 - 10) // 6
    for i, (num, label) in enumerate(NUMBERS):
        cx = 10 + i * cell_w
        if i:
            draw_ctx.line([(cx, 102), (cx, 140)], fill=GREY, width=1)
        nw = draw_ctx.textlength(num, font=SANS_B(20))
        draw_ctx.text((cx + (cell_w - nw) / 2, 102), num, font=SANS_B(20),
                      fill=RED)
        lab = wrap(label, SANS(10), cell_w - 12, 2)
        text_block(cx + 6, 126, lab, SANS(10), leading=12, fill=GREY)
    hrule(146, width=1)

    # region bar
    total = sum(c for _, c, _ in REGIONS)
    bx, bw, by, bh = 10, 1004, 154, 12
    pos = bx
    for name, count, colour in REGIONS:
        seg = bw * count / total
        draw_ctx.rectangle([pos, by, pos + seg - 1, by + bh - 1], fill=colour)
        pos += seg
    legend = "   ".join(f"{n} {c}" for n, c, _ in REGIONS)
    lw = draw_ctx.textlength(legend, font=SANS(11))
    draw_ctx.text(((W - lw) / 2, 170), legend, font=SANS(11), fill=INK)

    # section label
    draw_ctx.text((10, 192), "THE DAY IN THIRTEEN PICTURES", font=SANS_B(13),
                  fill=INK)
    draw_ctx.text((1014 - draw_ctx.textlength("30 STORIES · 7 REGIONS",
                                              font=SANS_B(13)), 192),
                  "30 STORIES · 7 REGIONS", font=SANS_B(13), fill=RED)

    # large panels
    for i, (scene, tag, hl, dk) in enumerate(LARGE):
        draw_large_panel(10 + i * 332, 212, 322, 212, scene, tag, hl, dk)

    # small panels, two rows of five
    for row in range(2):
        for col in range(5):
            item = SMALL[row * 5 + col]
            draw_small_panel(10 + col * 204, 432 + row * 158, 194, 152,
                             item[0], item[1], item[2], item[3])

    # bottom: map + date check (left), index (right)
    draw_map(10, 750, 346, 130)
    dc_y = 888
    draw_ctx.rectangle([10, dc_y, 355, 978], outline=RED, width=2)
    draw_ctx.text((20, dc_y + 6), "DATE CHECK — NOT TODAY:",
                  font=SANS_B(11), fill=RED)
    dc_lines = [
        "Kim's nuclear call · Sudan strikes (19 killed) ·",
        "Ramaphosa court win — all 25 Nov",
        "Shein $100m FTC deal · Venice Biennale India win ·",
        "Chess Game 2 — 24–25 Nov",
        "Real Madrid 5–1 PSV · Lebanon's second airport — 25 Nov",
    ]
    text_block(20, dc_y + 24, dc_lines, SANS(10.5), leading=13)

    draw_ctx.text((366, 750), "ALSO TODAY", font=SANS_B(13), fill=INK)
    hrule(768, x0=366, width=1)
    col_w = 316
    for i, (num, text) in enumerate(INDEX):
        col = i // 9
        row = i % 9
        ix = 366 + col * (col_w + 16)
        iy = 776 + row * 23
        draw_ctx.text((ix, iy), f"{num}.", font=SANS_B(11), fill=RED)
        item = wrap(text, SANS(11), col_w - 24, 1)
        draw_ctx.text((ix + 24, iy), item[0], font=SANS(11), fill=INK)

    # footer
    hrule(988, width=1)
    foot = ("Drawn entirely in code — no photographs. Sources: Reuters, AP, "
            "Economic Times, Al Jazeera, BBC, Manila Times, NZ Herald.")
    fw = draw_ctx.textlength(foot, font=SANS(10))
    draw_ctx.text(((W - fw) / 2, 994), foot, font=SANS(10), fill=GREY)

    return img


def main():
    img = build()
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    data = open(path, "rb").read()
    print(f"entry.png: {len(data)} bytes, {img.size[0]}x{img.size[1]}, "
          f"sha256={hashlib.sha256(data).hexdigest()}")
    assert len(data) <= 1048576, "over 1 MiB"
    assert img.size == (1024, 1024)


if __name__ == "__main__":
    main()
