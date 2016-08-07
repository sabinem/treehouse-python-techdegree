"""
This files contains some basic functions that are used by several classes
"""
from battleshipgame.board import COLS, ROWS


def clear_screen():
    """
    This method clears the screen for output,
    so that the players do not see each others hidden ships.
    """
    print("\033c", end="")


def check_input(userinput):
    """
    This method removes blanks from an input string.
    It returns the letters as a list, the string without blanks and the length of the string.
    """
    input_list = list(userinput)
    input_list = [str for str in input_list if str != ' ']
    input_string = ''.join(input_list)
    return input_list, input_string, len(input_list)


def check_gridpoint(userinput_point):
    """
    This function cleans an input-string and checks whether it is a a point on the grid.
    """
    input_list, input_string, input_length = check_input(userinput_point.upper())
    if input_length < 2 or input_length > 3:
        raise TypeError("Two parameter expected. {} were given!"
              .format(input_length))
    col = input_list[0]
    row = ''.join(input_list[1:])
    if col not in COLS:
        raise ValueError("{} is not a valid column."
                        .format(col))
    if row not in ROWS:
        raise ValueError("{} is not a valid row."
                        .format(row))
    return col, row