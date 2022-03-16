from player_move import *

# ALL STRATEGIES SHOULD EXTEND BASE STRATEGY. Or at least implement the same thing as base strategy
class BaseStrategy:
	def __init__(self):
		self.name = 'Scissors'

	# 'player1': player1
	# 'player2': player2
	# 'move1': move by player1
	# 'move2': move by player2
	# 'pos': turn count (position of the "move")
	def moveListener(self, move):
		pass

	# 'player1': player1
	# 'player2': player2
	# 'event': 'start' or 'end'
	# 'result': result if event is 'end'
	def matchListener(self, match):
		pass

	# 'event': 'start' or 'end'
	# 'players': list of players if event is 'start'
	# 'dropouts': dropouts if event is 'end'
	def roundListener(self, round):
		pass

	# Your main logic
	def getMove(self):
		return PlayerMove.SCISSORS

class Documenter(BaseStrategy):
	def __init__(self):
		self.logs = {}

	def matchListener(self, match):
		if match['event'] == 'end':
			p1 = match['player1']
			p2 = match['player2']
			result = match['result']

			if p1 not in self.logs:
				self.logs[p1] = {}
			if p2 not in self.logs:
				self.logs[p2] = {}

			if p2 not in self.logs[p1]:
				self.logs[p1][p2] = {'wins': 0, 'loses': 0, 'draws': 0}

			if p1 not in self.logs[p2]:
				self.logs[p2][p1] = {'wins': 0, 'loses': 0, 'draws': 0}

			if result == 'draw':
				self.logs[p1][p2]['draws'] += 1
				self.logs[p2][p1]['draws'] += 1
			else:
				loser = p1 if result == p2 else p2
				self.logs[result][loser]['wins'] += 1
				self.logs[loser][result]['loses'] += 1

	def toString(self):
		retVal = ''
		for player, performance in self.logs.items():
			retVal += f"{player}'s cumulative match results:\n"
			for opponent, result in performance.items():
				retVal += f"{opponent}: {result['wins']} wins, {result['loses']} loses, {result['draws']} draws\n"
			retVal += '\n'
		retVal += '\n'
		return retVal


class Rock(BaseStrategy):
	def __init__(self):
		self.name = 'Rocks'

	def getMove(self):
		return PlayerMove.ROCK

class Paper(BaseStrategy):
	def __init__(self):
		self.name = 'Papers'

	def getMove(self):
		return PlayerMove.PAPER

class Rand(BaseStrategy):
	def __init__(self):
		self.name = 'Rand'

	def getMove(self):
		import random
		r = random.randrange(0,3)
		return PlayerMove.ROCK if r == 0 else PlayerMove.PAPER if r == 1 else PlayerMove.SCISSORS
# =======================================================================#
class Player2(BaseStrategy):
	def __init__(self):
		self.name = 'Player2'
		self.round = 0
		self.state = None
		self.meLast = None
		self.enemyLast = None

	def matchListener(self, match):
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.round = 0

	def moveListener(self, move):
		if move['player1'] == self.name:
			self.meLast = move['move1']
			self.enemyLast = move['move2']
		elif move['player2'] == self.name:
			self.meLast = move['move2']
			self.enemyLast = move['move1']

	def getMove(self):
		retVal = None
		if self.round == 0:
			retVal = PlayerMove.PAPER
		elif self.meLast <= self.enemyLast:
			retVal = getCounter(self.enemyLast)
		else:
			retVal = self.enemyLast
		
		assert retVal != None
		self.round += 1
		return retVal

class Player4(BaseStrategy):
	def __init__(self):
		self.name = 'Player4'
		self.round = 0
		self.lastStart = PlayerMove.PAPER
		self.meLast = None
		self.enemyLast = None

	def matchListener(self, match):
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.round = 0

	def moveListener(self, move):
		if move['player1'] == self.name:
			self.meLast = move['move1']
			self.enemyLast = move['move2']
		elif move['player2'] == self.name:
			self.meLast = move['move2']
			self.enemyLast = move['move1']

	def getMove(self):
		retVal = None
		if self.round == 0:
			retVal = PlayerMove.PAPER if self.lastStart == PlayerMove.ROCK else PlayerMove.SCISSORS if self.lastStart == PlayerMove.PAPER else PlayerMove.ROCK
			self.lastStart = retVal
		elif self.meLast < self.enemyLast:
			retVal = getCounter(self.enemyLast)
		else:
			retVal = getCounter(self.meLast)
		
		assert retVal != None
		self.round += 1
		return retVal

