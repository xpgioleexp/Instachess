import math, os, struct, subprocess, sys, wave
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
FONTS = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

BLACK = (11, 11, 11)
GOLD = (212, 175, 55)
PAPER = (245, 241, 230)
STONE = (185, 177, 160)
BODY = (216, 209, 194)
LIGHT = (234, 219, 184)
DARK = (156, 122, 69)
INK = (20, 20, 20)

ANTON = os.path.join(FONTS, 'Anton-Regular.ttf')
INTER_B = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
INTER_SB = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
INTER_M = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
DEJAVU = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

GLYPH = {'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'}
FILES = 'abcdefgh'

def sq_xy(name, bx, by, s):
    return bx + FILES.index(name[0]) * s, by + (8 - int(name[1])) * s

def draw_piece(d, pc, cx, cy, s, alpha=255):
    f = font(DEJAVU, int(s * 0.82))
    white = pc.isupper()
    fill = (255, 255, 255) if white else INK
    d.text((cx, cy), GLYPH[pc.lower()], font=f, fill=fill, anchor='mm',
           stroke_width=max(2, int(s * 0.03)) if white else 0, stroke_fill=INK)

def draw_board(img, pos, bx, by, s, rings=(), coords=True, skip=()):
    d = ImageDraw.Draw(img)
    for r in range(8, 0, -1):
        for i in range(8):
            n = FILES[i] + str(r)
            x, y = sq_xy(n, bx, by, s)
            dark = (i + r) % 2 == 1
            d.rectangle([x, y, x + s - 1, y + s - 1], fill=DARK if dark else LIGHT)
    for n, w in rings:
        x, y = sq_xy(n, bx, by, s)
        d.rectangle([x, y, x + s - 1, y + s - 1], outline=GOLD, width=w)
    for n, pc in pos.items():
        if n in skip:
            continue
        x, y = sq_xy(n, bx, by, s)
        draw_piece(d, pc, x + s / 2, y + s / 2 + s * 0.02, s)
    if coords:
        cf = font(INTER_M, int(s * 0.24))
        for i in range(8):
            d.text((bx + i * s + s / 2, by + 8 * s + s * 0.28), FILES[i], font=cf, fill=STONE, anchor='mm')
        for r in range(8):
            d.text((bx - s * 0.28, by + r * s + s / 2), str(8 - r), font=cf, fill=STONE, anchor='mm')
    return d

def arrow(d, a, b, bx, by, s, t=1.0, width=None):
    x1, y1 = sq_xy(a, bx, by, s); x1 += s / 2; y1 += s / 2
    x2, y2 = sq_xy(b, bx, by, s); x2 += s / 2; y2 += s / 2
    w = width or int(s * 0.16)
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    head = s * 0.42
    end = (L - s * 0.12) * t
    shaft = max(0, end - head * 0.8)
    sx, sy = x1 + ux * shaft, y1 + uy * shaft
    d.line([(x1, y1), (sx, sy)], fill=GOLD, width=w)
    d.ellipse([x1 - w / 2, y1 - w / 2, x1 + w / 2, y1 + w / 2], fill=GOLD)
    if t > 0.05:
        tx, ty = x1 + ux * end, y1 + uy * end
        px, py = -uy, ux
        bxp, byp = tx - ux * head, ty - uy * head
        d.polygon([(tx, ty), (bxp + px * head * 0.55, byp + py * head * 0.55), (bxp - px * head * 0.55, byp - py * head * 0.55)], fill=GOLD)

def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def fade_color(c, a, bg=BLACK):
    a = max(0.0, min(1.0, a))
    return tuple(int(bg[i] + (c[i] - bg[i]) * a) for i in range(3))

# ---------------- Profile pictures ----------------
def pfp_knight():
    S = 1080
    img = Image.new('RGB', (S, S), BLACK)
    d = ImageDraw.Draw(img)
    d.text((S / 2 + 14, S / 2 + 26), GLYPH['n'], font=font(DEJAVU, 900), fill=GOLD, anchor='mm')
    img.save(os.path.join(OUT, 'pfp-gold-knight.png'))
    img.resize((220, 220), Image.LANCZOS).save(os.path.join(OUT, 'preview-small-knight.png'))

