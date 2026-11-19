#!/usr/bin/env python3
"""make.fun news-image-20261119 -- newspaper front page, 1024x768 PNG.

Pure standard library (zlib + struct). Deterministic: identical bytes on
every run, no network. Bitmap 5x7 font defined inline below.

Entry seed: hub-hub620 (drives palette / layout / headline-mix variation).
"""
import os
import struct
import zlib

W, H = 1024, 768
SEED = "hub-hub620"

# ---------------------------------------------------------------- PRNG ----
# Tiny deterministic xorshift, seeded from the entry name.
STATE = 0
for _ch in SEED:
    STATE = ((STATE * 131) + ord(_ch)) & 0xFFFFFFFF


def rnd():
    global STATE
    STATE ^= (STATE << 13) & 0xFFFFFFFF
    STATE ^= STATE >> 17
    STATE ^= (STATE << 5) & 0xFFFFFFFF
    return STATE


def ri(a, b):
    return a + rnd() % (b - a + 1)


# ------------------------------------------------------- 5x7 font ---------
# Rows are 5-bit strings, MSB = leftmost column of the 5-wide glyph.
F = {
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    'J': ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    '3': ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    '6': ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    '.': ["00000", "00000", "00000", "00000", "00000", "00100", "00100"],
    ',': ["00000", "00000", "00000", "00000", "00100", "00100", "01000"],
    ':': ["00000", "00100", "00100", "00000", "00100", "00100", "00000"],
    ';': ["00000", "00100", "00100", "00000", "00100", "00100", "01000"],
    '!': ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    '?': ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    '_': ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    "'": ["00100", "00100", "00000", "00000", "00000", "00000", "00000"],
    '"': ["01010", "01010", "00000", "00000", "00000", "00000", "00000"],
    '/': ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '&': ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    '+': ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    '=': ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    '%': ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
    '#': ["01010", "11111", "01010", "01010", "11111", "01010", "00000"],
    '$': ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    '@': ["01110", "10001", "00001", "01101", "10101", "10101", "01110"],
    '*': ["00000", "10101", "01110", "11111", "01110", "10101", "00000"],
    '<': ["00010", "00100", "01000", "10000", "01000", "00100", "00010"],
    '>': ["01000", "00100", "00010", "00001", "00010", "00100", "01000"],
    '~': ["00000", "00000", "01000", "10101", "00010", "00000", "00000"],
}

COLS = 5
ROWS = 7
GLYPH_W = COLS + 1  # 1px inter-character gap baked into advance

# ------------------------------------------------------- canvas ----------
CANVAS = [[(0, 0, 0)] * W for _ in range(H)]


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        CANVAS[y][x] = c


def rect(x, y, w, h, c):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    row = [c] * (x1 - x0)
    for yy in range(y0, y1):
        CANVAS[yy][x0:x1] = row


def rect_outline(x, y, w, h, c, t=1):
    rect(x, y, w, t, c)
    rect(x, y + h - t, w, t, c)
    rect(x, y, t, h, c)
    rect(x + w - t, y, t, h, c)


def hline(x, y, w, c):
    rect(x, y, w, 1, c)


def vline(x, y, h, c):
    rect(x, y, 1, h, c)


def glyph(ch, x, y, c, scale=1):
    g = F.get(ch)
    if g is None:
        g = F['?']
    for r in range(ROWS):
        rowb = g[r]
        yy = y + r * scale
        for col in range(COLS):
            if rowb[col] == '1':
                if scale == 1:
                    px(x + col, yy, c)
                else:
                    rect(x + col * scale, yy, scale, scale, c)


def text(s, x, y, c, scale=1, spacing=1):
    cx = x
    for ch in s:
        glyph(ch, cx, y, c, scale)
        cx += (COLS + spacing) * scale
    return cx


def textw(s, scale=1, spacing=1):
    if not s:
        return 0
    return len(s) * (COLS + spacing) * scale - spacing * scale


# ------------------------------------------------------- PNG writer ------
def chunk(tag, data):
    return (struct.pack('>I', len(data)) + tag + data +
            struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF))


def write_png(path, canvas):
    raw = bytearray()
    for row in canvas:
        raw.append(0)  # filter: none
        for (r, g, b) in row:
            raw += bytes((r, g, b))
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    png = (b'\x89PNG\r\n\x1a\n' +
           chunk(b'IHDR', ihdr) +
           chunk(b'IDAT', zlib.compress(bytes(raw), 9)) +
           chunk(b'IEND', b''))
    with open(path, 'wb') as fh:
        fh.write(png)
    return len(png)

# ------------------------------------------------------- palette ---------
INK = (26, 26, 28)
PAPER = (243, 239, 227)
FAINT = (219, 213, 195)
RULE = (94, 90, 82)
RED = (166, 46, 42)
BLUE = (36, 78, 128)
GREEN = (38, 106, 76)
GOLD = (184, 138, 44)
GREY = (126, 122, 112)
WHITE = (250, 248, 240)