class Player3(BaseStrategy):
	def __init__(self):
		self.name = 'Player3'
		self.enemyLastTwo = []

	def matchListener(self, match):
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.enemyLastTwo = []

	def moveListener(self, move):
		if move['player1'] == self.name:
			self.enemyLastTwo.append(move['move2'])
		elif move['player2'] == self.name:
			self.enemyLastTwo.append(move['move1'])

		if len(self.enemyLastTwo) > 2:
			self.enemyLastTwo.pop(0)

	def getMove(self):
		retVal = None
		if PlayerMove.ROCK in self.enemyLastTwo:
			retVal = PlayerMove.PAPER
		elif PlayerMove.PAPER in self.enemyLastTwo:
			retVal = PlayerMove.SCISSORS
		elif PlayerMove.SCISSORS in self.enemyLastTwo:
			retVal = PlayerMove.ROCK
		else:
			retVal = PlayerMove.ROCK
		
		assert retVal != None
		return retVal

class Player5(BaseStrategy):
	def __init__(self):
		self.name = 'Player5'
		self.enemyLast = None

	def moveListener(self, move):
		if move['player1'] == self.name:
			self.enemyLast= move['move2']
		elif move['player2'] == self.name:
			self.enemyLast= move['move1']

	def getMove(self):
		retVal = None

		if PlayerMove.SCISSORS == self.enemyLast:
			retVal = PlayerMove.SCISSORS
		else:
			retVal = PlayerMove.PAPER
		
		assert retVal != None
		return retVal

class Player6(BaseStrategy):
	def __init__(self):
		self.name = 'Player6'
		self.cycle = [PlayerMove.PAPER,PlayerMove.SCISSORS,PlayerMove.ROCK,PlayerMove.ROCK,PlayerMove.SCISSORS,PlayerMove.PAPER]
		self.index = 0

	def matchListener(self, match):
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.index = 0

	def getMove(self):
		retVal = self.cycle[self.index]
		self.index += 1
		self.index %= len(self.cycle)
		
		return retVal

class Player10(BaseStrategy):
	def __init__(self):
		self.name = 'Player10'
		self.meLast = None
		self.enemyLast = None

		self.win_23 = 0
		self.lose_23 = 0

		self.state = 'start'
		self.phase = 1

	def matchListener(self, match):
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.meLast = None
			self.enemyLast = None

			self.win_23 = 0
			self.lose_23 = 0

			self.state = 'start'
			self.phase = 1

	def moveListener(self, move):
		if move['player1'] == self.name:
			self.meLast = move['move1']
			self.enemyLast = move['move2']
		elif move['player2'] == self.name:
			self.meLast = move['move2']
			self.enemyLast = move['move1']
		else:
			return


		if self.state == 'start':
			self.state = 'copy_opponent'
			self.phase = 1
			self.win_23 = 0
			self.lose_23 = 0
		else:
			# Record win/loss
			if self.meLast > self.enemyLast:
				self.win_23 += 1
			elif self.meLast < self.enemyLast:
				self.lose_23 += 1

			# Check phase
			if self.phase == 1:
				self.phase = 2
			else:
				self.phase = 1
				# FSM
				if self.state == 'lose_opponent':
					if self.win_23 > self.lose_23:
						self.state = 'lose_opponent'
					elif self.win_23 < self.lose_23:
						self.state = 'win_opponent'
					else:
						self.state = 'copy_self'
				elif self.state == 'win_opponent':
					if self.win_23 > self.lose_23:
						self.state = 'win_opponent'
					elif self.win_23 < self.lose_23:
						self.state = 'copy_opponent'
					else:
						self.state = 'lose_opponent'
				elif self.state == 'copy_opponent':
					if self.win_23 > self.lose_23:
						self.state = 'copy_opponent'
					elif self.win_23 < self.lose_23:
						self.state = 'lose_opponent'
					else:
						self.state = 'win_self'
				elif self.state == 'lose_self':
					if self.win_23 > self.lose_23:
						self.state = 'lose_self'
					elif self.win_23 < self.lose_23:
						self.state = 'win_self'
					else:
						self.state = 'copy_self'
				elif self.state == 'win_self':
					if self.win_23 > self.lose_23:
						self.state = 'copy_self'
					elif self.win_23 < self.lose_23:
						self.state = 'lose_self'
					else:
						self.state = 'win_self'
				elif self.state == 'copy_self':
					if self.win_23 > self.lose_23:
						self.state = 'copy_self'
					elif self.win_23 < self.lose_23:
						self.state = 'lose_self'
					else:
						self.state = 'win_self'
				else:
					raise Exception

				self.win_23 = 0
				self.lose_23 = 0

	def getMove(self):
		retVal = None

		if self.state == 'start':
			retVal = PlayerMove.SCISSORS
		elif self.state == 'win_self':
			retVal = getCounter(self.meLast)
		elif self.state == 'lose_self':
			retVal = getNotCounter(self.meLast)
		elif self.state == 'copy_self':
			retVal = self.meLast
		elif self.state == 'win_opponent':
			retVal = getCounter(self.enemyLast)
		elif self.state == 'lose_opponent':
			retVal = getNotCounter(self.enemyLast)
		elif self.state == 'copy_opponent':
			retVal = self.enemyLast
			
		
		assert retVal != None
		return retVal

