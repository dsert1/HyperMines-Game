#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""
# @author Deniz Sert
# @version Start: February 29, 2020

# NO IMPORTS ALLOWED!

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION
def look_around(num_rows, num_cols, board):
    '''
    This function takes in the number rows, columns and the board; returns a new board with the updated bombs.
    '''
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == 0:
                neighbor_bombs = 0

                for i in range(-1, 2): #if statement refactors
                    for j in range(-1, 2):

                        if 0 <= r+i < num_rows:
                            if 0 <= c+j < num_cols:
                                if board[r+i][c+j] == '.':
                                    neighbor_bombs += 1

                board[r][c] = neighbor_bombs
    return board

def build_mask_and_board(num_rows, num_cols, bombs):
    '''
    Builds the mask and the board.
    '''
    board = []
    mask = []

    for r in range(num_rows):
        row = {'board': [], 'mask': []}
        for c in range(num_cols):
            row['mask'].append(False)

            if [r, c] in bombs or (r, c) in bombs:
                row['board'].append('.')

            else:
                row['board'].append(0)
        board.append(row['board'])
        mask.append(row['mask'])
    return board, mask


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """
    return new_game_nd((num_rows, num_cols), bombs)

def in_bounds(_game, row, col):
    '''Checks if the elements are in bounds.'''
    counter = 0
    if _game['board'][row][col] == 0:
        num_rows, num_cols = _game['dimensions']

        # REFACTOR ed
        for i in range(-1, 2):  # if statement refactors
            for j in range(-1, 2):
                if 0 <= row + i < num_rows:  # helper func
                    if 0 <= col + j < num_cols:
                        if _game['board'][row + i][col + j] != '.':
                            if _game['mask'][row + i][col + j] == False:
                                counter+=dig_2d(_game, row+i, col+j)
    return counter
def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """
    return dig_nd(game, (row, col))


def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, xray)