def pfp_board():
    S = 1080
    img = Image.new('RGB', (S, S), BLACK)
    d = ImageDraw.Draw(img)
    s = 340
    x0, y0 = (S - 2 * s) // 2, (S - 2 * s) // 2
    for r in range(2):
        for c in range(2):
            col = LIGHT if (r + c) % 2 == 0 else DARK
            d.rectangle([x0 + c * s, y0 + r * s, x0 + (c + 1) * s - 1, y0 + (r + 1) * s - 1], fill=col)
    d.rectangle([x0 - 14, y0 - 14, x0 + 2 * s + 13, y0 + 2 * s + 13], outline=GOLD, width=14)
    d.text((S / 2 + 6, S / 2 + 18), GLYPH['n'], font=font(DEJAVU, 640), fill=BLACK, anchor='mm',
           stroke_width=0)
    img.save(os.path.join(OUT, 'pfp-board-knight.png'))

pfp_knight()
pfp_board()

# ---------------- Reel ----------------
W, H, FPS = 1080, 1920, 30
DUR = 17.0
N = int(DUR * FPS)

P = {'g1': 'K', 'e1': 'R', 'c3': 'N', 'a2': 'P', 'b3': 'P', 'c2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P',
     'g8': 'k', 'd4': 'r', 'c6': 'n', 'a7': 'p', 'b7': 'p', 'f7': 'p', 'g7': 'p', 'h7': 'p'}
S = 104
BX = (W - 8 * S) // 2 + 6
BY = 560

T_COUNT = 2.6        # countdown starts
T_ANSWER = 7.6       # answer reveal
T_MOVE_END = 8.6
T_LINES = [9.4, 10.8, 12.2]
T_CTA = 14.6

lines = [
    ('Check.', 'The rook hits the king on rank 8.'),
    ('No escape.', 'Its own pawns block f7, g7, h7.'),
    ('No defense.', 'Nothing can take or block the rook.'),
]

def text_center(d, y, s, f, c):
    d.text((W / 2, y), s, font=f, fill=c, anchor='mm')