class Player8(BaseStrategy):
	def __init__(self):
		self.name = 'Player8'
		self.enemyLast = None
		self.meLast = None
		self.consecLoses = 0
		self.state = 1

	def matchListener(self, match):
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.options = [PlayerMove.SCISSORS, PlayerMove.SCISSORS, PlayerMove.SCISSORS, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.PAPER, PlayerMove.PAPER, PlayerMove.PAPER]
			self.meLast = None
			self.enemyLast = None
			self.consecLoses = 0
			self.state = 1

	def moveListener(self, move):
		if move['player1'] == self.name:
			me = move['move1']
			enemy = move['move2']
		elif move['player2'] == self.name:
			me = move['move2']
			enemy = move['move1']
		else:
			return
		if me < enemy:
			self.consecLoses += 1
		else:
			self.consecLoses = 0

		if self.consecLoses >= 6 or self.state == 10:
			self.state = 10
		else:
			self.state = (self.state - 1) % 8 + 2

		self.meLast = me
		self.enemyLast = enemy

	def getMove(self):
		retVal = None
		if self.state == 1:
			return PlayerMove.PAPER
		elif self.state == 10:
			retVal = self.enemyLast
		else:
			if self.meLast > self.enemyLast:
				retVal = self.meLast
			elif self.meLast == self.enemyLast:
				retVal = self.options[self.state - 2]
			else:
				lst = [PlayerMove.ROCK, PlayerMove.PAPER, PlayerMove.SCISSORS]
				lst.remove(self.meLast)
				lst.remove(self.enemyLast)
				retVal = lst.pop()
				assert retVal == getCounter(self.enemyLast)
		
		assert retVal != None
		return retVal

