from player_move import *
import random

class Tournament:
	def __init__(self, *participants, output = 'output.txt', observers = None, logging = True):
		self.logging = logging
		if logging:
			self.log = open(output, "w", encoding="utf-8")

		self.participants = {p.name: p for p in participants}
		self.moveAnnouncer = EventDispatcher()  #Announces player moves result (announce what the two picked)
		self.matchAnnouncer = EventDispatcher() #Announces match (starting match between two players)
		self.roundAnnouncer = EventDispatcher() #Announces round (list of players)

		for participant in participants:
			self.moveAnnouncer.addListener(participant.moveListener)
			self.matchAnnouncer.addListener(participant.matchListener)
			self.roundAnnouncer.addListener(participant.roundListener)

		for observer in observers:
			self.moveAnnouncer.addListener(observer.moveListener)
			self.matchAnnouncer.addListener(observer.matchListener)
			self.roundAnnouncer.addListener(observer.roundListener)

		self.currentPlayers = [p.name for p in participants]
		self.currentMatches = []
		self.currentResults = {}

	def _generateMatches(self):
		# I hate myself for writing codes so ugly... but it's soooo convenient
		self.currentMatches = [[self.currentPlayers[p], self.currentPlayers[q]] for p in range(len(self.currentPlayers)) for q in range(len(self.currentPlayers)) if p < q]
		random.shuffle(self.currentMatches)
		self.currentResults = {p: {q: None for q in self.currentPlayers if p is not q} for p in self.currentPlayers}

	def _executeMove(self, player1, player2, pos):
		move1 = self.participants[player1].getMove()
		move2 = self.participants[player2].getMove()

		self.moveAnnouncer.broadcast({
				'player1': player1,
				'player2': player2,
				'move1': move1,
				'move2': move2,
				'pos': pos,
			})

		return move1, move2

	def _executeMatch(self, player1, player2):
		win1 = 0
		win2 = 0
		draw = 0
		movePos = 0

		if self.logging:
			self.log.write(f'Starting match between {player1} and {player2}\n')
		self.matchAnnouncer.broadcast({
				'player1': player1,
				'player2': player2,
				'event': 'start',
			})

		while win1 < 10 and win2 < 10:
			if draw >= 500:
				if self.logging:
					self.log.write(f'Stalemate!\n')
				break

			# Executing a single move
			move1, move2 = self._executeMove(player1, player2, movePos)

			msg = 'ERR' #this should change
			if move1 > move2:
				win1 += 1
				msg = f'{player1} wins!'
			elif move1 < move2:
				win2 += 1
				msg = f'{player2} wins!'
			else:
				draw += 1
				msg = "it's a draw!"
			if self.logging:
				self.log.write(f'Turn {movePos}: {player1} plays {move1.value}, {player2} plays {move2.value}, {msg}\n')
			movePos += 1

		result = player1 if win1 == 10 else player2 if win2 == 10 else 'draw'
		
		if result == 'draw':
			if self.logging:
				self.log.write(f'Match ended in a draw!\n\n')
			self.currentResults[player1][player2] = 'draw'
			self.currentResults[player2][player1] = 'draw'
		else:
			if self.logging:
				self.log.write(f'Player {result} won the match!\n\n')
			self.currentResults[player1][player2] = 'win' if result == player1 else 'lose'
			self.currentResults[player2][player1] = 'lose' if result == player1 else 'win'

		self.matchAnnouncer.broadcast({
			'player1': player1,
			'player2': player2,
			'event': 'end',
			'result': result,
		})

	def _executeRound(self):
		self.roundAnnouncer.broadcast({
			'event': 'start',
			'players': self.currentPlayers,
		})
		if self.logging:
			self.log.write(f"Here's our contestants for this round: {', '.join(self.currentPlayers)}!\n")

		self._generateMatches()
		assert len(self.currentMatches) > 0

		while self.currentMatches:
			player1, player2 = self.currentMatches.pop()
			self._executeMatch(player1,player2)

		worst = self._findWorst()
		stats = self._generateStats()
		if self.logging:
			self.log.write(f"Round ended! Here's the score!\n")
		for p in self.currentPlayers:
			if self.logging:
				self.log.write(f"{p}: {stats[p]['wins']} wins, {stats[p]['loses']} loses, {stats[p]['draws']} draws\n")
		if self.logging:
			self.log.write(f"The following contestants dropped out: {' '.join(worst)}\n\n")

		self.currentPlayers = [p for p in self.currentPlayers if p not in worst]

		self.roundAnnouncer.broadcast({
			'event': 'end',
			'dropout': worst,
		})


	def _generateStats(self):
		stats = {p: {'wins': 0, 'loses': 0, 'draws': 0} for p in self.currentPlayers}
		for p in self.currentPlayers:
			for r,v in self.currentResults[p].items():
				assert v is not None
				stats[p]['wins'] += 1 if v == 'win' else 0
				stats[p]['loses'] += 1 if v == 'lose' else 0
				stats[p]['draws'] += 1 if v == 'draw' else 0
		return stats

	def _findWorst(self):
		stats = self._generateStats()

		min_win = min([v['wins'] for p,v in stats.items()])
		max_lose_in_min_win = max([v['loses'] for p,v in stats.items() if v['wins'] == min_win])
		worst_players = [p for p in stats if stats[p]['wins'] == min_win and stats[p]['loses'] == max_lose_in_min_win]

		assert len(worst_players) > 0

		if len(worst_players) == 1:
			return worst_players

		worst_of_worst = []
		for p in worst_players:
			for p2 in worst_players:
				if p is not p2 and self.currentResults[p][p2] == 'win':
					break
			else:
				worst_of_worst.append(p)

		if len(worst_of_worst) > 0:
			return worst_of_worst
		else:
			return worst_players

	def executeGame(self):
		if self.logging:
			self.log.write(f"The tournament has begun!\n")
		draws = []
		result = None
		while len(self.currentPlayers) > 1:
			draws = self.currentPlayers
			self._executeRound()

		if len(self.currentPlayers) == 1:
			if self.logging:
				self.log.write(f"Congratulations to {self.currentPlayers[0]} for winning the tournament!\n")
			result = self.currentPlayers
		if len(self.currentPlayers) == 0:
			if self.logging:
				self.log.write(f"Looks like there's no apparent victor! The following players tied for top place: {' '.join(draws)}\n")
			result = draws
		if self.logging:
			self.log.close()
		return result

class EventDispatcher:
	def __init__(self):
		self.listeners = []

	def addListener(self, listener):
		self.listeners.append(listener)

	def removeListener(self, listener):
		if listener in self.listeners:
			self.listeners.remove(listener)

	def broadcast(self, *data):
		for listener in self.listeners:
			listener(*data)
			# try:
			# except:
			# 	print(f'Error broadcasting {data} to {listener}')