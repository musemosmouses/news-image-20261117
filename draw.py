"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Deterministic: no clock, no random, no network. Run twice, same bytes.
News used (17 Nov 2026, as reported): Kerch/Crimea bridge struck again;
tankers hit near Hormuz, third US carrier arrives, Iran drones at a US
radar in Bahrain intercepted; Xi/Trump/Putin three-way meeting confirmed
for 19 Nov in Shenzhen; Pentagon audit fails 9th year; Japan scrambles
jets; Depardieu pleads guilty. No unconfirmed allegation is stated.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 36
PAPER = (247, 242, 231)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (16, 42, 78)
SEA = (18, 68, 96)
CREAM = (250, 240, 220)
WHITE = (255, 255, 255)
LIGHT = (214, 226, 238)
GREY = (120, 120, 116)
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y


def smoke(draw, cx, cy, scale):
    for dx, dy, r in [(-38, 6, 26), (-8, -14, 32), (26, 2, 24), (52, -10, 18)]:
        r = int(r * scale)
        draw.ellipse([cx + dx * scale - r, cy + dy * scale - r,
                      cx + dx * scale + r, cy + dy * scale + r],
                     fill=(200, 200, 196))


def bridge_scene(draw, x0, y0, x1, y1):
    # Sea, then a road bridge with a collapsed middle span and smoke.
    draw.rectangle([x0, y0, x1, y1], fill=(23, 58, 96))
    for wy in range(y0 + 108, y1, 22):
        for wx in range(x0 + 20, x1 - 40, 90):
            draw.arc([wx, wy, wx + 56, wy + 12], 0, 180, fill=(90, 140, 180), width=3)
    deck_y = y0 + 62
    # Intact deck left and right, gap in the middle where the span fell.
    draw.rectangle([x0, deck_y, x0 + 330, deck_y + 14], fill=(232, 228, 218))
    draw.rectangle([x0 + 560, deck_y, x1, deck_y + 14], fill=(232, 228, 218))
    # Fallen span, tilted down into the water.
    draw.polygon([(x0 + 350, deck_y + 8), (x0 + 540, deck_y + 8),
                  (x0 + 520, deck_y + 52), (x0 + 370, deck_y + 52)],
                 fill=(200, 194, 182))
    for tx in (x0 + 130, x0 + 700):
        draw.rectangle([tx, y0 + 6, tx + 12, deck_y + 14], fill=(232, 228, 218))
        draw.line([tx + 6, y0 + 6, x0 + 330, deck_y], fill=(180, 180, 172), width=2)
        draw.line([tx + 6, y0 + 6, x0 + 560, deck_y], fill=(180, 180, 172), width=2)
    smoke(draw, x0 + 445, y0 + 30, 1.0)
    draw.ellipse([x0 + 420, y0 + 18, x0 + 470, y0 + 48], fill=(240, 150, 40))
    draw.ellipse([x0 + 432, y0 + 26, x0 + 458, y0 + 44], fill=(250, 210, 80))


def tanker_scene(draw, x0, y0, x1, y1):
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(14, 52, 84))
    for wy in range(y0 + h - 18, y1, 16):
        for wx in range(x0 + 12, x1 - 30, 70):
            draw.arc([wx, wy, wx + 44, wy + 10], 0, 180, fill=(80, 130, 170), width=3)
    # Tanker hull, deck and funnel, with fire and smoke amidships.
    deck = y0 + h - 42
    draw.polygon([(x0 + 30, deck), (x1 - 30, deck),
                  (x1 - 70, y1 - 6), (x0 + 70, y1 - 6)], fill=(30, 30, 34))
    draw.rectangle([x0 + 30, deck - 12, x1 - 30, deck], fill=(178, 34, 34))
    draw.rectangle([x0 + 300, deck - 34, x0 + 330, deck - 12], fill=(240, 230, 210))
    smoke(draw, x0 + 200, deck - 30, 0.45)
    draw.polygon([(x0 + 180, deck - 12), (x0 + 200, deck - 38),
                  (x0 + 220, deck - 12)], fill=(240, 150, 40))
    draw.polygon([(x0 + 192, deck - 12), (x0 + 202, deck - 28),
                  (x0 + 212, deck - 12)], fill=(250, 210, 80))