class Player1(BaseStrategy):
	def __init__(self):
		self.name = 'Player1'
		self.firstMove = None
		self.meLast = None
		self.enemyLast = None

		self.win = 0
		self.lose = 0

		self.state = 'start'
		self.phase = 1

		self.moveTracker = {}
		self.moveTrackerOld = {}
		self.sameMovesUser = []
		self.pos = 0
		self.opponent = None

	def roundListener(self, round):
		if round['event'] == 'start':
			self.moveTrackerOld = self.moveTracker
			self.moveTracker = {p: [None] * 10 for p in round['players']}
		if round['event'] == 'end':
			self.sameMovesUser = []
			for p,v in self.moveTracker.items():
				if v != None:
					self.sameMovesUser.append(p)

	def matchListener(self, match):
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.opponent = match['player1'] if match['player1'] != self.name else match['player2']
			if self.opponent in ['Player2', 'Player3', 'Player4', 'Player5', 'Player6', 'Player7', 'Player8', 'Player10']:
				self.firstMove = PlayerMove.PAPER
			else:
				self.firstMove = PlayerMove.SCISSORS

			self.meLast = None
			self.enemyLast = None

			self.win = 0
			self.lose = 0

			self.state = 'start'
			self.phase = 1
			self.pos = 0

	def moveListener(self, move):
		p1 = move['player1']
		p2 = move['player2']
		m1 = move['move1']
		m2 = move['move2']
		pos = move['pos']

		if pos < 10 and self.moveTracker[p1] != None:
			if self.moveTracker[p1][pos] == None:
				self.moveTracker[p1][pos] = m1
			elif self.moveTracker[p1][pos] != m1:
				self.moveTracker[p1] = None

		if pos < 10 and self.moveTracker[p2] != None:
			if self.moveTracker[p2][pos] == None:
				self.moveTracker[p2][pos] = m2
			elif self.moveTracker[p2][pos] != m2:
				self.moveTracker[p2] = None

		if p1 == self.name:
			self.meLast = m1
			self.enemyLast = m2
		elif p2 == self.name:
			self.meLast = m2
			self.enemyLast = m1
		else:
			return

		if self.state == 'start':
			if self.opponent in self.sameMovesUser:
				if self.meLast > self.enemyLast:
					self.pos = pos + 1
				else:
					self.sameMovesUser.remove(self.opponent)
			else: 
				self.state = 'lose_opponent'
				self.phase = 1
				self.win = 0
				self.lose = 0
		else:
			# Record win/loss
			if self.meLast > self.enemyLast:
				self.win += 1
			elif self.meLast < self.enemyLast:
				self.lose += 1

			# Check phase
			if self.phase == 1:
				self.phase = 2
			elif self.phase == 2:
				self.phase = 3
			else:
				# Phase 3 - change strategy and reset to 1
				self.phase = 1
				if self.state == 'lose_opponent':
					if self.win > self.lose:
						self.state = 'lose_opponent'
					else:
						self.state = 'win_opponent'
				elif self.state == 'win_opponent':
					if self.win > self.lose:
						self.state = 'win_opponent'
					else:
						self.state = 'lose_opponent'
				else:
					raise Exception

				self.win = 0
				self.lose = 0

	def getMove(self):
		retVal = None

		if self.state == 'start':
			if self.opponent in self.sameMovesUser:
				retVal = getCounter(self.moveTrackerOld[self.opponent][self.pos])
			else:
				retVal = self.firstMove
		elif self.state == 'win_opponent':
			retVal = getCounter(self.enemyLast)
		elif self.state == 'lose_opponent':
			retVal = getNotCounter(self.enemyLast)	
		
		assert retVal != None
		return retVal

class Player7(BaseStrategy):
	def __init__(self):
		self.name = 'Player7'

		self.firstMoves = None
		self.moveWeights = None
		self.firstMoveFlag = False

		self.myScore = 0
		self.enemyScore = 0
		self.myEnemy = None
		self.panic = False

	def roundListener(self, round):
		if self.firstMoves == None: # First announcement
			self.firstMoves = {p: {'Rock': 0, 'Paper': 0, 'Scissors': 0} for p in round['players']}
			self.moveWeights = {p: {'Rock': 0, 'Paper': 0, 'Scissors': 0} for p in round['players']}

	def matchListener(self, match):
		self.firstMoveFlag = True
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.myScore = 0
			self.enemyScore = 0
			self.myEnemy = match['player1'] if match['player1'] != self.name else match['player2']
			self.panic = False

	def _update(self, weightValue, newMove):
		weightValue[newMove.value] += 1
		weightValue['Rock'] *= 0.8
		weightValue['Paper'] *= 0.8
		weightValue['Scissors'] *= 0.8

	def moveListener(self, move):
		if self.firstMoveFlag:
			self.firstMoveFlag = False
			self._update(self.firstMoves[move['player1']], move['move1'])
			self._update(self.firstMoves[move['player2']], move['move2'])

		if move['player1'] == self.name:
			self._update(self.moveWeights[move['player2']], move['move2'])
			me = move['move1']
			enemy = move['move2']
		elif move['player2'] == self.name:
			self._update(self.moveWeights[move['player1']], move['move1'])
			me = move['move2']
			enemy = move['move1']
		else:
			return

		if me > enemy:
			self.myScore += 1
		elif me < enemy:
			self.enemyScore += 1

		if self.enemyScore - self.myScore >= 5:
			self.panic = True

	def _getMostCommon(self, behavior):
		if behavior['Paper'] > behavior['Rock'] and behavior['Paper'] > behavior['Scissors']:
			return PlayerMove.PAPER
		elif behavior['Rock'] > behavior['Scissors']:
			return PlayerMove.ROCK
		else:
			return PlayerMove.SCISSORS

	def getMove(self):
		retVal = None

		if self.firstMoveFlag:
			retVal = getCounter(self._getMostCommon(self.firstMoves[self.myEnemy]))
		else:
			common = self._getMostCommon(self.moveWeights[self.myEnemy])
			if self.panic:
				retVal = common
			else:
				retVal = getCounter(common)

		assert retVal != None
		return retVal

