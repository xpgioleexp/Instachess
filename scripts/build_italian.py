"""Writes the board slides of the Italian Game carousel (source/italian-game/*.dc.html).

Mistakes.dc.html and Close.dc.html have no board and are hand-written.
Run: python3 scripts/build_italian.py, then scripts/export.py italian-game.
"""
import os
from board_slide import START, after, board_slide

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'source', 'italian-game')

ITALIAN = after(START, [('e2', 'e4'), ('e7', 'e5'), ('g1', 'f3'), ('b8', 'c6'), ('f1', 'c4')])
PLAN = after(ITALIAN, [('f8', 'c5'), ('c2', 'c3'), ('g8', 'f6'), ('d2', 'd4')])
TRAP = after(ITALIAN, [('g8', 'f6'), ('f3', 'g5'), ('d7', 'd5'), ('e4', 'd5'), ('f6', 'd5'), ('g5', 'f7')])
# 3...Nd4 4.Nxe5? Qg5 5.Nxf7 Qxg2 6.Rf1 Qxe4+ 7.Be2, Black to play
PUZZLE = after(ITALIAN, [('c6', 'd4'), ('f3', 'e5'), ('d8', 'g5'), ('e5', 'f7'), ('g5', 'g2'), ('h1', 'f1'), ('g2', 'e4'), ('c4', 'e2')])
ANSWER = after(PUZZLE, [('d4', 'f3')])

SLIDES = [
    dict(file='Main', title='Cover', head='The Italian Game', upper=True, size=100, meta='in 8 slides', n=1, pos=ITALIAN, ring=['c4', 'f7'], arrows=[('c4', 'f7', False)],
         label='Board after 1.e4 e5 2.Nf3 Nc6 3.Bc4, a gold arrow runs from the bishop on c4 to f7',
         lines=[('Openings, explained.', 'Three moves, one target, a trap, and a puzzle to test yourself.')]),
    dict(file='Moves', title='The moves', head='Three moves', upper=True, meta='The Italian Game', n=2, pos=ITALIAN, ring=['e4'], arrows=[('f3', 'e5', False), ('c4', 'f7', False)],
         label='Board after 1.e4 e5 2.Nf3 Nc6 3.Bc4: arrows show the knight on f3 attacking e5 and the bishop on c4 aiming at f7',
         lines=[('1.e4 e5 2.Nf3 Nc6 3.Bc4', 'e4 grabs the center, the knight hits e5, and the bishop lines up on f7.')]),
    dict(file='Target', title='The target', head='Aim at f7', upper=True, meta='The Italian Game', n=3, pos=ITALIAN, ring=['f7'], arrows=[('c4', 'f7', False)],
         label='Board after 3.Bc4 with f7 ringed in gold and an arrow from the bishop on c4 to f7',
         lines=[('Why f7?', "Only Black's king defends it. Add a knight or queen to the attack and that's where the game breaks open.")]),
    dict(file='Plan', title='The plan', head='Own the center', upper=True, meta='The Italian Game', n=4, pos=PLAN, ring=['c3', 'd4'], arrows=[('d4', 'e5', False), ('d4', 'c5', False)],
         label='Board after 3...Bc5 4.c3 Nf6 5.d4: the pawn on d4 attacks e5 and the bishop on c5, backed by the pawn on c3',
         lines=[('3...Bc5 4.c3 Nf6 5.d4', 'c3 prepares d4, which hits e5 and the bishop at once. If Black takes, take back with the pawn, then castle.')]),
    dict(file='Trap', title='The trap', head='The Fried Liver', upper=True, meta='The Italian Game', n=5, pos=TRAP, ring=['f7'], arrows=[('f7', 'd8', False), ('f7', 'h8', False)],
         label='Board after 6.Nxf7: the White knight on f7 attacks the Black queen on d8 and the rook on h8',
         lines=[('3...Nf6 4.Ng5 d5 5.exd5 Nxd5 6.Nxf7', 'forks queen and rook. After 6...Kxf7 7.Qf3+ the king is stuck in the open.'),
                (None, 'Playing Black? Answer 5.exd5 with 5...Na5.')]),
    dict(file='Puzzle', title='Puzzle', head='Your turn', upper=True, meta='Puzzle', n=6, pos=PUZZLE, ring=[], arrows=[],
         label='Puzzle position, Black to play: Black queen on e4 gives check, White has just blocked with the bishop on e2; Black knight on d4',
         lines=[('Black to play, mate in one.', 'White grabbed a pawn on move 4 and kept grabbing. Find the move that ends it, then swipe.')]),
    dict(file='Answer', title='Puzzle answer', head='...Nf3 is mate', upper=False, meta='Answer', n=7, pos=ANSWER, ring=['e1', 'e2'], arrows=[('d4', 'f3', False), ('e4', 'e1', True)],
         label='Answer: the knight jumps from d4 to f3 with check; the bishop on e2 cannot take it because the queen on e4 pins it to the king on e1',
         lines=[('Check, and no way out.', "The bishop on e2 can't take: the queen pins it to the king. d1, d2, f1 and f2 are all blocked."),
                (None, "Lesson: after 3...Nd4, don't take on e5. Play 4.Nxd4 or castle.")]),
]

if __name__ == '__main__':
    for d in SLIDES:
        open(os.path.join(OUT, d['file'] + '.dc.html'), 'w').write(board_slide(dict(d, total=9)))
    print('wrote', len(SLIDES), 'slides')
