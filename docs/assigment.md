# Detailed Assignment

## Python Techdegree Treehouse Project 2

This project was an assignment of [Treehouse Techdegree Python](https://teamtreehouse.com/techdegree/python-web-development). Below you find the original description of the project.

## Description

In this project you will implement a console-based version of the popular battleship game. If you’re unfamiliar with this game please read this description on [Wikipedia](https://en.wikipedia.org/wiki/Battleship_(game)#Description). The game will be playable by two players by passing a laptop back and forth.

## Project Instructions

You’ll build a two player battleship game. Each player will place their ships without the other one watching. Then each player will take turns guessing locations where their opponent’s ships are. After the player has entered a location the screen will be cleared and the results of the guess will be displayed on the screen. The next player then has a turn. Players continue taking turns until one of the players guesses all of the locations on the board that opponent’s ships occupy. That player is declared the winner.
Part of the purpose of this project is to test your ability to perform object oriented programming. To get full credit, you’ll need to write a minimum of three class definitions. You may write more than three though.
The code should be clean, readable, and well organized and comply with Python PEP 8 standards.

### Prompt the players for their names.
Refer to players using their names whenever possible.
### Display an empty board.
Clear the screen and display an empty board on the screen. Use the EMPTY marker for all locations on the board. The board displays column headers as letters in the alphabet and displays numeric row numbers along the left side of the board.
### Prompt user to place a ship.
Under the board, prompt the user to enter one ship at a time. For each ship, ask if they want the ship to be oriented horizontally or vertically then ask which location on the board the first ships should be placed at: Below is an example prompt. You can use a different prompt.
Place the location of the aircraft carrier (5 spaces): a2 Is it horizontal? (Y)/N: n
### Validate user input.
If, at any time, the player enters input that can’t be parsed then continue prompting until valid input has been entered. Tell the user why their input was invalid before prompting again.
Be as accepting as possible of input. For example, spaces before or after the player’s input is allowed. Both lower and uppercase characters are also allowed. In order to reduce confusion, you may want to clear the screen and display the screen again before each attempt.
### Validate ship placement.
Verify that the ships fit on the board and that they don’t overlap with any existing ships. If a ship violates either of these rules, inform the player about the problem and prompt for a new location.
### Update the board.
After the user places a ship, clear the screen and print the board to the screen with all of the ships that the player has placed up until that point displayed on the board using the appropriate symbols.
### Prompt second player to place their ships
After the first player has placed all their ships, clear the screen and prompt the second player, by name, to begin placing their ships.
### Allow players to take turns.
Clear the screen after each player has finished taking their turn. Prompt the next player, by name, that it is their turn. Prompt them to press enter to continue. This gives the previous player a chance to hand the computer to the next player so they don’t see each other’s boards
### Display boards to the screen.
Clear the screen and print a board that shows where the current player has guessed so far. Use the appropriate markers to display which locations hit a ship, which locations are misses, and which locations are a sunken ship.
On the same screen but on a separate printed board, print a board that displays where their opponent has guessed up until then. Use the appropriate markers to display which locations hit a ship, which locations are misses, and which locations are a sunken ship. This board also displays the full locations of the current player’s ships using the appropriate markers.
### Prompt player for guess.
Prompt the player, by name, to guess where their opponent’s ships are by entering a location. For example:
Bob, enter a location: f7
### Validate guess.
If the player enters a location that they’ve already guessed, then prompt the user for a new location after telling them why their previous guess was unacceptable.
### Display guess results.
Clear the screen, and print a message stating that the player missed, hit, or sunk a ship. Prompt the next player, by name, that it is their turn and to press enter to continue.
### Declare a winner.
Continue the game until one of the players has sunk all of their opponent’s ships. Congratulate the winner with a final message. For an exceeds, display both the player’s boards on the screen.

## Extra Credit

- The screen is cleared after an invalid entry. The board and prompts are redisplayed and the game informs the player why their input was unacceptable.
Detailed error messages are displayed.
- Error messages are detailed and include the invalid guess information.
- Display both the player’s boards on the screen showing the ship positions.