class Player9(BaseStrategy):
	def __init__(self):
		self.name = 'Player9'
		self.base = [PlayerMove.SCISSORS, PlayerMove.SCISSORS, PlayerMove.PAPER, PlayerMove.PAPER, PlayerMove.ROCK, PlayerMove.SCISSORS, PlayerMove.ROCK, PlayerMove.PAPER, PlayerMove.PAPER, PlayerMove.PAPER, PlayerMove.ROCK, PlayerMove.SCISSORS, PlayerMove.PAPER, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.PAPER, PlayerMove.PAPER, PlayerMove.SCISSORS, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.SCISSORS, PlayerMove.PAPER, PlayerMove.PAPER, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.SCISSORS, PlayerMove.ROCK, PlayerMove.SCISSORS, PlayerMove.PAPER, PlayerMove.ROCK, PlayerMove.SCISSORS, PlayerMove.PAPER, PlayerMove.PAPER, PlayerMove.SCISSORS, PlayerMove.ROCK, PlayerMove.PAPER, PlayerMove.ROCK, PlayerMove.SCISSORS, PlayerMove.PAPER, PlayerMove.PAPER, PlayerMove.SCISSORS, PlayerMove.PAPER, PlayerMove.PAPER, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.PAPER, PlayerMove.ROCK, PlayerMove.ROCK]
		self.increments = [7,11,3,1,17,9,13]
		self.p1 = "Paper, Paper, Paper, Paper"
		self.p2 = "Scissors, Scissors, Scissors, Scissors"
		self.p3 = "Rock, Rock, Rock, Rock"
		self.p4 = ["Paper, Scissors, Rock, Paper, Scissors", "Scissors, Paper, Rock, Scissors, Paper"]
		self.p5 = ["Scissors, Rock, Paper, Scissors, Rock", "Rock, Scissors, Paper, Rock, Scissors"]
		self.p6 = ["Rock, Paper, Scissors, Rock, Paper", "Paper, Rock, Scissors, Paper, Rock"]

		self.antiCounterCounter = 0 #cheesy name
		self.meLast = None
		self.enemyLast = [] #cheesy name
		self.enemyWins = 0
		self.gameID = 0
		self.count = 0

	def matchListener(self, match):
		self.gameID += 1
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.count = (self.count + self.increments[self.gameID % 7]) % 50
			self.meLast = None
			self.enemyMoves = []
			self.enemyWins = 0

	def moveListener(self, move):
		if move['player1'] == self.name:
			me = move['move1']
			enemy = move['move2']
		elif move['player2'] == self.name:
			me = move['move2']
			enemy = move['move1']
		else:
			return

		if self.meLast != None and getCounter(self.meLast) == enemy:
			self.antiCounterCounter += 1
		else:
			self.antiCounterCounter = 0

		self.meLast = me
		self.enemyLast.append(enemy.value)
		self.enemyWins += 1 if enemy > me else 0
		self.count = (self.count + 1) % 50

		if len(self.enemyLast) > 5:
			self.enemyLast.pop(0)

	def _enemyToString(self, start_index):
		return ', '.join(self.enemyLast[start_index:5])

	def getMove(self):
		retVal = self.base[self.count]

		if self.enemyWins > 5:
			last_5 = self._enemyToString(0)
			last_4 = self._enemyToString(1)
			if last_4 == self.p1:
				retVal = PlayerMove.SCISSORS
			if last_4 == self.p2:
				retVal = PlayerMove.ROCK
			if last_4 == self.p3:
				retVal = PlayerMove.PAPER
			if self.antiCounterCounter >= 4:
				retVal = getNotCounter(self.meLast)
			if last_5 in self.p4:
				retVal = PlayerMove.PAPER
			if last_5 in self.p5:
				retVal = PlayerMove.SCISSORS
			if last_5 in self.p6:
				retVal = PlayerMove.ROCK

		return retVal

