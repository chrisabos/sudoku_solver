import numpy as np
import json

# board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
#          [6, 0, 0, 1, 9, 5, 0, 0, 0],
#          [0, 9, 8, 0, 0, 0, 0, 6, 0],
#          [8, 0, 0, 0, 6, 0, 0, 0, 3],
#          [4, 0, 0, 8, 0, 3, 0, 0, 1],
#          [7, 0, 0, 0, 2, 0, 0, 0, 6],
#          [0, 6, 0, 0, 0, 0, 2, 8, 0],
#          [0, 0, 0, 4, 1, 9, 0, 0, 5],
#          [0, 0, 0, 0, 8, 0, 0, 7, 9]]

game = {
    # the board is represented as a list of lists containing the number at that location in the grid
    # 0 means the location is not filled
    "board": [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 4, 0, 0, 0, 0],
              [0, 0, 3, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]],

    # each thermometer is represented as a list of tuples where the first tuple is the bulb
    # this is a list of thermometers
    "thermometers": [[(2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3)],
                     [(4, 2), (3, 2)],
                     [(4, 2), (5, 2)],
                     [(4, 2), (4, 3), (4, 4), (4, 5)],
                     [(7, 5), (6, 5), (6, 6), (6, 7), (6, 8), (7, 8), (8, 8)],
                     [(7, 5), (8, 5)]],

    # sum_areas is a list of distionanies
    "sum_areas": [{
        "sum": 10,
        "locations": [(0, 0), (0, 1)],
    },
    {
        "sum": 10,
        "locations": [(1, 0), (1, 1)],
    },
    {
        "sum": 10,
        "locations": [(0, 3), (1, 3)],
    },
    {
        "sum": 10,
        "locations": [(5, 3), (5, 4)],
    },
    {
        "sum": 10,
        "locations": [(7, 3), (7, 4)],
    },
    {
        "sum": 10,
        "locations": [(8, 3), (8, 4)],
    },
    {
        "sum": 10,
        "locations": [(0, 4), (1, 4)],
    },
    {
        "sum": 10,
        "locations": [(4, 5), (5, 5)],
    },
    {
        "sum": 10,
        "locations": [(8, 6), (8, 7)],
    },
    {
        "sum": 10,
        "locations": [(2, 7), (2, 8)],
    },
    {
        "sum": 10,
        "locations": [(3, 7), (4, 7)],
    }],

    "constraints": {
        "sudoku_row": True,
        "sudoku_column": True,
        "sudoku_box": True,
        "chess_knight": True,
        "thermometers": True
    }
}

i = 0


# returns true if n can be placed in row r
# false if n is already in row r
def constraint_row(board, r, n):
    for c in range(9):
        if board[r][c] == n:
            return False
    return True

# returns true if n can be placed in column c
# false if n is already in column c
def constraint_column(board, c, n):
    for r in range(9):
        if board[r][c] == n:
            return False
    return True


