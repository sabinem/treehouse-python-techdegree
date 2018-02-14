"""
This file contains the Player Class.
"""
import sys

from board import BOARD_HIT, BOARD_HIDDEN, \
    BOARD_EMPTY, BOARD_UNHIT_CHOICES
from board import Board
from basic import clear_screen, check_gridpoint, check_input
from ship import BattleShip, PatrolBoat, Cruiser, \
    AircraftCarrier, Submarine


class Player:
    """
    The two players of the Game are instances of the player class.
    It keeps track of their ships on the board and their status.
    """
    def __init__(self, opponent=None):
        """
        This sets the name of the player and initializes
        his board and the player status.
        """
        self.name = self.get_name(opponent)
        self.board = Board()
        self.defeated = False

    def get_name(self, opponent=None):
        """
        This method gets the player's name from the user.
        A player's names should be different from each other and not blank.
        """
        while True:
            userinput_name = input('> ').strip()
            input_list, input_string, input_length \
                = check_input(userinput_name)
            if input_length == 0:
                print('Players name must not be blank!')
                continue
            try:
                if userinput_name == opponent.name:
                    print('Players must have different names. '
                          '{} is taken already by the other player'
                          .format(userinput_name))
                    continue
            except (AttributeError, NameError):
                pass
            return userinput_name

    def get_attack_point(self, opponent):
        """
        This asks the player, where he wants to attack.
        """
        while True:
            hit_location = input("{}, select a location to shoot at.\n> "
                                 .format(self))
            try:
                attack_point = check_gridpoint(hit_location)
            except (ValueError, TypeError) as error:
                print(error)
                continue
            if (opponent.board.board_dict[attack_point]
                not in BOARD_UNHIT_CHOICES):
                    print("You have attacked {} before".format(attack_point))
                    continue
            return attack_point

    def handover_control(self):
        """
        After a player's move he is asked to hand over control
        to his opponent by hitting any key.
        """
        input('{}, press Enter when you are ready to give control'
              ' to the other player.'
              .format(self.name))

    def setup_ships(self):
        """
        The player's ships are set up here. Afterward the player's board
        is printed and he is asked to hand over to his opponent.
        """
        print('Hello {}, now it is time for you to set up your battleships!'
              .format(self))
        self.board.print()
        self.ships_afloat = []
        self.ships_afloat.append(BattleShip(self, self.board))
        self.ships_afloat.append(Submarine(self, self.board))
        self.ships_afloat.append(Cruiser(self, self.board))
        self.ships_afloat.append(AircraftCarrier(self, self.board))
        self.ships_afloat.append(PatrolBoat(self, self.board))
        clear_screen()
        print("Bravo {}, you are done with your setup. It looks fantastic:"
              .format(self))
        self.board.print()
        self.handover_control()

    def perform_turn(self, opponent):
        """
        The player's turn is performed. He is shown his opponent's board
        with all that he has currently acchieved.
        He is also shown his own board with what the opponent acchieved.
        He is then promted to chose a point on the grid to attack.
        The result of the attack is evaluated and presented to him.
        If he wins, the game ends. Otherwise,
        he is asked to hand over to his opponent.
        """
        print("{}'s' board:".format(opponent.name))
        opponent.board.print(hide_ships=True)
        print("Your board:")
        self.board.print()
        attack_point = self.get_attack_point(opponent)
        clear_screen()
        opponent.point_take_hit(attack_point, self)
        opponent.board.print(hide_ships=True)
        if opponent.defeated:
            print("Congratulations, {}! You won the game!"
                  .format(self))
            print("That is what {} has guessed so far from you:"
                  .format(opponent))
            self.board.print()
            sys.exit()
        else:
            self.handover_control()

    def point_take_hit(self, attack_point, attacker):
        """
        This method takes the hit and determines
        whether it is a hit or a miss.
        """
        board_value = self.board.board_dict[attack_point]
        if board_value == BOARD_EMPTY:
            self.board.set_board_value_miss(attack_point)
            print("Sorry {}, you missed.".format(attacker))
        elif board_value in BOARD_HIDDEN:
            self.ships_take_hit(attack_point, attacker)
        else:
            raise ValueError('you already hit this point')

    def ships_take_hit(self, attack_point, attacker):
        """
        This methods evaluates a hit on the ships of the player.
        """
        print("Gratulation {}, this is a hit:".format(attacker))
        for ship in self.ships_afloat:
            if attack_point in ship.gridpoints_unhit:
                print("You hit the {}". format(ship))
                self.board.board_dict[attack_point] = BOARD_HIT
                if ship.check_sunk(attack_point):
                    print("you sunk the {}".format(ship))
                    self.ships_afloat.remove(ship)
                    self.check_defeated()

    def check_defeated(self):
        """
        This checks whether the player is defeated.
        He is defeated, if all his ships are sunk.
        """
        if self.ships_afloat == []:
            self.defeated = True

    def __str__(self):
        """
        The player is represented by the players name, when printed
        """
        return self.name
