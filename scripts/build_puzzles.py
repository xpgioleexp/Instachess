"""Writes the board slides of the puzzles carousel (source/puzzles/*.dc.html).

The board fills the slide width (896px, 112px squares) and uses the cburnett
piece set in source/puzzles/pieces/. Close.dc.html is hand-written and left alone.
Run: python3 scripts/build_puzzles.py, then scripts/export.py puzzles.
"""
import json, os
from board_slide import HEAD, after, board_slide

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'source', 'puzzles')

P1 = {'g1': 'K', 'e1': 'R', 'c3': 'N', 'a2': 'P', 'b3': 'P', 'c2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P', 'g8': 'k', 'd4': 'r', 'c6': 'n', 'a7': 'p', 'b7': 'p', 'f7': 'p', 'g7': 'p', 'h7': 'p'}
P2 = {'g1': 'K', 'e1': 'R', 'd5': 'N', 'a2': 'P', 'b2': 'P', 'c2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P', 'g8': 'k', 'c6': 'q', 'f8': 'r', 'c8': 'b', 'a7': 'p', 'b7': 'p', 'f7': 'p', 'g7': 'p', 'h7': 'p'}
P3 = {'g1': 'K', 'c4': 'Q', 'h6': 'N', 'c1': 'B', 'a1': 'R', 'f1': 'R', 'a2': 'P', 'b2': 'P', 'c3': 'P', 'e4': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P', 'h8': 'k', 'd8': 'q', 'f8': 'r', 'a8': 'r', 'c8': 'b', 'a7': 'p', 'b7': 'p', 'c6': 'p', 'e5': 'p', 'g7': 'p', 'h7': 'p'}

A1 = after(P1, [('e1', 'e8')])
A2 = after(P2, [('d5', 'e7')])
A3 = after(P3, [('c4', 'g8'), ('f8', 'g8'), ('h6', 'f7')])

# Each answer paragraph: (bold lead, body); the last line is the lesson, in stone.
SLIDES = [
    dict(file='P1', title='Puzzle 1', head='Mate in one', upper=True, meta='Puzzle 1, easy', n=2, pos=P1, ring=[], arrows=[],
         label='Puzzle 1, White to play: White rook on e1, Black king on g8 behind pawns on f7, g7 and h7',
         lines=[('White to play.', "One move ends the game. Where can Black's king run? Comment your answer, then swipe.")]),
    dict(file='A1', title='Answer 1', head='Re8 is mate', upper=False, meta='Answer 1', n=3, pos=A1, ring=['g8'], arrows=[('e1', 'e8', False)],
         label='Answer: the rook moves from e1 to e8 and checks the king on g8 along the back rank',
         lines=[('Back-rank mate.', "The rook checks on e8. Black's own pawns trap the king, and nothing can block or take."),
                (None, 'Lesson: give your king an exit early, with a move like h6.')]),
    dict(file='P2', title='Puzzle 2', head='Win the queen', upper=True, meta='Puzzle 2, medium', n=4, pos=P2, ring=[], arrows=[],
         label='Puzzle 2, White to play: White knight on d5 is attacked by the Black queen on c6; Black king on g8',
         lines=[('White to play.', "Black's queen attacks your knight. Don't retreat it: one knight move saves it and wins the queen.")]),
    dict(file='A2', title='Answer 2', head='Ne7+ forks', upper=False, meta='Answer 2', n=5, pos=A2, ring=['e7'], arrows=[('e7', 'g8', False), ('e7', 'c6', False)],
         label='Answer: the knight jumps to e7, checking the king on g8 and attacking the queen on c6',
         lines=[('Two targets.', 'The knight checks the king and hits the queen. The king must move, then Nxc6.'),
                (None, 'Lesson: answer a threat with a bigger threat.')]),
    dict(file='P3', title='Puzzle 3', head='Mate in two', upper=True, meta='Puzzle 3, hard', n=6, pos=P3, ring=[], arrows=[],
         label='Puzzle 3, White to play: White queen on c4 and knight on h6, Black king on h8 with a rook on f8 and pawns on g7 and h7',
         lines=[('White to play.', "Black's king is boxed into the corner. Hint: the winning first move gives away your queen.")]),
    dict(file='A3', title='Answer 3', head='Qg8+! then Nf7#', upper=False, meta='Answer 3', n=7, pos=A3, ring=['h8'], arrows=[('c4', 'g8', True), ('h6', 'f7', False)],
         label='Final position: the queen was sacrificed on g8 and taken by the rook; the knight jumped from h6 to f7 and mates the king on h8',
         lines=[('1.Qg8+ Rxg8', 'is forced, because the knight guards g8. 2.Nf7# and the king is smothered by its own pieces.'),
                (None, 'Lesson: a sacrifice works when every reply is forced.')]),
]

# Cover: the three puzzle positions as thumbnails, same piece set.
MINI = """<div style="display: flex; flex-direction: column; gap: 16px">
<div role="img" aria-label="Puzzle %(i)d preview" style="display: grid; grid-template-columns: repeat(8, 37px); width: 296px; border-radius: 3px; overflow: hidden">
<sc-for list="{{b%(i)d}}" as="sq" hint-placeholder-count="64"><div style="position: relative; width: 37px; height: 37px; background: {{sq.bg}}"><sc-if value="{{sq.img}}"><img src="{{sq.img}}" alt="" style="position: absolute; inset: 0; width: 100%%; height: 100%%"></sc-if></div></sc-for>
</div>
<div style="font-size: 30px; font-weight: 700">%(name)s</div>
<div style="font-size: 26px; color: #B9B1A0; margin-top: -8px">%(task)s</div>
</div>"""

COVER = """<div style="width: 1080px; height: 1350px; box-sizing: border-box; padding: 64px 72px 48px; background: #0B0B0B; color: #F5F1E6; font-family: Inter, sans-serif; display: flex; flex-direction: column; gap: 40px">
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 26px; font-weight: 600; color: #B9B1A0">
<div>Puzzle Tuesday</div>
<div>1 / 8</div>
</div>
<div style="flex: 1"></div>
<h1 style="margin: 0; font-family: Anton, sans-serif; font-weight: 400; font-size: 150px; line-height: 0.94; text-transform: uppercase; letter-spacing: 1px">Can you<br>solve all 3?</h1>
<p style="margin: 0; font-size: 38px; line-height: 1.35; color: #D8D1C2; max-width: 880px">Easy, medium, hard. Each answer is on the slide right after its puzzle, so solve before you swipe.</p>
<div style="display: flex; justify-content: space-between; margin-top: 12px">
%(minis)s
</div>
<div style="flex: 1"></div>
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 26px; font-weight: 600; color: #B9B1A0">
<div>@pawn.to.king.chess</div>
<div style="display: flex; align-items: center; gap: 14px; color: #F5F1E6">Swipe<svg aria-hidden="true" width="44" height="28" viewBox="0 0 44 28" fill="none" stroke="currentColor" stroke-width="3.5"><path d="M2 14h38M28 3l12 11-12 11"></path></svg></div>
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":1080,"height":1350}}'>
class Component extends DCLogic {
squares(pos) {
var f = 'abcdefgh', out = [];
for (var r = 8; r >= 1; r--) {
for (var i = 0; i < 8; i++) {
var n = f[i] + r, dark = (i + r) %% 2 === 1, pc = pos[n], img = '';
if (pc) img = './pieces/' + (pc === pc.toUpperCase() ? 'w' : 'b') + pc.toUpperCase() + '.svg';
out.push({ img: img, bg: dark ? '#9C7A45' : '#EADBB8' });
}
}
return out;
}
renderVals() {
return { b1: this.squares(%(p1)s), b2: this.squares(%(p2)s), b3: this.squares(%(p3)s) };
}
}
</script>
</body>
</html>
"""

def cover():
    minis = '\n'.join(MINI % dict(i=i, name=n, task=t) for i, n, t in [(1, '1. Easy', 'Mate in one'), (2, '2. Medium', 'Win the queen'), (3, '3. Hard', 'Mate in two')])
    return HEAD % {'title': 'Cover'} + COVER % dict(minis=minis, p1=json.dumps(P1), p2=json.dumps(P2), p3=json.dumps(P3))

if __name__ == '__main__':
    open(os.path.join(OUT, 'Main.dc.html'), 'w').write(cover())
    for d in SLIDES:
        open(os.path.join(OUT, d['file'] + '.dc.html'), 'w').write(board_slide(dict(d, total=8)))
    print('wrote', 1 + len(SLIDES), 'slides')
