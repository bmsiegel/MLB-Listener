import statsapi as sa
import datetime
from playsound import playsound as ps
import os


teamName = input("Enter the team you would like to listen to: ")

TeamData = sa.lookup_team(teamName)

teamID = TeamData[0]['id']

printed = False

os.system('clear')

while 1:
	schedule = sa.schedule(datetime.date.today(), team = teamID)
	
	oldScoring = []
	inprog = False

	game = schedule[0]
	if game['status'] == 'In Progress':
		inprog = True
		printed = False
		homeTeamStr = game['home_name']
		awayTeamStr = game['away_name']
		homeTeamID = game['home_id']
		awayTeamID = game['away_id']
		if teamName in homeTeamStr:
			print("The " + homeTeamStr + " are playing against the " + awayTeamStr)
		else:
			print("The " + awayTeamStr + " are playing against the " + homeTeamStr)
		while game['status'] == 'In Progress':
			newScoring = sa.game_scoring_plays(game['game_id']).split("\n\n")
			if len(oldScoring) != len(newScoring):
				if ("homers" in newScoring[-1] and game['current_inning'] == newScoring[-1].split(" ")[1] and game['inning_state'] == newScoring[-1].split(" ")[0]):
					playerName = newScoring[-1].split(" homers")[0]
					if (playerName in sa.roster(teamID)):
						print(newScoring[-1])
						ps('SEE YA.mp3')
			oldScoring = newScoring
			game = sa.schedule(datetime.date.today(), team = teamID)[0]
	
	if not inprog and not printed:
		print("The " + teamName + " are not playing a game right now")
		printed = True
	elif not printed:
		if (teamName in game['winning_team']):
			print("Game Over! The " + teamName + " win!")
		else:
			print("Game Over! The " + teamName + " lose!")
