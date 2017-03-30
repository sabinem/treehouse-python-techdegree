"""File includes all functions for Building a Soccer League 
and printing team assigmnet letters for the players"""
import csv
import operator
DRAGONS = 'Dragons'
SHARKS = 'Sharks'
RAPTORS = 'Raptors'
PRACTICE_DATETIME = {DRAGONS: 'March 17 at 1pm',
                     SHARKS: 'March 17 at 3pm',
                     RAPTORS: 'March 18 at 1pm'}


def print_letter_to_guardian(teamname, player):
    """A letter is written to the Guardians about which team the player is in and when practice is starting.
    The letter is written to a file with the name of the players: sabine_maennel.txt is the letter regarding
    player Sabine Maennel for example."""
    template = "Dear {},\nwe are happy to inform you that {} made it into team {}.\nThe first soccer " \
               "practice will be on {}.\nwith kind regards\n    The Soccer League"
    letter = template.format(player['Guardian Name(s)'],
                          player['Name'],
                          teamname,
                          PRACTICE_DATETIME[teamname])
    filename = '/'.join(['result','.'.join(['_'.join(player['Name'].lower().split(' ')),'txt'])])
    with open(filename, 'w') as file:
        file.write(letter)
    return filename

def process_team(teamname, players):
    """the team is processed: the writing of the letters to the players
    guardians is triggered here. Also a message is printed about how the players
    have been distributed into the teams."""
    teamcount = 0
    teamheight_sum = 0
    teamcount_experienced = 0
    letters = []
    for player in players:
        teamcount += 1
        teamheight_sum += int(player['Height (inches)'])
        if player['Soccer Experience'] == 'YES':
            teamcount_experienced += 1
        filename = print_letter_to_guardian(teamname, player)
        letters.append(filename)
    teamheight_avg = teamheight_sum/teamcount
    print("TEAM {} \n  Average height: {}, \n  Players: Total/Experienced {}/{}\n  Letters printed: {}".
          format(teamname, teamheight_avg, teamcount, teamcount_experienced, ', '.join(letters)))


if __name__ == "__main__":
    """main programm opens the player file and builds the teams so that
    they have players with balanced experence and height of players"""
    with open('data/soccer_players.csv', newline='\n') as playerfile:
        players = csv.DictReader(playerfile, delimiter=',')
        playerslist = list(players)
        playerslist.sort(key=operator.itemgetter('Height (inches)'))
        experience = [player for player in playerslist if player['Soccer Experience'] == 'YES']
        noexperience = [player for player in playerslist if player['Soccer Experience'] == 'NO']
        teams = {}
        teams[SHARKS] = experience[::3] + noexperience[2::3]
        teams[RAPTORS] = experience[1::3] + noexperience[1::3]
        teams[DRAGONS] = experience[2::3] + noexperience[::3]
        result = {}
        for key, value in teams.items():
            process_team(key, value)
