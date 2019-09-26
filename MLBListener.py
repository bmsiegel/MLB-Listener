import statsapi as sa
import datetime
from playsound import playsound as ps
import os



def printProgress(game, teamName):
		homeTeamStr = game['home_name']
		awayTeamStr = game['away_name']
		homeTeamID = game['home_id']
		awayTeamID = game['away_id']
		if teamName in homeTeamStr:
			print("The " + homeTeamStr + " are playing against the " + awayTeamStr)
		else:
			print("The " + awayTeamStr + " are playing against the " + homeTeamStr)

def printScheduled(game, teamName):
		if teamName in game['home_name']:
			print("The " + game['home_name'] + " are scheduled to play versus the " + game['away_name'] + " today")
		if teamName in game['away_name']:
			print("The " + game['away_name'] + " are schedule to play at the " + game['home_name'] + " today")

def printFinal(game, teamName):
		if teamName in game['winning_team']:
			print("The " + teamName + " already won today against the " + game['losing_team'])
		else:
			print("The " + teamName + " already lost today against the " + game['winning_team'])

def main():
	#0 - No State
	#1 - Before Game
	#2 - During Game
	#3 - After Game
	state = 0

	teamName = input("Enter the team you would like to listen to: ")

	TeamData = sa.lookup_team(teamName)

	teamID = TeamData[0]['id']

	printed = False

	os.system('cls' if os.name == 'nt' else 'clear')

	while 1:
		schedule = sa.schedule(datetime.date.today(), team = teamID)

		oldScoring = []
		inprog = False
		scheddy = False
		final = False

		game = schedule[0]
		#gonna have to make this an FSM Prolly
		if state is 0:
			if game['status'] == 'In Progress':
				state = 1
				printProgress(game, teamName)
			elif  game['status'] == 'Scheduled' or game['status'] == 'Pre-Game' or game['status'] == 'Warmup':
				state = 2
				printScheduled(game, teamName)
			elif game['status'] == 'Final':
				state = 3
				printFinal(game, teamName)
		elif state is 1:
			if  game['status'] == 'Scheduled' or game['status'] == 'Pre-Game' or game['status'] == 'Warmup':
				state = 2
				printScheduled(game, teamName)
			elif game['status'] == 'Final':
				state = 3
				printFinal(game, teamName)
			try:
				newScoring = sa.game_scoring_plays(game['game_id']).split("\n\n")
			except:
				continue
			if len(oldScoring) != len(newScoring):
				if ("homers" in newScoring[-1]):
					playerName = newScoring[-1].split(" homers")[0]
					if (playerName in sa.roster(teamID) and game['current_inning'] == int(newScoring[-1].split("\n")[1].split(" ")[1])):
						print(newScoring[-1])
						ps('SEE YA.mp3')
			oldScoring = newScoring
		elif state is 2:
			if game['status'] == 'In Progress':
				state = 1
				printProgress(game, teamName)
			elif game['status'] == 'Final':
				state = 3
				printFinal(game, teamName)
		elif state is 3:
			if game['status'] == 'In Progress':
				state = 1
				printProgress(game, teamName)
			elif  game['status'] == 'Scheduled' or game['status'] == 'Pre-Game' or game['status'] == 'Warmup':
				state = 2
				printSchedule(game, teamName)
		game = sa.schedule(datetime.date.today(), team = teamID)[0]

main()
