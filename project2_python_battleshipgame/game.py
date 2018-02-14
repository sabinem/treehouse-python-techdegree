"""
This is the main file of the Battleship Game.
It includes and initiates the Game-Class
"""
from basic import clear_screen
from player import Player


class Game:
    """
    Initiation of the Game Class starts the Battleship Game
    """
    def setup(self):
        """
        This methods sets up the game.
        """
        self.get_players()
        self.setup_player(self.player1)
        self.setup_player(self.player2)

    def get_players(self):
        """
        This gets the names of the players and prompts them to continue into
        the single player setup for both players.
        """
        clear_screen()
        print('Welcome to the Battleship game. You need two players. '
              '\nPlease give the name of the first player:')
        self.player1 = Player()
        print("Thank you. So {} is playing.\n"
              "Now please provide the second player's name!"
              .format(self.player1))
        self.player2 = Player(opponent=self.player1)
        input('Great {} and {}! '
              'Press Enter when you are ready to start the game.'
              .format(self.player1, self.player2))

    def setup_player(self, player):
        """
        This is the single player setup of their battleships.
        """
        clear_screen()
        input("{}! It is your turn to set up your battleships.\n"
              "Press Enter when you are ready to do that."
              .format(player))
        player.setup_ships()

    def get_turn(self, player):
        """
        This prompts a player to take his turn. When he is ready,
        he hits any key, then the screen is cleared an his turn starts.
        """
        clear_screen()
        input("It is {}'s turn!\n{}, "
              "press Enter when you are ready to start you turn."
              .format(player, player))
        clear_screen()
        opponent_player = self.get_opponent_in_game(player)
        player.perform_turn(opponent_player)

    def get_opponent_in_game(self, player):
        """
        This fetches the other player in the game.
        """
        try:
            if player == self.player1:
                return self.player2
            else:
                return self.player1
        except NameError:
            return None

    def __init__(self):
        """
        This initiates the game. It is over,
        when one of the players is defeated,
        meaning all his ships are sunk.
        """
        self.setup()
        while not (self.player1.defeated or self.player2.defeated):
            self.get_turn(self.player1)
            self.get_turn(self.player2)

Game()