class WaPlayer1(BaseStrategy):
	def __init__(self):
		self.name = 'WaPlayer1'
		self.order = [PlayerMove.ROCK, PlayerMove.PAPER, PlayerMove.ROCK, PlayerMove.SCISSORS, PlayerMove.PAPER, PlayerMove.SCISSORS, PlayerMove.SCISSORS, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.PAPER]
		self.loseStreak = 0
		self.pos = 0

	def moveListener(self, move):
		if move['player1'] == self.name:
			me = move['move1']
			enemy = move['move2']
		elif move['player2'] == self.name:
			me = move['move2']
			enemy = move['move1']
		else:
			return

		self.pos = move['pos'] + 1
		if enemy > me:
			self.loseStreak += 1
		else:
			self.loseStreak = 0


	def matchListener(self, match):
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.loseStreak = 0
			self.pos = 0

	def getMove(self):
		return self.order[self.pos % 10] if self.loseStreak < 5 else PlayerMove.ROCK

class Cycler(BaseStrategy):
	def __init__(self):
		self.name = 'Cycler'
		self.order = [PlayerMove.ROCK, PlayerMove.PAPER, PlayerMove.ROCK, PlayerMove.SCISSORS, PlayerMove.PAPER, PlayerMove.SCISSORS, PlayerMove.SCISSORS, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.PAPER]
		self.pos = 0

	def moveListener(self, move):
		if move['player1'] == self.name or move['player2'] == self.name:
			self.pos = move['pos'] + 1

	def matchListener(self, match):
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.pos = 0

	def getMove(self):
		return self.order[self.pos % len(self.order)]

class Adam(BaseStrategy):
	def __init__(self):
		self.name = 'Adam'
		self.enemyLast = None
		self.meLast = None
		self.consecLoses = 0
		self.totalDraws = 0
		self.state = 1

	def matchListener(self, match):
		if match['event'] == 'start' and (match['player1'] == self.name or match['player2'] == self.name):
			self.options = [PlayerMove.SCISSORS, PlayerMove.SCISSORS, PlayerMove.SCISSORS, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.ROCK, PlayerMove.PAPER, PlayerMove.PAPER, PlayerMove.PAPER]
			self.meLast = None
			self.enemyLast = None
			self.consecLoses = 0
			self.totalDraws = 0
			self.state = 1

	def moveListener(self, move):
		if move['player1'] == self.name:
			me = move['move1']
			enemy = move['move2']
		elif move['player2'] == self.name:
			me = move['move2']
			enemy = move['move1']
		else:
			return
		if me < enemy:
			self.consecLoses += 1
		else:
			self.consecLoses = 0

		if me == enemy:
			self.totalDraws += 1

		if self.consecLoses >= 6 or self.totalDraws >= 8 or self.state == 10:
			self.state = 10
		else:
			self.state = (self.state - 1) % 8 + 2

		self.meLast = me
		self.enemyLast = enemy

	def getMove(self):
		retVal = None
		if self.state == 1:
			return PlayerMove.PAPER
		elif self.state == 10:
			retVal = self.enemyLast
		else:
			if self.meLast > self.enemyLast:
				retVal = self.meLast
			elif self.meLast == self.enemyLast:
				retVal = self.options[self.state - 2]
			else:
				lst = [PlayerMove.ROCK, PlayerMove.PAPER, PlayerMove.SCISSORS]
				lst.remove(self.meLast)
				lst.remove(self.enemyLast)
				retVal = lst.pop()

		assert retVal != None
		return retVal