ACCENTS = [RED, BLUE, GREEN, GOLD]


def wrapped(text_str, width_chars):
    words = text_str.split()
    lines, cur = [], ''
    for wd in words:
        trial = wd if not cur else cur + ' ' + wd
        if len(trial) <= width_chars or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------ content ----------
MAST = "WORLD NEWS"
DATLINE = "Thursday 19 November 2026"
ED = "No. 9,0497  *  EVENING FINAL  *  $2.50"

# (section tag, body text, accent colour, lead flag)
STORIES = [
    ("TECH / GAMING",
     "GTA VI launches worldwide today as PS5 and Xbox consoles sell out in "
     "hours; retailers report the biggest entertainment release in history",
     RED, True),
    ("MARKETS",
     "Global stocks slip as traders weigh fresh inflation data; the dollar "
     "firm while gold holds near record highs in quiet Thursday trade",
     BLUE, False),
    ("CLIMATE",
     "Delegates at the COP31 summit reach a draft deal on adaptation "
     "finance, but fossil-fuel language remains unresolved before Friday",
     GREEN, True),
    ("TECH / AI",
     "AI regulators agree on cross-border testing rules for frontier "
     "models as chipmakers post record quarterly orders",
     GOLD, False),
    ("SPORT",
     "World Cup playoff draw set up a dramatic international window; "
     "fans travel as host cities unveil final stadium plans",
     BLUE, True),
    ("WORLD",
     "Leaders gather for a one-day energy summit as winter supply talks "
     "stretch late into the night",
     GREY, False),
]

# ------------------------------------------------------- layout ----------
def draw():
    rect(0, 0, W, H, PAPER)

    # subtle halftone dot field from the seed (deterministic texture)
    dot = (231, 226, 211)
    for gy in range(0, H, 8):
        off = (gy // 8) % 2 * 4
        for gx in range(off, W, 8):
            rect(gx, gy, 1, 1, dot)

    m = 24  # margin

    # ---- masthead ------------------------------------------------------
    y = 18
    text(MAST, (W - textw(MAST, 6)) // 2, y, INK, 6)
    y = 18 + 7 * 6 + 8
    t = DATLINE
    text(t, (W - textw(t, 2)) // 2, y, RED, 2)
    y += 7 * 2 + 6
    t = ED
    text(t, (W - textw(t, 1)) // 2, y, GREY, 1)

    # double rule under masthead
    y += 7 + 8
    hline(m, y, W - 2 * m, INK)
    hline(m, y + 3, W - 2 * m, INK)
    y += 11

    # ---- edition banner strip -----------------------------------------
    strip_h = 22
    rect(m, y, W - 2 * m, strip_h, INK)
    t = "  TODAY IN THE WORLD  *  SIX STORIES THAT SHAPED THURSDAY  "
    text(t, m + (W - 2 * m - textw(t, 1)) // 2, y + 8, PAPER, 1)
    y += strip_h + 12

    # ---- headline grid -------------------------------------------------
    body_top = y
    bottom = H - 26
    gutter = 12
    col_w = (W - 2 * m - gutter) // 2

    # seed-driven asymmetric split of the 6 stories across 2 columns
    left_n = ri(2, 4)
    left_n = max(1, min(5, left_n))
    cols = [STORIES[:left_n], STORIES[left_n:]]

    for ci, stories in enumerate(cols):
        x = m + ci * (col_w + gutter)
        cy = body_top
        for si, (tag, body, accent, lead) in enumerate(stories):
            scale = 3 if lead else 2
            need = 22 + scale * 7 + 10 + 12
            if cy + need > bottom + 12:
                break
            draw_story(x, cy, col_w, tag, body, accent, lead, scale)
            cy += need + 2

    # ---- footer --------------------------------------------------------
    hline(m, H - 22, W - 2 * m, RULE)
    ft = "make.fun  *  news-image-20261119  *  hub-hub620  *  all pixels set locally"
    text(ft, (W - textw(ft, 1)) // 2, H - 16, GREY, 1)


def draw_story(x, y, w, tag, body, accent, lead, scale):
    boxh = 22 + scale * 7 + 10 + 12
    rect_outline(x, y, w, boxh, RULE, 1)
    rect(x, y, w, 3, accent)

    # kicker
    text(" " + tag + " ", x + 6, y + 7, accent, 1)

    # headline, wrapped
    inner = w - 12
    cw = (COLS + 1) * scale
    maxch = inner // cw
    lines = wrapped(body, maxch)
    hy = y + 22
    maxlines = 5 if scale == 2 else 4
    for ln in lines[:maxlines]:
        text(ln, x + 6, hy, INK, scale)
        hy += 7 * scale

    # corner index mark
    rect(x + w - 4, y + 4, 2, 2, accent)

# ------------------------------------------------------- main ------------
def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    draw()
    n = write_png(path, CANVAS)
    print(f"wrote {path} ({n} bytes)")


if __name__ == "__main__":
    main()