# returns true if n can be placed in box b
# false if n is already in box b
def constraint_box(board, x, y, n):
    bx = (x // 3) * 3
    by = (y // 3) * 3
    for r in range(3):
        for c in range(3):
            if board[by + r][bx + c] == n:
                return False
    return True


# returns true if n can be placed at x,y in the board breaking the chess knights rule
# false if n is a knights move away
def constraint_chess_knight(board, x, y, n):
    for r in range(9):
        for c in range(9):
            distance = abs(r - y) + abs(c - x)
            if not distance == 3:
                continue
            if r == y:
                continue
            if c == x:
                continue
            if board[r][c] == n:
                return False
    return True


# returns true if n can be placed at x,y in the board without breaking the chess king rule
# false if n is a kings move away
def constraint_chess_king(board, x, y, n):
    for r in range(3):
        for c in range(3):

            #   x x x
            #   x K x   we can skip 1, 1 because this represents the current
            #   x x x   location as illustrated here
            if r == 1 and c == 1:
                continue

            lx = x+c-1 # location x and y are the current location we are evaluating in the board
            ly = y+r-1
            if lx < 0 or lx > 8 or ly < 0 or ly > 8:
                continue

            # check surrounding square
            if board[ly][lx] == n:
                return False

    # if we didnt find a reason to fail, it succeeds
    return True


# returns true if n can be placed at x,y in the board without breaking the thermometer rule
# false if placing n at x,y breaks a thermometer
# thermometer sudoku is where there is a line on the sudoku board, and the numbers on the line
# can only grow as they get further from the start (aka the bulb) of the thermometer
def constraint_thermometer(game, x, y, n):
    board = game.get('board')
    thermometers = game.get('thermometers')

    if not isinstance(thermometers, list):
        return True

    # search over all the thermometers
    for t in thermometers:

        # check if x, y exists on this thermometer
        found = False
        for pos in t:
            if pos[0] == x and pos[1] == y:
                found = True
                break

        # this x,y was not found on this thermometer,
        # so check the next thermomemter
        if not found:
            continue

        before = True # this keeps track if out current pos is before the given x,y along the thermometer
        for pos in t:
            if pos[0] == x and pos[1] == y:
                before = False
                continue

            # if this position on the board is empty, skip this one
            if board[pos[1]][pos[0]] == 0:
                continue

            if before:
                if n <= board[pos[1]][pos[0]]:
                    return False
            else:
                if n >= board[pos[1]][pos[0]]:
                    return False

    # we havent failed, so we good?
    return True


# returns true if the x,y cell is not consecutive to the orthogonally adjacent cells
# returns false if at least 1 neighbor cell is consecutive to n
def constraint_consecutive_orthogonally_adjacent(game, x, y, n):
    board = game.get('board')

    # check that we arent at the border of the board
    if x > 0:
        # check if the difference between the adjacent cell and x,y cell is 1
        if not board[y][x - 1] == 0:
            if abs(board[y][x - 1] - n) == 1:
                # if so return false
                return False
    if x < 8:
        if not board[y][x + 1] == 0:
            if abs(board[y][x + 1] - n) == 1:
                return False
    if y > 0:
        if not board[y - 1][x] == 0:
            if abs(board[y - 1][x] - n) == 1:
                return False
    if y < 8:
        if not board[y + 1][x] == 0:
            if abs(board[y + 1][x] - n) == 1:
                return False

    # none of the adjacent test failed, so we pass
    return True


def constraint_sum_areas(game, x, y, n):
    board = game.get('board')
    sum_areas = game.get('sum_areas')

    for sa in sum_areas:
        sa_sum = sa.get('sum')
        sa_locs = sa.get('locations')

        # check if x, y exists on this sum_area
        found = False
        for pos in sa_locs:
            if pos[0] == x and pos[1] == y:
                found = True
                break

        if not found:
            continue

        # iterate over all the positions in the sum_area
        sum = 0
        exact = True # if all the locations in the sum_area are filled in, then the sum needs to be exact
        for pos in sa_locs:
            if pos[0] == x and pos[1] == y:
                sum += n
                continue

            bval = board[pos[1]][pos[0]]

            # if one location is not filled in, then the sum doesnt have to be exact
            if bval == 0:
                exact = False

            sum += bval

        if exact:
            return sum == sa_sum
        else:
            if sum > sa_sum:
                return False

    return True


def possible(game, x, y, n):
    board = game.get('board')
    constraints = game.get('constraints', {'sudoku_row': True, 'sudoku_column': True, 'sudoku_box': True})

    if True == constraints.get('sudoku_row', False):
        if not constraint_row(board, y, n):
            return False

    if True == constraints.get('sudoku_column', False):
        if not constraint_column(board, x, n):
            return False

    if True == constraints.get('sudoku_box', False):
        if not constraint_box(board, x, y, n):
            return False

    if True == constraints.get('chess_knight', False):
        if not constraint_chess_knight(board, x, y, n):
            return False

    if True == constraints.get('chess_king', False):
        if not constraint_chess_king(board, x, y, n):
            return False

    if True == constraints.get('thermometers', False):
        if not constraint_thermometer(game, x, y, n):
            return False

    if True == constraints.get('consecutive_orthogonally_adjacent', False):
        if not constraint_consecutive_orthogonally_adjacent(game, x, y, n):
            return False

    if True == constraints.get('sum_areas', False):
        if not constraint_sum_areas(game, x, y, n):
            return False

    return True


def solve(game):
    board = game.get('board')
    #print(np.matrix(board))
    #input('Step?')

    global i
    if i % 100000 == 0:
        print(np.matrix(board))
    i += 1

    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                for n in range(1, 10):
                    if possible(game, x, y, n):
                        board[y][x] = n
                        solve(game)
                        board[y][x] = 0
                return
    print(np.matrix(board))
    input('More?')


if __name__ == "__main__":
    game_name = input('Game name: ')

    with open(f'games/{game_name}.json', 'r') as game_file:
        game_data = json.loads(game_file.read())
        solve(game_data)
