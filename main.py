import numpy as np

# board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
#          [6, 0, 0, 1, 9, 5, 0, 0, 0],
#          [0, 9, 8, 0, 0, 0, 0, 6, 0],
#          [8, 0, 0, 0, 6, 0, 0, 0, 3],
#          [4, 0, 0, 8, 0, 3, 0, 0, 1],
#          [7, 0, 0, 0, 2, 0, 0, 0, 6],
#          [0, 6, 0, 0, 0, 0, 2, 8, 0],
#          [0, 0, 0, 4, 1, 9, 0, 0, 5],
#          [0, 0, 0, 0, 8, 0, 0, 7, 9]]

board = [[0, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 3, 0, 2, 0, 0, 0],
         [0, 0, 9, 0, 0, 0, 3, 0, 0],
         [0, 2, 0, 0, 0, 0, 0, 4, 0],
         [3, 0, 0, 0, 0, 0, 0, 0, 5],
         [0, 4, 0, 0, 0, 0, 0, 6, 0],
         [0, 0, 4, 0, 0, 0, 7, 0, 0],
         [0, 0, 0, 1, 0, 8, 0, 0, 0],
         [0, 0, 0, 0, 9, 0, 0, 0, 0]]


# returns true if n can be placed in row r
# false if n is already in row r
def constraint_row(r, n):
    global board
    for c in range(9):
        if board[r][c] == n:
            return False
    return True

# returns true if n can be placed in column c
# false if n is already in column c
def constraint_column(c, n):
    global board
    for r in range(9):
        if board[r][c] == n:
            return False
    return True


# returns true if n can be placed in box b
# false if n is already in box b
def constraint_box(x, y, n):
    global board
    bx = (x // 3) * 3
    by = (y // 3) * 3
    for r in range(3):
        for c in range(3):
            if board[by + r][bx + c] == n:
                return False
    return True

def constraint_chess_knight(x, y, n):
    global board
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

def possible(x, y, n):
    if not constraint_row(y, n):
        return False

    if not constraint_column(x, n):
        return False

    if not constraint_box(x, y, n):
        return False

    if not constraint_chess_knight(x, y, n):
        return False

    return True


def solve():
    global board
    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                for n in range(1, 10):
                    if possible(x, y, n):
                        board[y][x] = n
                        solve()
                        board[y][x] = 0
                return
    print(np.matrix(board))
    input('More?')


if __name__ == "__main__":
    solve()
