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
	scheddy = False
	final = False

	game = schedule[0]
	#gonna have to make this an FSM Prolly
	if game['status'] == 'In Progress':
		inprog = True
		scheddy = False
		final = False
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
				if ("homers" in newScoring[-1]):
					playerName = newScoring[-1].split(" homers")[0]
					if (playerName in sa.roster(teamID)):
						print(newScoring[-1])
						ps('SEE YA.mp3')
			oldScoring = newScoring
			game = sa.schedule(datetime.date.today(), team = teamID)[0]
	elif game['status'] == 'Scheduled' or game['status'] == 'Pre-Game' or game['status'] == 'Warmup':
		scheddy = True
		inprog = False
		final = False
	elif game['status'] == 'Final':
		final = True
		scheddy = False
		inprog = False
	if not printed:
		if scheddy:
			if teamName in game['home_name']:
				print("The " + game['home_name'] + " are scheduled to play versus the " + game['away_name'] + " today")
			if teamName in game['away_name']:
				print("The " + game['away_name'] + " are schedule to play at the " + game['home_name'] + " today")
		elif final:
			if teamName in game['winning_team']:
				print("The " + teamName + " already won today against the " + game['losing_team'])
			else:
				print("The " + teamName + " already lost today against the " + game['winning_team'])
		else:
			print("The " + teamName + " are off today")
		printed = True
