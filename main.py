from tournament import *
from strategies import *
resultSetPoints = {}
resultSetWins = {}
observer = Documenter()
for i in range(100):
	if i % 100 == 0:
		print (i//100)
	participants = []
	# participants.append(WaPlayer1())
	# participants.append(Adam())
	# participants.append(Rock())
	# participants.append(Paper())
	# participants.append(BaseStrategy())
	# participants.append(Rand())
	participants.append(Player2())
	participants.append(Player3())
	participants.append(Player4())
	# participants.append(Player5())
	participants.append(Player6())
	participants.append(Player1())
	participants.append(Player7())
	participants.append(Player8())
	# participants.append(Player9())
	participants.append(Player10())

	tournament = Tournament(*participants, observers = [observer], logging = False)
	result = tournament.executeGame()
	points = 2520 // len(result) 
	for p in result:
		if p in resultSetWins:
			resultSetPoints[p] += points
			resultSetWins[p] += 1
		else:
			resultSetPoints[p] = points
			resultSetWins[p] = 1

def resultSetToString(r, format):
	retVal = ''
	retVal += f"Cumulative {format}:\n"
	for player, performance in r.items():
		retVal += f"{player}: {performance} {format}\n"
	
	retVal += '\n'
	return retVal

log = open('cumulative.txt', "w", encoding="utf-8")

log.write(resultSetToString(resultSetWins, 'wins'))
log.write(resultSetToString(resultSetPoints, 'points'))
log.write(observer.toString())

log.close()

print(resultSetToString(resultSetWins, 'wins'))
print(resultSetToString(resultSetPoints, 'points'))
print(observer.toString())

input("Enter any key to quit.")