def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """

    res = ''
    rendered_game = render_2d(game, xray)
    for i in range(len(rendered_game)):
        if i != len(rendered_game)-1:
            res += ''.join(rendered_game[i]) + "\n"
        else:
            res += ''.join(rendered_game[i])

    return res



# N-D IMPLEMENTATION

#***HELPER ND's******
def get_nd_value(array, coord_tup): # (0, 0, 0, 0)
    '''
    Given an N-D array and a tuple of coordinates, returns the value at those coordinates in the array
    >>> get_nd_value([[[0, 1, 0], [69, 0, 1], [71, 37, 6]], [[2, 7, 0], [45, 0, 8], [71, 9, 6]]], (0, 2, 2))
    6
    '''

    if len(coord_tup) == 1: #base case
        return array[coord_tup[0]]
    else: #recursive
        return get_nd_value(array[coord_tup[0]], coord_tup[1:])

def set_nd_value(array, coord_tup, value):
    '''
    Given an N-D array, a tuple of coordinates, and a value; sets the value at that coordinate to the passed in value.
    >>> set_nd_value([[[0, 1, 0], [69, 0, 1], [71, 37, 6]], [[2, 7, 0], [45, 0, 8], [71, 9, 6]]], (0, 2, 2), 5) is None
    True
    '''
    if len(coord_tup) == 1: #base case
        array[coord_tup[0]] = value
    else: #recursive
        set_nd_value(array[coord_tup[0]], coord_tup[1:], value)

def create_nd_array(dimension_list, value):
    '''Given dimension list and a value; creates a new N-D array with those dimensions where each value in the array is the given value.
    >>> create_nd_array((2, 2, 2), 5)
    [[[5, 5], [5, 5]], [[5, 5], [5, 5]]]

    '''
    if len(dimension_list) == 1:
        return [value for i in range(dimension_list[0])]
    else:
        return [create_nd_array(dimension_list[1:], value) for i in range(dimension_list[0])]

def get_game_state(game):
    '''
    Given a game; returns the game state ('ongoing', 'defeat', or 'victory')
    >>> get_game_state({'board': [[[0, 0], [1, 1], [1, 1]], [[0, 0], [1, 1], ['.', 1]], [[0, 0], [1, 1], [1, 1]]],  'dimensions': (3, 3, 2), 'mask': [[[False, False], [False, False], [False, False]], [[False, False], [False, False], [False, False]], [[False, False], [False, False], [False, False]]], 'state': 'ongoing'})
    'ongoing'
    '''

    x = get_all_possible_coords(game['dimensions'])
    done = True
    for i in x:
        if get_nd_value(game['mask'], i) and get_nd_value(game['board'], i) == '.':
            return 'defeat'
        if not (get_nd_value(game['mask'], i) or get_nd_value(game['board'], i) == '.'):
            done = False
            break
    if done:
        return 'victory'
    return 'ongoing'





def get_neighbors(cood, dim):
    '''
    Given coordinates, and dimensions; yields all neighbors of the given coordinates.
    # >>> list(get_neighbors({'board': [[[0, 0], [1, 1], [1, 1]], [[0, 0], [1, 1], ['.', 1]], [[0, 0], [1, 1], [1, 1]]],  'dimensions': (3, 3, 2), 'mask': [[[False, False], [False, False], [False, False]], [[False, False], [False, False], [False, False]], [[False, False], [False, False], [False, False]]], 'state': 'ongoing'}, (1, 2, 0)))

    >>> list(get_neighbors((1,), (3,)))
    [(0,), (1,), (2,)]

    >>> list(get_neighbors((1, 2, 0), (3, 3, 2)))
    [(0, 1, 0), (1, 1, 0), (2, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0), (0, 1, 1), (1, 1, 1), (2, 1, 1), (0, 2, 1), (1, 2, 1), (2, 2, 1)]
    '''


    if len(cood) == 1: #base case
        for z in range(-1, 2):
            num = cood[0] + z
            if 0 <= num< dim[0]: #check if in bounds
                yield (num,)
    else: #recursive
        my_neighbor_list = get_neighbors(cood[1:], dim[1:])
        for sq in my_neighbor_list:
            for z in range(-1, 2):
                num = cood[0] + z
                if 0 <= num < dim[0]: #check if in bounds
                    yield (num,) + sq

def get_all_possible_coords(dim):
    '''
    Given a game, yields all possible coordinates

    >>> list(get_all_possible_coords((2, 2)))
    [(0, 0), (1, 0), (0, 1), (1, 1)]

    '''


    if len(dim) == 1: #base case
        for i in range(dim[0]):
            yield (i,)


    else:
        x = get_all_possible_coords(dim[1:])
        for sq in x:
            for i in range(dim[0]): #loop thru last dimensios
                yield (i,) + sq





#*****BEGIN GAME*******
def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """
    board = create_nd_array(dimensions, 0)  # board of all zeros
    mask = create_nd_array(dimensions, False) #mask

    for b in bombs:
        set_nd_value(board, b, '.')
        for neighbor in get_neighbors(b, dimensions): #loop thru the bombs
            if get_nd_value(board, neighbor) != '.':
                set_nd_value(board, neighbor, get_nd_value(board, neighbor) + 1)

    return {
        'dimensions': dimensions,
        'board': board,
        'mask': mask,
        'state': 'ongoing'}


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coords (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """
    if get_nd_value(game['mask'], coordinates):
        return 0
    revealed_sq = 0

    val = get_nd_value(game['board'], coordinates)
    if val == '.':  # bomb case
        set_nd_value(game['mask'], coordinates, True)
        game['state'] = 'defeat'
        return 1

    if not game['state'] == 'ongoing':
        return 0

    if val != 0:  # if not a bomb and not zero
        set_nd_value(game['mask'], coordinates, True)
        revealed_sq += 1
        if get_game_state(game) == 'victory':
            game['state'] = 'victory'




    #recursive case
    else:
        set_nd_value(game['mask'], coordinates, True)
        revealed_sq+=1

        neighbors = get_neighbors(coordinates, game['dimensions'])
        for n in neighbors:
            revealed_sq+=dig_nd(game, n)

        if get_game_state(game) == 'victory':
            game['state'] = 'victory'


    return revealed_sq



def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """

    new_board = create_nd_array(game['dimensions'], 0)
    for x in get_all_possible_coords(game['dimensions']):

        elt = get_nd_value(game['board'], x)
        elt_tf = get_nd_value(game['mask'], x)

        if elt_tf or xray:
            if elt == 0:
                set_nd_value(new_board, x, ' ')
            elif elt == '.':
                set_nd_value(new_board, x, '.')
            else:
                set_nd_value(new_board, x, str(elt))
        else:
            set_nd_value(new_board, x, '_')



    return new_board













if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    doctest.run_docstring_examples(dig_2d, globals(), optionflags=_doctest_flags, verbose=False)

    # ********RENDER 2D TESTS*******
    # g = {'dimensions': (2, 4),
    #        'state': 'ongoing',
    #     'board': [['.', 3, 1, 0],
    #             ['.', '.', 1, 0]],
    #     'mask': [[False, True, True, False],
    #             [False, False, True, False]]}
    # game = {'dimensions': (2, 4),
    #             'state': 'ongoing',
    #                'board': [['.', 3, 1, 0],
    #                        ['.', '.', 1, 0]],
    #                'mask':  [[True, True, True, False],
    #                         [False, False, True, False]]}
    # print("MY PRINT\n\n\n\n\n", render_2d(g))

    #**********RENDER ASCII TESTS**********
    # expected = ('        \n'
    #             '     111\n'
    #             '    12__\n'
    #             '12122___\n'
    #             '________\n'
    #             '________\n'
    #             '________\n'
    #             '________\n'
    #             '________\n'
    #             '________')
    # # print("EXPECTED: \n", render_2d(game))
    # #
    # #
    # # print("\n\n\nRESULT: \n", render_ascii(game))
    # # print(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    #
    # #********REFACTOR DIG2D TEST*******
    # game = {'dimensions': (2, 4),
    #             'board': [['.', 3, 1, 0],
    #                               ['.', '.', 1, 0]],
    #
    # 'mask': [[False, True, False, False],
    #          [False, False, False, False]],
    #
    # 'state': 'ongoing'}
    #
    # print(dig_2d(game, 0, 3))


    # print(get_neighbors({'board': [(4,), (5,), (6,)], 'dimensions': (3,), 'mask': [False, False, False], 'state': 'ongoing'}, (1,)))

    # [print(x) for x in get_neighbors((1, 1, 1), (3, 3, 3))]


