import statsapi as sa
from playsound import playsound as ps
import os

class MLBFSM:
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
            print("The " + game['away_name'] + " are scheduled to play at the " + game['home_name'] + " today")

    def printFinal(game, teamName):
        if teamName in game['winning_team']:
            print("The " + teamName + " already won today against the " + game['losing_team'])
        else:
            print("The " + teamName + " already lost today against the " + game['winning_team'])

    def getCurrentInning(newScoring):
        return int(newScoring[-1].split("\n")[1].split(" ")[1])

    def getCurrentInningState(newScoring):
        return newScoring[-1].split("\n")[1].split(" ")[0]

    def playHomeRun(self, newScoring, teamID, game, printed):
        if ("homers" in newScoring[-1]):
            playerName = newScoring[-1].split(" homers")[0]
            if (playerName in sa.roster(teamID) and game['current_inning'] == self.getCurrentInning(newScoring) and game['inning_state'] == self.getCurrentInningState(newScoring) and not printed):
                print(newScoring[-1])
                ps('SEE YA.mp3')
                printed = True
            return printed

    def printBoxScore(game):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(sa.linescore(game['game_id']))

    def getGameInfo(teamID):
        nextGameData = sa.boxscore_data(sa.next_game(teamID))['teamInfo']
        nextGameDate = sa.schedule(game_id = sa.next_game(teamID))[0]['game_date']
        if (nextGameData['away']['id'] != teamID):
            return [nextGameData['away']['teamName'], nextGameDate]
        else:
            return [nextGameData['home']['teamName'], nextGameDate]

    def stateMachine(self, game, gameState, inningState, teamName, oldScoring, teamID, printed):
        if gameState is 0:
            if game['status'] == 'In Progress':
                gameState = 1
                self.printProgress(game, teamName)
            elif  game['status'] == 'Scheduled' or game['status'] == 'Pre-Game' or game['status'] == 'Warmup':
                gameState = 2
                self.printScheduled(game, teamName)
            elif game['status'] == 'Final':
                gameState = 3
                self.printFinal(game, teamName)
        elif gameState is 1:
            if  game['status'] == 'Scheduled' or game['status'] == 'Pre-Game' or game['status'] == 'Warmup':
                gameState = 2
                self.printScheduled(game, teamName)
            elif game['status'] == 'Final':
                gameState = 3
                self.printFinal(game, teamName)
            topBottom = game['inning_state'];
            if inningState is -1:
                if topBottom == "Top":
                    inningState = 0
                    self.printBoxScore(game)
                    printed = False
                elif topBottom == "Middle":
                    inningState = 1
                    self.printBoxScore(game)
                elif topBottom == "Bottom":
                    inningState = 2
                    self.printBoxScore(game)
                    printed = False
                elif topBottom == "End":
                    inningState = 3
                    self.printBoxScore(game)
                    printed = False
            elif inningState is 0:
                if topBottom == "Middle":
                    inningState = 1
                    self.printBoxScore(game)
                    printed = False
            elif inningState is 1:
                if topBottom == "Bottom":
                    inningState = 2
                    self.printBoxScore(game)
                    printed = False
            elif inningState is 2:
                if topBottom == "End":
                    inningState = 3
                    self.printBoxScore(game)
                    printed = False
            elif inningState is 3:
                if topBottom == "Top":
                    inningState = 0
                    self.printBoxScore(game)
                    printed = False
            try:
                newScoring = sa.game_scoring_plays(game['game_id']).split("\n\n")
            except:
                raise Exception('No Scoring Plays')
            printed = self.playHomeRun(self, newScoring, teamID, game, printed)
        elif gameState is 2:
            if game['status'] == 'In Progress':
                gameState = 1
                self.printProgress(game, teamName)
            elif game['status'] == 'Final':
                gameState = 3
                self.printFinal(game, teamName)
            elif gameState is 3:
                if game['status'] == 'In Progress':
                    gameState = 1
                    self.printProgress(game, teamName)
                elif game['status'] == 'Scheduled' or game['status'] == 'Pre-Game' or game['status'] == 'Warmup':
                    gameState = 2
                    self.printSchedule(game, teamName)
        return [gameState, inningState, printed]
