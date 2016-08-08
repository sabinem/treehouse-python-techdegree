"""
This file contains the Board Class. Each Player has his own board.
On the board the status of the game is recorded. The ships on the
opponents board are hidden until they take a hit.
"""
from collections import OrderedDict


VERTICALLY = 'vertically'
HORIZONTALLY = 'horizontally'
BOARD_SIZE = 10
BOARD_VERTICAL_SHIP = '|'
BOARD_HORIZONTAL_SHIP = '-'
BOARD_EMPTY = 'O'
BOARD_MISS = '.'
BOARD_HIT = '*'
BOARD_SUNK = '#'
BOARD_HIT_CHOICES = [BOARD_HIT, BOARD_MISS, BOARD_SUNK]
BOARD_UNHIT_CHOICES = [BOARD_EMPTY, BOARD_HORIZONTAL_SHIP, BOARD_VERTICAL_SHIP]
BOARD_HIDDEN = [BOARD_VERTICAL_SHIP, BOARD_HORIZONTAL_SHIP]
ROWS = [str(num) for num in range(1, BOARD_SIZE+1)]
COLS = [letter for letter in 'ABCDEDFGHIJ']
GRID = [(x, y) for x in COLS for y in ROWS]


def board_value_view(value, hide_ships=False):
    """
    Eventually hides the ships when preparing the board for print.
    """
    if value in BOARD_HIDDEN and hide_ships:
        return BOARD_EMPTY
    else:
        return value


class Board:
    """
    This is the board class. It is implemented as an ordered dictionary
     on a grid of rows and columns.
    """
    def __init__(self):
        """
        The boards dictionary is initialized with the value of '0'
        on each grid point.
        """
        self.board_dict = OrderedDict({key: value for key
                                       in [p for p in GRID]
                                       for value in [BOARD_EMPTY]})

    def row_to_string(self, row_nr, hide_ships=False):
        """
        This function builds a string out of the values
        of the board dictionary for a given row.
        """
        row_dict = {key: board_value_view(value, hide_ships)
                    for key, value in self.board_dict.items()
                    if key[1] == row_nr}
        row = OrderedDict(sorted(row_dict.items(), key=lambda t: t[0][0]))
        return ''.join(row.values())

    def board_as_list_of_row_strings(self, hide_ships=False):
        """
        The boards dictionaries values are taken and transformed
        as a list of strings.
        There is one string for each row.
        """
        return [self.row_to_string(row_nr, hide_ships) for row_nr in ROWS]

    def print(self, hide_ships=False):
        """
        This method prints the board to the screen.
        Eventually ships, that have not been hit yet are hidden.
        """
        print("   " + " "
              .join([chr(c) for c in range(ord('A'), ord('A') + BOARD_SIZE)]))
        row_num = 1
        for row_string in self.board_as_list_of_row_strings(hide_ships):
            print(str(row_num).rjust(2) + " " + (" ".join(row_string)))
            row_num += 1

    def set_ship(self, ship, point):
        """
        This method sets up a ship on the board, starting at the given point.
        The direction of the setup may be vertically or horizontally.
        """
        col, row = point
        shipgridpoints = []
        for idx in range(0, ship.length):
            if ship.direction == HORIZONTALLY:
                nextcol = chr(ord(col) + idx)
                nextpoint = (nextcol, row)
            else:
                nextrow = str(int(row) + idx)
                nextpoint = (col, nextrow)
            if nextpoint in GRID and self.board_dict[nextpoint] == BOARD_EMPTY:
                shipgridpoints.append(nextpoint)
            elif nextpoint not in GRID:
                raise OverflowError(
                    'Ship does not fit on the board that way!'
                    ' {} is not on board'
                    .format(nextpoint))
            else:
                raise ValueError(
                    'Conflict with another ship: {} is already occupied.'
                    .format(nextpoint))
        for point in shipgridpoints:
            self.board_dict[point] = ship.marker
        return shipgridpoints

    def set_board_value_miss(self, point):
        """
        This method marks a miss on the board, for a point that was attacked.
        """
        self.board_dict[point] = BOARD_MISS
