from enum import Enum, auto
class PlayerMove(Enum):
	ROCK = 'Rock'
	PAPER = 'Paper'
	SCISSORS = 'Scissors'

	def __gt__(self, obj):
		if isinstance(obj, PlayerMove):
			return self == PlayerMove.ROCK and obj == PlayerMove.SCISSORS or \
				self == PlayerMove.PAPER and obj == PlayerMove.ROCK or \
				self == PlayerMove.SCISSORS and obj == PlayerMove.PAPER
		else:
			raise TypeError(f'Not instance of PlayerMove{obj}')

	def __ge__(self,obj):
		if isinstance(obj, PlayerMove):
			return self > obj or self == obj
		else:
			raise TypeError(f'Not instance of PlayerMove{obj}')

	def __lt__(self,obj):
		if isinstance(obj, PlayerMove):
			return not self >= obj 
		else:
			raise TypeError(f'Not instance of PlayerMove{obj}')

	def __le__(self,obj):
		if isinstance(obj, PlayerMove):
			return self < obj or self == obj
		else:
			raise TypeError(f'Not instance of PlayerMove{obj}')

def getCounter(move):
	if isinstance(move, PlayerMove):
		return PlayerMove.PAPER if move == PlayerMove.ROCK else PlayerMove.SCISSORS if move == PlayerMove.PAPER else PlayerMove.ROCK
	else:
		raise TypeError(f'Not instance of PlayerMove{obj}')

def getNotCounter(move):
	if isinstance(move, PlayerMove):
		return PlayerMove.PAPER if move == PlayerMove.SCISSORS else PlayerMove.SCISSORS if move == PlayerMove.ROCK else PlayerMove.ROCK
	else:
		raise TypeError(f'Not instance of PlayerMove{obj}')

def toRPS(seq):
	ret = []
	for s in seq:
		if s == 's':
			ret.append(PlayerMove.SCISSORS)
		elif s == 'p':
			ret.append(PlayerMove.PAPER)
		elif s == 'r':
			ret.append(PlayerMove.ROCK)
		else:
			raise Exception
	return ret

if __name__ == "__main__":
	print(f'PlayerMove.ROCK > PlayerMove.PAPER: {PlayerMove.ROCK > PlayerMove.PAPER}, Expected: False')
	print(f'PlayerMove.ROCK >= PlayerMove.PAPER: {PlayerMove.ROCK >= PlayerMove.PAPER}, Expected: False')
	print(f'PlayerMove.ROCK < PlayerMove.PAPER: {PlayerMove.ROCK < PlayerMove.PAPER}, Expected: True')
	print(f'PlayerMove.ROCK <= PlayerMove.PAPER: {PlayerMove.ROCK <= PlayerMove.PAPER}, Expected: True')
	print(f'PlayerMove.ROCK == PlayerMove.PAPER: {PlayerMove.ROCK == PlayerMove.PAPER}, Expected: False')
	print(f'PlayerMove.ROCK > PlayerMove.ROCK: {PlayerMove.ROCK > PlayerMove.ROCK}, Expected: False')
	print(f'PlayerMove.ROCK >= PlayerMove.ROCK: {PlayerMove.ROCK >= PlayerMove.ROCK}, Expected: True')
	print(f'PlayerMove.ROCK < PlayerMove.ROCK: {PlayerMove.ROCK < PlayerMove.ROCK}, Expected: False')
	print(f'PlayerMove.ROCK <= PlayerMove.ROCK: {PlayerMove.ROCK <= PlayerMove.ROCK}, Expected: True')
	print(f'PlayerMove.ROCK == PlayerMove.ROCK: {PlayerMove.ROCK == PlayerMove.ROCK}, Expected: True')
	print(f'PlayerMove.PAPER > PlayerMove.ROCK: {PlayerMove.PAPER > PlayerMove.ROCK}, Expected: True')
	print(f'PlayerMove.PAPER >= PlayerMove.ROCK: {PlayerMove.PAPER >= PlayerMove.ROCK}, Expected: True')
	print(f'PlayerMove.PAPER < PlayerMove.ROCK: {PlayerMove.PAPER < PlayerMove.ROCK}, Expected: False')
	print(f'PlayerMove.PAPER <= PlayerMove.ROCK: {PlayerMove.PAPER <= PlayerMove.ROCK}, Expected: False')
	print(f'PlayerMove.PAPER == PlayerMove.ROCK: {PlayerMove.PAPER == PlayerMove.ROCK}, Expected: False')
