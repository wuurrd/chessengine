#!/usr/bin/env python
# -*-coding: utf-8-*-
# Title: chessboard.py
# Author: Gribouillis
# Created: 2012-05-19 22:18:09.909216 (isoformat date)
# License: Public Domain
# Use this code freely.
version_info = (0, 1)
version = ".".join(map(str, version_info))
# some noise
pieces = u''.join(unichr(9812 + x) for x in range(12))
pieces = u' ' + pieces[:6][::-1] + pieces[6:]
allbox = u''.join(unichr(9472 + x) for x in range(200))
box = [ allbox[i] for i in (2, 0, 12, 16, 20, 24, 44, 52, 28, 36, 60) ]
(vbar, hbar, ul, ur, ll, lr, nt, st, wt, et, plus) = box
h3 = hbar * 3
# useful constant unicode strings to draw the square borders
topline = ul + (h3 + nt) * 7 + h3 + ur
midline = wt + (h3 + plus) * 7 + h3 + et
botline = ll + (h3 + st) * 7 + h3 + lr
tpl = u' {0} ' + vbar

def inter(*args):
    """Return a unicode string with a line of the chessboard.

    args are 8 integers with the values
        0 : empty square
        1, 2, 3, 4, 5, 6: white pawn, knight, bishop, rook, queen, king
        -1, -2, -3, -4, -5, -6: same black pieces
    """
    assert len(args) == 8
    return vbar + u''.join((tpl.format(pieces[a]) for a in args))
start_position = (
    [
        (-4, -2, -3, -5, -6, -3, -2, -4),
        (-1,) * 8,
    ] +
    [ (0,) * 8 ] * 4 +
    [
        (1,) * 8,
        (4, 2, 3, 5, 6, 3, 2, 4),
    ]
)
def _game(position):
    yield topline
    yield inter(*position[0])
    for row in position[1:]:
        yield midline
        yield inter(*row)
    yield botline
draw_board = lambda squares: "\n".join(_game(squares))
draw_board.__doc__ = """Return the chessboard as a string for a given position.
    position is a list of 8 lists or tuples of length 8 containing integers
"""
if __name__ == "__main__":
    print draw_board(start_position)