def frame(i):
    t = i / FPS
    img = Image.new('RGB', (W, H), BLACK)
    d = ImageDraw.Draw(img)

    # header (stays above Reels top UI)
    d.text((80, 250), 'Puzzle Tuesday', font=font(INTER_SB, 36), fill=STONE, anchor='lm')
    d.text((W - 80, 250), 'Easy', font=font(INTER_SB, 36), fill=STONE, anchor='rm')

    # board + piece state
    pos = dict(P)
    moving = None
    if t >= T_ANSWER:
        k = ease((t - T_ANSWER) / (T_MOVE_END - T_ANSWER))
        x1, y1 = sq_xy('e1', BX, BY, S); x2, y2 = sq_xy('e8', BX, BY, S)
        moving = (x1 + (x2 - x1) * k, y1 + (y2 - y1) * k)
        del pos['e1']
    rings = []
    if t >= T_MOVE_END:
        pulse = 0.5 + 0.5 * math.sin((t - T_MOVE_END) * 5)
        rings = [('g8', int(8 + 6 * pulse))]
    draw_board(img, pos, BX, BY, S, rings=rings)
    d = ImageDraw.Draw(img)
    if moving:
        if t >= T_ANSWER + 0.1:
            pass
        draw_piece(d, 'R', moving[0] + S / 2, moving[1] + S / 2 + S * 0.02, S)

    # title / explanation zone (y 330..500)
    if t < T_ANSWER:
        a = ease(t / 0.5)
        text_center(d, 360, 'MATE IN ONE', font(ANTON, 132), fade_color(PAPER, a))
        text_center(d, 470, 'White to play. Can you find it?', font(INTER_SB, 44), fade_color(BODY, a))
    elif t < T_CTA:
        a = ease((t - T_ANSWER) / 0.4)
        d.text((W / 2, 360), 'Re8 is mate', font=font(ANTON, 132), fill=fade_color(GOLD, a), anchor='mm')
        text_center(d, 470, 'The back-rank mate', font(INTER_SB, 44), fade_color(BODY, a))
    else:
        a = ease((t - T_CTA) / 0.4)
        text_center(d, 360, 'GOT IT?', font(ANTON, 132), fade_color(PAPER, a))
        text_center(d, 470, 'Comment how fast you saw it', font(INTER_SB, 44), fade_color(BODY, a))

    # arrow after the move lands
    if t >= T_MOVE_END - 0.2 and t < T_CTA + 2:
        k = ease((t - (T_MOVE_END - 0.2)) / 0.5)
        arrow(d, 'e8', 'g8', BX, BY, S, t=k)

    # below board zone (y ~1440..1640), clear of caption area
    yb = BY + 8 * S + 90
    if T_COUNT <= t < T_ANSWER:
        n = 5 - int(t - T_COUNT)
        frac = (t - T_COUNT) % 1.0
        scale = 1.0 + 0.25 * (1 - ease(frac / 0.25))
        text_center(d, yb + 40, str(n), font(ANTON, int(150 * scale)), GOLD)
        # progress bar
        total = (t - T_COUNT) / (T_ANSWER - T_COUNT)
        bw = 760
        x0 = (W - bw) / 2
        d.rounded_rectangle([x0, yb + 150, x0 + bw, yb + 162], radius=6, fill=(46, 42, 36))
        d.rounded_rectangle([x0, yb + 150, x0 + bw * (1 - total), yb + 162], radius=6, fill=GOLD)
    elif t < T_COUNT:
        a = ease((t - 0.8) / 0.5)
        text_center(d, yb + 40, 'Timer starts now', font(INTER_SB, 44), fade_color(STONE, a))
    elif t < T_CTA:
        for j, (b, rest) in enumerate(lines):
            if t >= T_LINES[j]:
                a = ease((t - T_LINES[j]) / 0.35)
                y = yb + j * 64
                fb = font(INTER_B, 40); fr = font(INTER_M, 40)
                wb = d.textlength(b + ' ', font=fb)
                wr = d.textlength(rest, font=fr)
                x = (W - wb - wr) / 2
                d.text((x, y), b + ' ', font=fb, fill=fade_color(PAPER, a), anchor='lm')
                d.text((x + wb, y), rest, font=fr, fill=fade_color(BODY, a), anchor='lm')
    else:
        a = ease((t - T_CTA) / 0.4)
        text_center(d, yb + 20, 'New puzzle every Tuesday', font(INTER_B, 46), fade_color(PAPER, a))
        text_center(d, yb + 90, 'Follow so you don’t miss the next one', font(INTER_M, 40), fade_color(STONE, a))

    # global fade in / out
    if t < 0.3 or t > DUR - 0.4:
        a = ease(t / 0.3) if t < 0.3 else ease((DUR - t) / 0.4)
        img = Image.blend(Image.new('RGB', (W, H), BLACK), img, a)
    return img

# audio: ticks during countdown, a chime at the reveal
SR = 44100
samples = [0.0] * int(DUR * SR)
def add_tone(start, dur, freqs, vol, decay):
    s0 = int(start * SR)
    for k in range(int(dur * SR)):
        if s0 + k >= len(samples):
            break
        tt = k / SR
        env = math.exp(-tt * decay)
        samples[s0 + k] += vol * env * sum(math.sin(2 * math.pi * f * tt) for f in freqs) / len(freqs)
for k in range(5):
    add_tone(T_COUNT + k, 0.08, [1500], 0.35, 60)
add_tone(T_ANSWER, 1.4, [659.25, 987.77], 0.32, 3)
add_tone(T_MOVE_END, 0.25, [220], 0.4, 18)
wav = os.path.join(OUT, 'sfx.wav')
with wave.open(wav, 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, x)) * 32000)) for x in samples))

mp4 = os.path.join(OUT, 'puzzle-reel.mp4')
proc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                         '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', wav,
                         '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium',
                         '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', mp4],
                        stdin=subprocess.PIPE)
for i in range(N):
    im = frame(i)
    proc.stdin.write(im.tobytes())
    if i in (int(1.5 * FPS), int(4 * FPS), int(9.0 * FPS), int(13.5 * FPS), int(15.5 * FPS)):
        im.save(os.path.join(OUT, f'check-{i:03d}.png'))
proc.stdin.close()
proc.wait()
print('done', proc.returncode)
