import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
S = 1080
BLACK = (11, 11, 11); GOLD = (212, 175, 55); PAPER = (245, 241, 230)
img = Image.new('RGB', (S, S), BLACK)
d = ImageDraw.Draw(img)

# pawn
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 760)
cx = S / 2
d.text((cx, 660), '♟', font=f, fill=PAPER, anchor='mm')
bbox = d.textbbox((cx, 660), '♟', font=f, anchor='mm')
top = bbox[1]

# crown sitting just above the pawn's head
w, band = 360, 60
base_y = top + 52
x0, x1 = cx - w / 2, cx + w / 2
spike = 150
pts = [(x0, base_y), (x0, base_y - band - 40), (x0 + w * 0.25, base_y - band - 6),
       (cx, base_y - band - spike), (x0 + w * 0.75, base_y - band - 6),
       (x1, base_y - band - 40), (x1, base_y)]
d.polygon(pts, fill=GOLD)
r = 24
for (px, py) in [(x0, base_y - band - 40), (cx, base_y - band - spike), (x1, base_y - band - 40)]:
    d.ellipse([px - r, py - r, px + r, py + r], fill=GOLD)
d.rectangle([x0, base_y - band + 6, x1, base_y], fill=GOLD)
d.line([(x0 + 18, base_y - band + 2), (x1 - 18, base_y - band + 2)], fill=BLACK, width=8)

img.save(OUT + '/pfp-pawn-to-king.png')
im = img.resize((160, 160), Image.LANCZOS)
m = Image.new('L', (160, 160), 0); ImageDraw.Draw(m).ellipse([0, 0, 159, 159], fill=255)
bg = Image.new('RGB', (180, 180), (255, 255, 255)); bg.paste(im, (10, 10), m)
full = img.copy(); mk = Image.new('L', (S, S), 0); ImageDraw.Draw(mk).ellipse([0, 0, S - 1, S - 1], fill=255)
circ = Image.new('RGB', (S, S), (255, 255, 255)); circ.paste(full, (0, 0), mk)
sheet = Image.new('RGB', (540 + 200, 540), (255, 255, 255))
sheet.paste(circ.resize((540, 540), Image.LANCZOS), (0, 0)); sheet.paste(bg, (560, 180))
sheet.save(OUT + '/preview-pawn-to-king.png')
