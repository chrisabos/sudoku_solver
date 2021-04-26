# sudoku_solver

simple sudoku solver using recursive backtracking

(aka. very slow and not optimized)

## How to use:
```
python3 main.py
```

The program will prompt the user for a game file name. "classic" is one provided but the text input corresponds to a json file in the games directory

## Implemented constraints:
These constraints are can be optionally selected using the game file. See games/killer_thermometer.json for an example

Normal sudoku constraints:
- Each row contains the digits 1-9
- Each column contains the digits 1-9
- Each box contains the digits 1-9

Chess sudoku constraints:
- Knights move constraint - The same number cannot exists where, if it were a chess knight, it could move to
- Kings move constraint - The same number cannot exist where, if it were a chess king, it could move

Sum area constraint
This is an abstract implementation of the boxes present in "killer sudoku." These defined areas have a sum and a list of cells, where the numbers in the cells have to add to equal the sum

Thermometers constraint
The defined thermometers have to have increasing numbers along the thermometer starting at the "bulb" or the start of the list

Consecutive Orthogonally Adjacent constraint
This is a common constraint found in sudoku puzzles where cells directly adjacent to the top, bottom, left, or right of a cell cannot be a consecutive digit to itself
