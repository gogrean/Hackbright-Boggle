"""Boggle word check.

Given a 5x5 boggle board, see if you can find a given word in it.

In Boggle, you can start with any letter, then move in any NEWS direction.
You can continue to change directions, but you cannot use the exact same
tile twice.

So, for example::

    N C A N E
    O U I O P
    Z Q Z O N
    F A D P L
    E D E A Z
 
In this grid, you could find `NOON* (start at the `N` in the top
row, head south, and turn east in the third row). You cannot find
the word `CANON` --- while you can find `CANO` by starting at the
top-left `C`, you can 't re-use the exact same `N` tile on the
front row, and there's no other `N` you can reach.

For example::

    >>> board = make_board('''
    ... N C A N E
    ... O U I O P
    ... Z Q Z O N
    ... F A D P L
    ... E D E A Z
    ... ''')

`NOON` should be found (0, 3) -> (1, 3) -> (2, 3) -> (2, 4)::
 
    >>> find(board, "NOON")
    True

`NOPE` should be found (0, 3) -> (1, 3) -> (1, 4) -> (0, 4)::

    >>> find(board, "NOPE")
    True

`CANON` can't be found (`CANO` starts at (0, 1) but can't find
the last `N` and can't re-use the N)::

    >>> find(board, "CANON")
    False

You cannot travel diagonally in one move, which would be required
to find `QUINE`::

    >>> find(board, "QUINE")
    False

We can recover if we start going down a false path (start 3, 0)::

    >>> find(board, "FADED")
    True


An extra tricky case --- it needs to find the `N` toward the top right,
and then go down, left, up, up, right to find all four `O`s and the `S`::

    >>> board2 = make_board('''
    ... E D O S Z
    ... N S O N R
    ... O U O O P
    ... Z Q Z O R
    ... F A D P L
    ... ''')

    >>> find(board2, "NOOOOS")
    True
    
"""

board_size = 5

def make_board(board_string):
    """Make a board from a string.

    For example::

        >>> board = make_board('''
        ... N C A N E
        ... O U I O P
        ... Z Q Z O N
        ... F A D P L
        ... E D E A Z
        ... ''')

        >>> len(board)
        5

        >>> board[0]
        ['N', 'C', 'A', 'N', 'E']
    """

    letters = board_string.split()

    board = [
        letters[0:5],
        letters[5:10],
        letters[10:15],
        letters[15:20],
        letters[20:25],
    ]

    return board


def find_neighbors(pos):
    left_pos = (pos[0], pos[1]+1)
    right_pos = (pos[0], pos[1]-1)
    up_pos = (pos[0]-1, pos[1])
    down_pos = (pos[0]+1, pos[1])
    valid_neighbors = [p for p in [left_pos, right_pos, up_pos, down_pos] if (0 <= p[0] < board_size) and (0 <= p[1] < board_size)]
    return valid_neighbors

def reset_board():
    all_tiles = [(i,j) for i in range(5) for j in range(5)]
    return [], all_tiles

def find(board, word, available_tiles=None, current_path=[]):
    """Can word be found in board?"""
    # If there are no available tiles, it means that a new search has started,
    # either for a new word, or a search that begins at a new position on the 
    # board (looking for a new path to find the word). In this case, the 
    # available tiles are set to include all the tiles of the board, and the 
    # current path is (re)set to an empty list.
    if not available_tiles:
        current_path, available_tiles = reset_board()
    if len(word) == 1:
        if word in [board[tile[0]][tile[1]] for tile in available_tiles if tile not in current_path]:
            return True
        return False
    origin_tile = [tile for tile in available_tiles if board[tile[0]][tile[1]] == word[0] if tile not in current_path]
    if origin_tile:
        neighbors = {}
        for ot in origin_tile:
            neighbors[ot] = find_neighbors(ot)

        for ot in origin_tile:
            current_path.append(ot)
            if find(board, word[1:], available_tiles=neighbors[ot], current_path=current_path):
                return True
            current_path = []
    return False



if __name__ == '__main__':
    import doctest
    if doctest.testmod().failed == 0:
        print("\n*** ALL TESTS PASSED; YOU FOUND SUCCESS! ***\n")
