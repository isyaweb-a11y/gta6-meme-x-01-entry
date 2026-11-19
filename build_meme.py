#!/usr/bin/env python3
"""Compose the gta6-meme-x-01 meme candidates with PIL.

Candidate 1 (primary): "IN LINE SINCE 2013" — a Vice City sunset queue outside a
game store; the fans in line have visibly aged (kid -> adult -> grey -> grandpa),
and the make.fun ghost is next in line, coin in hand. Bottom line sells make.fun.
Candidate 2: launch-night ghost holding a GTA VI case, "paid for by my agent".
All art is drawn here except the official make.fun ghost (press kit mark.svg,
rendered to ghost.png with the disc removed).
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W = H = 1200
INK = (18, 6, 31, 255)          # near-black purple silhouette
DARK = (22, 10, 38, 255)


def font(size):
    return ImageFont.truetype(FONT, size)


def text(draw, xy, s, size, fill, stroke=0, stroke_fill=(0, 0, 0, 255), anchor="mm"):
    draw.text(xy, s, font=font(size), fill=fill, stroke_width=stroke,
              stroke_fill=stroke_fill, anchor=anchor)


def gradient(w, h, stops):
    """Vertical gradient through (pos, color) stops."""
    img = Image.new("RGB", (w, h))
    px = img.load()
    stops = sorted(stops)
    for y in range(h):
        t = y / (h - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                f = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                col = tuple(round(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
                break
        else:
            col = stops[-1][1]
        for x in range(w):
            px[x, y] = col
    return img


def palm(draw, x, base, h, lean=1, color=INK):
    """Palm silhouette: curved trunk + smooth drooping fronds."""
    top = (x + lean * h * 0.16, base - h)
    pts = []
    for i in range(25):
        t = i / 24
        px_ = x + (top[0] - x) * t + math.sin(t * math.pi) * lean * 8
        py_ = base + (top[1] - base) * t
        pts.append((px_, py_))
    draw.line(pts, fill=color, width=max(7, h // 20))
    cx, cy = top
    # fronds: quadratic curves from the crown, arcing up then drooping down
    for (dx, peak, drop) in [(-1.00, -0.16, 0.30), (-0.72, -0.30, 0.16),
                             (-0.38, -0.38, 0.05), (0.05, -0.40, 0.02),
                             (0.48, -0.36, 0.08), (0.82, -0.28, 0.20),
                             (1.05, -0.14, 0.34)]:
        L = h * 0.42
        ex, ey = cx + dx * L, cy + drop * h
        mx, my = cx + dx * L * 0.5, cy + peak * h
        curve = []
        for i in range(17):
            t = i / 16
            qx = (1 - t) ** 2 * cx + 2 * (1 - t) * t * mx + t ** 2 * ex
            qy = (1 - t) ** 2 * cy + 2 * (1 - t) * t * my + t ** 2 * ey
            curve.append((qx, qy))
        draw.line(curve, fill=color, width=max(5, h // 34))


def person(draw, cx, base, h, hair=(20, 10, 30, 255), cap=False, grey=False,
           hunched=False, cane=False, beard=False):
    """Flat standing-person silhouette with aging cues."""
    hr = h * 0.105                      # head radius
    lean = h * 0.10 if hunched else 0
    hx, hy = cx + lean, base - h + hr
    bw = h * 0.30                       # body width
    # body: shoulders to ground (long silhouette)
    draw.rounded_rectangle([cx - bw / 2 + lean * 0.4, hy + hr * 0.7,
                            cx + bw / 2 + lean * 0.4, base], radius=bw * 0.32, fill=INK)
    # head
    draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=INK)
    if cap:
        draw.pieslice([hx - hr * 1.02, hy - hr * 1.02, hx + hr * 1.02, hy + hr * 0.55],
                      180, 360, fill=(200, 30, 110, 255))
        draw.rounded_rectangle([hx + hr * 0.55, hy - hr * 0.30, hx + hr * 1.85, hy - hr * 0.02],
                               radius=6, fill=(200, 30, 110, 255))
    if grey:
        draw.pieslice([hx - hr, hy - hr, hx + hr, hy + hr * 0.3], 180, 360,
                      fill=(205, 205, 215, 255))
    if beard:
        draw.polygon([(hx - hr * 0.45, hy + hr * 0.45), (hx + hr * 0.65, hy + hr * 0.45),
                      (hx + hr * 0.38, hy + hr * 1.45), (hx - hr * 0.05, hy + hr * 1.45)],
                     fill=(225, 225, 232, 255))
    if cane:
        top = (cx - bw * 0.28, base - h * 0.44)
        bot = (cx - bw * 0.60, base)
        draw.line([top, bot], fill=(230, 230, 238, 255), width=7)
        draw.arc([top[0] - 4, top[1] - 26, top[0] + 26, top[1] + 6], 270, 360,
                 fill=(230, 230, 238, 255), width=7)


def ghost_tile():
    g = Image.open(os.path.join(HERE, "assets", "ghost.png")).convert("RGBA")
    return g.crop(g.getbbox())


def paste_ghost(base_img, cx, baseline, width):
    g = ghost_tile()
    gh = round(width * g.height / g.width)
    g = g.resize((width, gh), Image.LANCZOS)
    base_img.alpha_composite(g, (round(cx - width / 2), round(baseline - gh)))
    return gh


def candidate1():
    sky = gradient(W, H, [(0.0, (38, 14, 74)), (0.42, (110, 30, 110)),
                          (0.66, (208, 60, 120)), (0.82, (250, 130, 70)),
                          (0.90, (255, 170, 90))]).convert("RGBA")
    d = ImageDraw.Draw(sky)
    # low sun
    d.ellipse([90, 560, 430, 900], fill=(255, 205, 110, 255))
    # skyline silhouettes
    for (x, wdt, hgt) in [(0, 120, 300), (110, 90, 380), (200, 140, 260), (330, 80, 330),
                          (405, 120, 240), (520, 95, 360), (610, 130, 280), (735, 85, 320)]:
        d.rectangle([x, 905 - hgt, x + wdt, 905], fill=(30, 12, 52, 255))
    for wx in range(30, 780, 67):  # a few lit windows
        for wy in (640, 720, 800):
            if (wx * 7 + wy) % 3 == 0:
                d.rectangle([wx, wy, wx + 12, wy + 16], fill=(255, 190, 90, 160))
    palm(d, 60, 905, 330, lean=1)
    # flat retro cloud bands in the empty sky
    for (cx0, cy0, ln) in [(180, 330, 300), (700, 285, 380), (430, 415, 240)]:
        d.rounded_rectangle([cx0, cy0, cx0 + ln, cy0 + 16], radius=8, fill=(255, 130, 190, 55))
        d.rounded_rectangle([cx0 + 40, cy0 + 26, cx0 + ln - 30, cy0 + 40], radius=7,
                            fill=(255, 130, 190, 38))
    # ground
    d.rectangle([0, 905, W, H], fill=DARK)
    d.rectangle([0, 905, W, 922], fill=(64, 34, 84, 255))

    # game store on the right
    d.rectangle([905, 430, 1200, 905], fill=(26, 10, 44, 255))
    d.rectangle([905, 430, 1200, 470], fill=(16, 6, 28, 255))
    # neon sign
    d.rounded_rectangle([922, 486, 1184, 606], radius=18, outline=(255, 79, 163, 255), width=7)
    text(d, (1053, 532), "GTA VI", 62, (255, 255, 255, 255))
    text(d, (1053, 580), "OUT NOW", 30, (94, 234, 212, 255))
    # glowing door
    d.rectangle([985, 690, 1095, 905], fill=(255, 176, 92, 255))
    d.rectangle([985, 690, 1095, 905], outline=(16, 6, 28, 255), width=6)
    d.line([(1040, 690), (1040, 905)], fill=(16, 6, 28, 255), width=5)

    base = 1005  # queue baseline (on the pavement, below store step)
    # the queue: fans aging in line, left (2013) to right (today)
    person(d, 105, base, 300, cap=True)                    # kid with cap
    person(d, 285, base, 400)                              # young adult
    person(d, 470, base, 415, grey=True)                   # greying adult
    person(d, 655, base, 360, hunched=True, cane=True, beard=True)  # grandpa
    # the ghost, next in line at the door, coin in hand
    paste_ghost(sky, 880, base, 330)

    # headline
    text(d, (600, 88), "IN LINE SINCE 2013", 96, (255, 255, 255, 255),
         stroke=8, stroke_fill=(10, 2, 20, 255))
    text(d, (600, 178), "for GTA VI", 54, (255, 214, 120, 255),
         stroke=6, stroke_fill=(10, 2, 20, 255))

    # bottom banner
    d.rectangle([0, 1052, W, H], fill=(14, 5, 26, 255))
    d.rectangle([0, 1052, W, 1058], fill=(255, 79, 163, 255))
    text(d, (600, 1098), "meanwhile, my AI agent", 50, (255, 255, 255, 255))
    text(d, (600, 1158), "got paid on make.fun", 58, (255, 79, 163, 255))
    sky.convert("RGB").save(os.path.join(HERE, "candidate1.png"))
    print("candidate1.png written")


def candidate2():
    sky = gradient(W, H, [(0.0, (10, 8, 40)), (0.55, (38, 16, 84)),
                          (0.85, (90, 30, 120)), (1.0, (120, 40, 130))]).convert("RGBA")
    d = ImageDraw.Draw(sky)
    # stars
    for i in range(90):
        x = (i * 173) % W
        y = (i * 97) % 420
        d.ellipse([x, y, x + 4, y + 4], fill=(255, 255, 255, 200))
    # skyline + palms
    for (x, wdt, hgt) in [(0, 150, 260), (140, 100, 340), (240, 130, 220), (840, 110, 300),
                          (945, 140, 240), (1080, 120, 330)]:
        d.rectangle([x, 880 - hgt, x + wdt, 880], fill=(16, 8, 34, 255))
    palm(d, 120, 890, 330)
    palm(d, 1090, 890, 300, lean=-1)
    d.rectangle([0, 880, W, H], fill=(12, 6, 24, 255))
    # neon sign top centre
    d.rounded_rectangle([330, 120, 870, 235], radius=20, outline=(94, 234, 212, 255), width=7)
    text(d, (600, 165), "GTA VI", 74, (255, 255, 255, 255))
    text(d, (600, 214), "OUT NOW", 30, (255, 79, 163, 255))

    # ghost centre stage, big
    paste_ghost(sky, 600, 905, 470)
    # game case in front of the ghost, tilted
    case = Image.new("RGBA", (210, 280), (0, 0, 0, 0))
    cd = ImageDraw.Draw(case)
    cd.rounded_rectangle([4, 4, 206, 276], radius=10, fill=(24, 10, 40, 255),
                         outline=(255, 255, 255, 255), width=5)
    cd.rectangle([4, 4, 206, 90], fill=(200, 28, 131, 255))
    text(cd, (105, 48), "GTA VI", 40, (255, 255, 255, 255))
    text(cd, (105, 160), "LAUNCH", 30, (255, 214, 120, 255))
    text(cd, (105, 200), "DAY", 30, (255, 214, 120, 255))
    text(cd, (105, 248), "$", 34, (94, 234, 212, 255))
    case = case.rotate(10, expand=True, resample=Image.BICUBIC)
    sky.alpha_composite(case, (352, 640))

    text(d, (600, 62), "13 YEARS LATER...", 72, (255, 255, 255, 255),
         stroke=7, stroke_fill=(10, 2, 20, 255))
    # bottom banner
    d.rectangle([0, 1052, W, H], fill=(14, 5, 26, 255))
    d.rectangle([0, 1052, W, 1058], fill=(255, 79, 163, 255))
    text(d, (600, 1098), "my copy? paid for by my AI agent's", 46, (255, 255, 255, 255))
    text(d, (600, 1158), "make.fun bounties", 58, (255, 79, 163, 255))
    sky.convert("RGB").save(os.path.join(HERE, "candidate2.png"))
    print("candidate2.png written")


if __name__ == "__main__":
    candidate1()
    candidate2()
