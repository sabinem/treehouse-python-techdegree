# Treehouse Python Techdegree: 1. Project Soccer League Team Assigments

## Assignment: 

### Description
You have volunteered to be the Coordinator for your town’s youth soccer league. As part of your job you need to divide the 18 children who have signed up for the league into three even teams - Dragons, Sharks and Raptors. In years past, the teams have been unevenly matched, so this year you are doing your best to fix that. For each child, you will have the following information: Name, height (in inches), whether or not they have played soccer before, and their guardians’ names.

The project has three major parts. For each part choose from the tools we have covered in the courses so far. Please don’t employ more advanced tools we haven’t covered yet, even if they are right for the job. However, if you identify a place where a more advanced tool is appropriate, please mention that in a code comment as you and your mentor may want to discuss it later.

Part 1: We have provided information for the 18 players in the attached spreadsheet. Please choose an appropriate data type to store the information for each player. Once you have decided on what tools to use, convert the player data so it can be used in Part 2.

Part 2: Create logic that can iterate through all 18 players and assign them to teams such that the number of experienced players on each team are the same. Store each team’s players in its own new collection variable for use in Part 3. (Please note: your logic should work correctly regardless of the initial ordering of the players. Also, if you would like to attain an “exceeds expectations” rating for this project, add logic to ensure that each teams’ average height is within 1 inch of the others.)

Part 3: Create logic that iterates through all three teams of players and generates a personalized letter to the guardians, letting them know which team the child has been placed on and when they should attend their first team team practice. As long as you provide the necessary information (player name, guardians’ names, practice date/time), feel free to have fun with the content of the letter. The team practice dates/times are as follows:

Dragons - March 17, 1pm, Sharks - March 17, 3pm, Raptors - March 18, 1pm

When your complete code is run, it should output individual letters to file. There should be a total of 18 letters, one for each player.

As always, meaningful and concise code comments are expected. Your code should be written and refined in workspaces or on your local machine, but be sure to upload it to GitHub, as per the instructions in this tutorial.

### Project Instructions

- Manually create a single collection that contains all information for all 18 players. Each player should themselves be represented by their own collection.

- Create appropriate variables and logic to sort and store players into three teams: Sharks, Dragons and Raptors. Be sure that your logic results in all teams having the same number of experienced players on each. The collections will be named sharks, dragons, raptors, and league.

- Create a function named write_letter that takes a player and returns a string of the letter to their guardian(s). Be sure the string is formatted as a letter and starts with "Dear" and the guardian(s) name(s) and with the additional required information: player's name, team name, and date & time of first practice.

- Save all 18 letters to disk, giving each letter a filename of the player's name, in lowercase and with underscores and ending in .txt. For example, kenneth_love.txt.
- Ensure your script doesn't execute when imported; put all of your logic and function calls inside of an if __name__ == "__main__": block.
- Save to disk, a personalized letter to the Guardians of each player. Specify: the player’s name, team name, and date/time of their first team practice. There should be a total of 18 letters, one for each player.
- As always, please add concise and descriptive comments to your code and be sure to name your constants, variables and keys descriptively.
- In order to get an “Exceeds Expectations” rating, also provide logic to ensure each team’s average height is within 1 inch of the others, as well as having each team contain the same number of experienced players.

## Installation

- Download the zip file to your computer and unzip
- Go into the directory
- Start the application with `python3 soccer_league.py` 
- it will generate a text file for each player with the team assgnement
