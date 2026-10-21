"""Shared full-width board slide (896px board, cburnett pieces, outlined gold arrows).

board_slide(d) returns a .dc.html slide. d keys: file, title, head, upper, meta,
n, total, pos ({square: piece}, uppercase = White), ring (squares), arrows
([(from, to, dashed)]), label (alt text), lines ([(bold lead or None, text)]),
and optionally size (headline px, default 86). The slide expects a pieces/
folder next to it.
"""
import json

START = {f + '1': p for f, p in zip('abcdefgh', 'RNBQKBNR')}
START.update({f + '2': 'P' for f in 'abcdefgh'})
START.update({f + '7': 'p' for f in 'abcdefgh'})
START.update({f + '8': p for f, p in zip('abcdefgh', 'rnbqkbnr')})

def after(pos, moves):
    """Plays (from, to) square pairs on a copy of pos. No castling or en passant."""
    p = dict(pos)
    for a, b in moves:
        p[b] = p.pop(a)
    return p

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>%(title)s</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>
body{margin:0}
</style>
</helmet>
"""

# One square of the big board: piece image, gold ring, and the coordinate labels drawn inside the edge squares.
SQUARE = """<sc-for list="{{squares}}" as="sq" hint-placeholder-count="64">
<div style="position: relative; width: %(s)dpx; height: %(s)dpx; background: {{sq.bg}}; box-shadow: {{sq.ring}}">
<div aria-hidden="true" style="position: absolute; left: 7px; top: 4px; font-size: 19px; font-weight: 700; color: {{sq.co}}">{{sq.rank}}</div>
<div aria-hidden="true" style="position: absolute; right: 7px; bottom: 3px; font-size: 19px; font-weight: 700; color: {{sq.co}}">{{sq.file}}</div>
</div>
</sc-for>"""

# Pieces sit in their own grid above the arrows, so an arrow never hides a piece.
PIECES = """<div style="position: absolute; inset: 0; display: grid; grid-template-columns: repeat(8, %(s)dpx); pointer-events: none">
<sc-for list="{{squares}}" as="sq" hint-placeholder-count="64"><div style="position: relative; width: %(s)dpx; height: %(s)dpx"><sc-if value="{{sq.img}}"><img src="{{sq.img}}" alt="" style="position: absolute; inset: 0; width: 100%%; height: 100%%"></sc-if></div></sc-for>
</div>"""

BOARD_SLIDE = """<div style="width: 1080px; height: 1350px; box-sizing: border-box; padding: 44px 92px 40px; background: #0B0B0B; color: #F5F1E6; font-family: Inter, sans-serif; display: flex; flex-direction: column; gap: 24px">
<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 24px">
<h2 style="margin: 0; font-family: Anton, sans-serif; font-weight: 400; font-size: %(size)dpx; line-height: 1; letter-spacing: 1px%(upper)s">%(head)s</h2>
<div style="font-size: 26px; font-weight: 600; color: #B9B1A0; white-space: nowrap">%(meta)s</div>
</div>
<div role="img" aria-label="%(label)s" style="position: relative; width: 896px; height: 896px; display: grid; grid-template-columns: repeat(8, 112px); flex-shrink: 0; border-radius: 4px; overflow: hidden">
%(squares)s
%(arrows)s%(pieces)s
</div>
<div style="display: flex; flex-direction: column; gap: 10px">
%(lines)s
</div>
<div style="flex: 1"></div>
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 26px; font-weight: 600; color: #B9B1A0">
<div>@pawn.to.king.chess</div>
<div style="display: flex; align-items: center; gap: 18px">%(n)d / %(total)d<svg aria-hidden="true" width="44" height="28" viewBox="0 0 44 28" fill="none" stroke="currentColor" stroke-width="3.5"><path d="M2 14h38M28 3l12 11-12 11"></path></svg></div>
</div>
</div>
</x-dc>
"""

# Arrows are drawn twice: a dark outline pass under all of them, then the gold pass,
# so they read on the light squares and two arrows from one square don't cut each other.
ARROWS = """<svg aria-hidden="true" width="896" height="896" viewBox="0 0 896 896" style="position: absolute; left: 0; top: 0; pointer-events: none"><g stroke="#141414" stroke-opacity="0.75" stroke-linecap="round" stroke-linejoin="round" fill="#141414" fill-opacity="0.75">%(outline)s</g><g stroke="#D4AF37" stroke-linecap="round" stroke-linejoin="round" fill="#D4AF37">%(gold)s</g></svg>
"""

SCRIPT = """<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":1080,"height":1350}}'>
class Component extends DCLogic {
squares(pos, hl, s) {
var f = 'abcdefgh', out = [];
for (var r = 8; r >= 1; r--) {
for (var i = 0; i < 8; i++) {
var n = f[i] + r, dark = (i + r) %% 2 === 1, pc = pos[n], img = '';
if (pc) img = './pieces/' + (pc === pc.toUpperCase() ? 'w' : 'b') + pc.toUpperCase() + '.svg';
out.push({ img: img, bg: dark ? '#9C7A45' : '#EADBB8', co: dark ? '#EADBB8' : '#9C7A45', rank: i === 0 ? String(r) : '', file: r === 1 ? f[i] : '', ring: hl.indexOf(n) >= 0 ? 'inset 0 0 0 8px #D4AF37' : 'none' });
}
}
return out;
}
arrow(a, b, s) {
var f = 'abcdefgh', x1 = f.indexOf(a[0]) * s + s / 2, y1 = (8 - Number(a[1])) * s + s / 2, x2 = f.indexOf(b[0]) * s + s / 2, y2 = (8 - Number(b[1])) * s + s / 2;
var dx = x2 - x1, dy = y2 - y1, L = Math.sqrt(dx * dx + dy * dy), ux = dx / L, uy = dy / L;
var tip = L - s * 0.26, base = tip - s * 0.5, w = s * 0.32;
var tx = x1 + ux * tip, ty = y1 + uy * tip, bx = x1 + ux * base, by = y1 + uy * base;
var pt = function (x, y) { return x.toFixed(1) + ',' + y.toFixed(1); };
return { shaft: 'M' + x1 + ' ' + y1 + 'L' + pt(bx + ux * 4, by + uy * 4).replace(',', ' '), head: pt(tx, ty) + ' ' + pt(bx - uy * w, by + ux * w) + ' ' + pt(bx + uy * w, by - ux * w) };
}
renderVals() {
var p = %(pos)s;
return { squares: this.squares(p, %(ring)s, 112)%(arrowvals)s };
}
}
</script>
</body>
</html>
"""

def board_slide(d):
    outline, gold, vals = [], [], []
    for i, (a, b, dashed) in enumerate(d['arrows'], 1):
        dash = ' stroke-dasharray="1 40"' if dashed else ''
        outline.append('<path d="{{a%d.shaft}}" stroke-width="38" fill="none"%s></path><polygon points="{{a%d.head}}" stroke-width="12"></polygon>' % (i, dash, i))
        gold.append('<path d="{{a%d.shaft}}" stroke-width="28" fill="none"%s></path><polygon points="{{a%d.head}}" stroke-width="2"></polygon>' % (i, dash, i))
        vals.append(", a%d: this.arrow('%s', '%s', 112)" % (i, a, b))
    lines = []
    for lead, body in d['lines']:
        if lead:
            lines.append('<p style="margin: 0; font-size: 33px; line-height: 1.34; color: #D8D1C2; max-width: 896px"><b style="color: #F5F1E6">%s</b> %s</p>' % (lead, body))
        else:
            lines.append('<p style="margin: 0; font-size: 28px; line-height: 1.34; color: #B9B1A0; max-width: 896px">%s</p>' % body)
    html = HEAD % d + BOARD_SLIDE % dict(
        upper='; text-transform: uppercase' if d['upper'] else '', head=d['head'], meta=d['meta'], label=d['label'], n=d['n'], total=d['total'], size=d.get('size', 86),
        squares=SQUARE % {'s': 112}, pieces=PIECES % {'s': 112}, arrows=ARROWS % {'outline': ''.join(outline), 'gold': ''.join(gold)} if gold else '',
        lines='\n'.join(lines))
    html += SCRIPT % dict(pos=json.dumps(d['pos']), ring=json.dumps(d['ring']), arrowvals=''.join(vals))
    return html

