"""
This file contains the Ship Classes. Each ship type has its owm class.
"""
from .board import BOARD_HORIZONTAL_SHIP, BOARD_VERTICAL_SHIP
from .board import HORIZONTALLY, VERTICALLY
from .basic import check_gridpoint, check_input, clear_screen


class Ship:
    """
    The Ships are placed by the players on the board.
    Ships keep track of their status: they know which gridpoints
    have been uncovered so far.
    """
    length = 0
    ship_type = None
    gridpoints_unhit = []
    gridpoints_sunk = []
    direction = None
    marker = None

    def __init__(self, player, board):
        """
        The ship is set up on the board.
        """
        clear_screen()
        board.print()
        print('{}, how do you want to set up your {} of length {}?' \
              .format(player, self, self.length))
        self.get_direction()
        self.get_location(board)

    def get_direction(self):
        """
        This method gets the direction of the ship for the setup.
        It may be placed horizontally or vertically.
        """
        while True:
            userinput_direction = input('Choose: [v]vertical or [h]orizontal \n> ')
            input_list, input_string, input_length = check_input(userinput_direction)
            if input_length != 1:
                print("Only one parameter expected. {} were given!"
                      .format(input_length))
                continue
            elif input_string not in 'vh':
                print("{} is not a valid direction."
                      .format(input_string))
                continue
            if input_string == 'h':
                self.direction = HORIZONTALLY
                self.marker = BOARD_HORIZONTAL_SHIP
            else:
                self.direction = VERTICALLY
                self.marker = BOARD_VERTICAL_SHIP
            break

    def get_location(self, board):
        """
        This method gets the startpoint of the setup of the ship on the grid.
        The ship is then placed to the left or downwards and takes up gridpoints
        according to its length.
        """
        while True:
            userinput_point = input(
                "Give startcoordinates as column row to place {} {}: Example B2\n> "
                .format(self, self.direction)).upper()
            try:
                gridpoint = check_gridpoint(userinput_point)
            except (ValueError, TypeError) as error:
                print(error)
                continue
            try:
                self.gridpoints_unhit = board.set_ship(self, gridpoint)
            except (ValueError, OverflowError) as error:
                print(error)
                continue
            break

    def check_sunk(self, attack_point):
        """
        This method checks whether the current attack point sunk the ship, which is the case
        if it was the last missing hit for the ship.
        """
        if attack_point in self.gridpoints_unhit:
            self.gridpoints_unhit.remove(attack_point)
            self.gridpoints_sunk.append(attack_point)
            if self.gridpoints_unhit == []:
                return True
            else:
                return False

    def __str__(self):
        """
        The ship is represented by the ship-type when printed.
        """
        return self.ship_type


class AircraftCarrier(Ship):
    """
    Aircraft Carrier
    """
    length = 5
    ship_type = 'Aircraft Carrier'


class BattleShip(Ship):
    """
    Battle Ship
    """
    length = 2
    ship_type = 'Battleship'


class Submarine(Ship):
    """
    Submarine
    """
    length = 4
    ship_type = 'Submarine'


class Cruiser(Ship):
    """
    Cruiser
    """
    length = 4
    ship_type = 'Cruiser'


class PatrolBoat(Ship):
    """
    Patrol Boat
    """
    length = 4
    ship_type = 'Patrol Boat'


