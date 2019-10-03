import statsapi as sa
import datetime
import os
from MLBFSM import MLBFSM as FSM
import time

def main():
	#0 - No State
	#1 - Before Game
	#2 - During Game
	#3 - After Game
	gameState = 0
	inningState = -1
	homeRun = False
	states = [gameState, inningState, homeRun]
	teamName = input("Enter the team you would like to listen to: ")

	TeamData = sa.lookup_team(teamName)

	teamID = TeamData[0]['id']

	printed = False

	os.system('cls' if os.name == 'nt' else 'clear')

	while 1:
		oldScoring = []
		schedule = sa.schedule(datetime.date.today(), team = teamID)
		try:
			game = schedule[0]
		except:
			if not printed:
				print("The " + teamName + " do not have a game today, their next game will be against the " + FSM.getGameInfo(teamID)[0] + " on " + FSM.getGameInfo(teamID)[1])
				printed = True
			continue

		#try:
		states = FSM.stateMachine(FSM, game, states[0], states[1], teamName, oldScoring, teamID, states[2])
		#except:
		#	continue

		time.sleep(120)


main()
