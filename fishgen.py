import random as rand
from fishes import Fishes, Common1, Common2, Common3, Common4, Common5, Common6, Uncommon1, Uncommon2, Uncommon3, Uncommon4, Rare1, Rare2, Rare3, Epic1, Epic2, Epic3, Legendary1, Legendary2, Legendary3
# Common (60.00% Base Drop Rate)   roll < 100
# Uncommon (26.00% Base Drop Rate) roll < 40
# Rare (10.00% Base Drop Rate)	   roll < 14
# Very Rare (3.00% Base Drop Rate) roll < 4
# Legendary (1.00% Base Drop Rate) roll < 1

#chance upgrade = 3 every time
# each one -9

fishId = ""

def fishgen(chance = 0) -> tuple[str, int]:

	roll = rand.random()
	roll *= 100
	#[Rarity, Game rounds, fish id, money]
	if roll < -8+chance:
		return ("Legendary", 12)
	
	elif roll < -5+chance:
		return ("Epic", 9)
	
	elif roll < 5+chance*2:
		return ("Rare", 6)
	
	elif roll < 31+chance*3:
		return ("Uncommon", 4)
	
	elif roll < 100:
		return ("Common", 3)
	
	else:
		return ("huh", 1)
#FACTORY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def speciesGen(rarity: str) -> Fishes:
	size = rand.random()*1.3+0.7
	match rarity:
		case "Common":
			species = rand.choice([
				Common1,
				Common2,
				Common3,
				Common4,
				Common5,
				Common6,
			])
			return species(size)
		case "Uncommon":
			species = rand.choice([
				Uncommon1,
				Uncommon2,
				Uncommon3,
				Uncommon4,
			])
			return species(size)
		case "Rare":
			species = rand.choice([
				Rare1,
				Rare2,
				Rare3,
			])
			return species(size)
		case "Epic":
			species = rand.choice([
				Epic1,
				Epic2,
				Epic3,
			])
			return species(size)
		case "Legendary":
			species = rand.choice([
				Legendary1,
				Legendary2,
				Legendary3,
			])
			return species(size)
		case _:
			return Fishes()
