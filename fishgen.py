import random
from fishes import Fishes, Common1, Common2, Common3, Common4, Common5
# Common (60.00% Base Drop Rate)
# Uncommon (26.00% Base Drop Rate)
# Rare (10.00% Base Drop Rate)
# Very Rare (3.00% Base Drop Rate)
# Legendary (1.00% Base Drop Rate)

#chance upgrade = 18

fishId = ""

def fishgen(chance = 0) -> tuple[str, int]:

    roll = random.random()
    roll *= 100
    #[Rarity, Game rounds, fish id, money]
    if roll < 1:
        return ("Legendary", 12)
    
    elif roll < 4:
        return ("Very Rare", 9)
    
    elif roll < 14:
        return ("Rare", 6)
    
    elif roll < 40:
        return ("Uncommon", 4)
    
    elif roll < 100:
        return ("Common", 3)
    
    else:
        return ("huh", 1)
#FACTORY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def speciesGen(rarity: str) -> Fishes:
    size = random.random()*1.5+0.5
    match rarity:
        case "Common":
            species = random.choice([
                Common1,
                Common2,
                Common3,
                Common4,
                Common5,
            ])
            return species(size)
        case _:
            return Fishes()
