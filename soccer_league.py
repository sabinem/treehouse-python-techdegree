import csv
import operator
DRAGONS = 'Dragons'
SHARKS = 'Sharks'
RAPTORS = 'Raptors'
PRACTICE_DATETIME = {DRAGONS: 'March 17 at 1pm',
                     SHARKS: 'March 17 at 3pm',
                     RAPTORS: 'March 18 at 1pm'}


def print_letter_to_guardian(teamname, player):
    """
    A letter is written to the Guardians about which team the player is in and when practice is starting.
    The letter is written to a file with the name of the players: sabine_maennel.txt is the letter regarding
    player Sabine Maennel for example.
    """
    template = "Dear {},\nwe are happy to inform you that {} made it into team {}.\nThe first soccer " \
               "practice will be on {}.\nwith kind regards\n    The Soccer League"
    letter = template.format(player['Guardian Name(s)'],
                          player['Name'],
                          teamname,
                          PRACTICE_DATETIME[teamname])
    filename = '.'.join(['_'.join(player['Name'].lower().split(' ')),'txt'])
    with open(filename, 'w') as file:
        file.write(letter)
    return filename

def process_team(teamname, players):
    """
    the team is processed: the writing of the letters to the players
    guardians is triggered here. Also a message is printed about hwo the players
    have been distributed into the teams.
    """
    teamcount = 0
    teamheight_sum = 0
    teamcount_experienced = 0
    letters = []

    # process the players in the team
    for player in players:

        teamcount += 1
        teamheight_sum += int(player['Height (inches)'])

        if player['Soccer Experience'] == 'YES':
            teamcount_experienced += 1

        # the letter is written
        filename = print_letter_to_guardian(teamname, player)
        letters.append(filename)

    # the average team height is calculated
    teamheight_avg = teamheight_sum/teamcount

    # message to the user about the result of the team building
    print("TEAM {} \n  Average height: {}, \n  Players: Total/Experienced {}/{}\n  Letters printed: {}".
          format(teamname, teamheight_avg, teamcount, teamcount_experienced, ', '.join(letters)))


if __name__ == "__main__":
    # read players from csv files
    with open('soccer_players.csv', newline='\n') as playerfile:

        # read form csv file into a dictionary
        players = csv.DictReader(playerfile, delimiter=',')

        # transform into a list of players
        playerslist = list(players)

        # sort list by players height
        playerslist.sort(key=operator.itemgetter('Height (inches)'))

        # seperate experienced from unexperienced players
        experience = [player for player in playerslist if player['Soccer Experience'] == 'YES']
        noexperience = [player for player in playerslist if player['Soccer Experience'] == 'NO']

        # now slice both lists in a way that height is distributed as equal as possible
        teams = {}
        teams[SHARKS] = experience[::3] + noexperience[2::3]
        teams[RAPTORS] = experience[1::3] + noexperience[1::3]
        teams[DRAGONS] = experience[2::3] + noexperience[::3]
        result = {}
        for key, value in teams.items():
            process_team(key, value)