def flag(draw, x, y, w, h, kind):
    if kind == "china":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        for sx, sy in [(14, 12), (34, 18), (34, 34), (14, 40), (26, 26)]:
            draw.ellipse([x + sx, y + sy, x + sx + 8, y + sy + 8], fill=(255, 222, 0))
    elif kind == "usa":
        for i in range(7):
            draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                           fill=RED if i % 2 == 0 else WHITE)
        draw.rectangle([x, y, x + w * 0.45, y + h * 0.55], fill=(30, 50, 110))
    else:  # russia: white / blue / red horizontal bands
        draw.rectangle([x, y, x + w, y + h // 3], fill=WHITE)
        draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
        draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    # Masthead.
    serif = font("DejaVuSerif-Bold.ttf", 58)
    sans_b = font("DejaVuSans-Bold.ttf", 38)
    sans = font("DejaVuSans.ttf", 24)
    centred(d, W // 2, 30, "THE WORLD IN ONE IMAGE", serif, INK)
    d.rectangle([M, 116, W - M, 118], fill=RED)
    # Date band: the day, unmissable.
    d.rectangle([M, 128, W - M, 184], fill=RED)
    centred(d, W // 2, 138, "TUESDAY 17 NOVEMBER 2026", sans_b, WHITE)
    # Lead panel: Crimea bridge.
    d.rectangle([M, 200, W - M, 540], fill=NAVY)
    d.rectangle([M, 200, M + 210, 232], fill=RED)
    d.text((M + 14, 206), "LEAD STORY", font=font("DejaVuSans-Bold.ttf", 20), fill=WHITE)
    head = font("DejaVuSerif-Bold.ttf", 38)
    sub = font("DejaVuSans.ttf", 24)
    text_block(d, M + 20, 244, "UKRAINE HITS CRIMEA BRIDGE AGAIN",
               head, WHITE, W - 2 * M - 40, 48)
    text_block(d, M + 20, 296,
               "Second strike in 24 hours \u2014 Zelenskyy hails \u2018unprecedented "
               "operation\u2019; Russia hits Kyiv bridges, power and heating cut",
               sub, LIGHT, W - 2 * M - 40, 31)
    bridge_scene(d, M, 392, W - M, 540)
    # Second row: Hormuz (left) and Shenzhen (right).
    row_y, row_h, col_w = 556, 280, 466
    d.rectangle([M, row_y, M + col_w, row_y + row_h], fill=SEA)
    d.text((M + 16, row_y + 12), "MIDDLE EAST", font=font("DejaVuSans-Bold.ttf", 19), fill=(255, 210, 120))
    text_block(d, M + 16, row_y + 40, "TANKERS HIT NEAR HORMUZ",
               font("DejaVuSerif-Bold.ttf", 28), WHITE, col_w - 32, 32)
    text_block(d, M + 16, row_y + 108,
               "Mines / projectile disable a tanker; third US carrier "
               "arrives; Iran drones target US radar in Bahrain \u2014 "
               "intercepted, no casualties",
               font("DejaVuSans.ttf", 19), LIGHT, col_w - 32, 23)
    tanker_scene(d, M, row_y + 186, M + col_w, row_y + row_h)
    rx = W - M - col_w
    d.rectangle([rx, row_y, rx + col_w, row_y + row_h], fill=CREAM)
    d.rectangle([rx, row_y, rx + col_w, row_y + 6], fill=RED)
    d.text((rx + 16, row_y + 12), "DIPLOMACY", font=font("DejaVuSans-Bold.ttf", 19), fill=RED)
    text_block(d, rx + 16, row_y + 40, "XI, TRUMP & PUTIN TO MEET",
               font("DejaVuSerif-Bold.ttf", 28), INK, col_w - 32, 32)
    text_block(d, rx + 16, row_y + 108,
               "First three-way summit confirmed for Thursday 19 Nov in "
               "Shenzhen, on APEC sidelines",
               font("DejaVuSans.ttf", 19), (60, 60, 60), col_w - 32, 23)
    for i, kind in enumerate(["china", "usa", "russia"]):
        flag(d, rx + 16 + i * 148, row_y + 184, 132, 66, kind)
    d.rectangle([rx + 16, row_y + 260, rx + col_w - 16, row_y + 266], fill=(150, 130, 110))
    # Bottom ticker: three more stories from the same day.
    d.rectangle([M, 852, W - M, 988], fill=INK)
    d.text((M + 16, 864), "ALSO ON 17 NOVEMBER", font=font("DejaVuSans-Bold.ttf", 19), fill=(255, 210, 120))
    items = [
        ("PENTAGON FAILS AUDIT", "9th year in a row"),
        ("JAPAN SCRAMBLES JETS", "Russian aircraft in its airspace"),
        ("DEPARDIEU PLEADS GUILTY", "Drops sexual-assault appeal"),
    ]
    for i, (label, note) in enumerate(items):
        x = M + 16 + i * 312
        d.text((x, 896), label, font=font("DejaVuSans-Bold.ttf", 20), fill=WHITE)
        text_block(d, x, 924, note, font("DejaVuSans.ttf", 19),
                   (200, 200, 200), 292, 24)
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
