import pygame
from pygame import Rect
from pygame.key import get_pressed
from globals import FPS, SCREEN_SIZE, CursorTools, TextDisplay
from player import Player
from interactables import FishingHole, tutorial, SellStation
from fishgen import fishgen
from fishgen import speciesGen
from fishes import Fishes
# from pygame import mixer
pygame.init()

# mixer.init()

close = pygame.image.load('resources/close.png')

doExit = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE))

defaultImg = pygame.image.load("default.png")
# clickableImg = pygame.image.load("clickable.png")
interactImg = pygame.image.load("interact.png")
bgImage = pygame.image.load("resources/grass.png")
bgImage2 = pygame.transform.scale_by(bgImage,2)
bgImage = bgImage2

font = pygame.font.Font(None, 60)

ct = CursorTools(screen,defaultImg,interactImg)
guy = Player(1)
lake = FishingHole()
deltalist = []
teste1 = Fishes()
inv = TextDisplay(guy.inventory,5,5,32)
market = SellStation()
viewInv = False
newest = 0


def doNothing():
	return True
gamestate = "main"

tutorial(screen)

pressDown = False
unpress = False
while not doExit:
	delta = clock.tick(FPS) / 1000
	pressDown = False
	unpress = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True #lets you quit program
		if event.type == pygame.KEYDOWN and get_pressed()[pygame.K_e]:
			gamestate = "inventory"
		if event.type == pygame.MOUSEBUTTONDOWN:
			pressDown = True
		if event.type == pygame.MOUSEBUTTONUP:
			unpress = True
			print("dvuaywDIViuawvcduiaywcdiuawcdvw")


		
	screen.blit(bgImage,(0,0))
	#--------------------------------- MAIN ----------------------------------------
	if gamestate == "main":
		
		if ct.playerInteract(lake.rect,guy.centerpos, doNothing):
			gamestate = "lake"

		lake.draw(screen)

		

		market.draw(screen)

		guy.update(delta,screen)

		text = font.render(f"fishbux: {str(guy.money)}",1,(20,30,0))
		screen.blit(text,(10,10))

		if ct.playerInteract(market.rect,guy.centerpos, lambda: market.select(True), 400, pressDown):
			gamestate = "market"
	#--------------------------------- MARKET ----------------------------------------
	if gamestate == "market":
		market.drawButtons(screen)
		if ct.playerInteract(market.upgRect, guy.centerpos, lambda: market.upgButton(), 1600):
			gamestate = "upgrading"
		if ct.playerInteract(market.sellRect, guy.centerpos, lambda: market.sellButton(), 1600):
			gamestate = "selling"

	if gamestate == "upgrading":
		text = font.render("UPGRADE",1,(20,30,0))
		textrect = text.get_rect()
		textrect.topleft = (650,450)
		screen.blit(text,(650,450))
		if ct.playerInteract(textrect, guy.centerpos, lambda: guy.upgrade(), 1600):
			print(guy.chance)
			gamestate = "main"
	if gamestate == "selling":
		screen.fill((70, 130, 10))
		teste2 = [100,1]
		screen.blit(close, (20,20))
		i = 0
		while i < len(guy.inventory):
			guy.inventory[i].invDisplay(screen,teste2)
			if teste2[0] < 1300:
				teste2[0]+=200
			else: 
				teste2[0] = 1
				teste2[1] += 120
			if ct.playerInteract(guy.inventory[i].invImgRect, guy.centerpos, doNothing,1600):
				guy.money+=guy.inventory[i].price
				guy.inventory.pop(i)
				i=-1
			i+=1
			
		if get_pressed()[pygame.K_ESCAPE] or ct.playerInteract(Rect(20,20,65,65), guy.centerpos, doNothing, 1600):
			gamestate = "main"
	#----------------pass----------------- LAKE ----------------------------------------
	if gamestate == "lake":
		whatfish = fishgen(guy.chance)
		if lake.quicktime(screen,delta,whatfish[1]):
			guy.inventory.append(speciesGen(whatfish[0]))
			for i in range(len(guy.inventory)-1):
				guy.inventory[i].toggleBigView(False)
				viewInv = False
			newest = len(guy.inventory)-1
			gamestate = "sub-inventory1"
	#--------------------------------- INVENTORY ----------------------------------------
	if gamestate == "sub-inventory1":
		screen.fill((70, 130, 10))
		if guy.inventory[newest].bigView == True:
				guy.inventory[newest].caughtDisplay(screen)
				ct.playerInteract(guy.inventory[newest].close, guy.centerpos, lambda: guy.inventory[newest].toggleBigView(False), 1600)
				if get_pressed()[pygame.K_ESCAPE]:
					guy.inventory[newest].toggleBigView(False)
					gamestate = "main"
		else:
			gamestate = "main"
	
	if gamestate == "sub-inventory2":
		screen.fill((70, 130, 10))
		if guy.inventory[newest].bigView == True:
				guy.inventory[newest].caughtDisplay(screen)
				ct.playerInteract(guy.inventory[newest].close, guy.centerpos, lambda: guy.inventory[newest].toggleBigView(False), 1600)
				if get_pressed()[pygame.K_ESCAPE]:
					guy.inventory[newest].toggleBigView(False)
					gamestate = "inventory"
		else:
			gamestate = "inventory"

	if gamestate == "inventory":
		screen.fill((70, 130, 10))
		teste2 = [100,1]
		screen.blit(close, (20,20))
		for i in range(len(guy.inventory)):
			guy.inventory[i].invDisplay(screen,teste2)
			if teste2[0] < 1300:
				teste2[0]+=200
			else: 
				teste2[0] = 1
				teste2[1] += 120
			ct.playerInteract(guy.inventory[i].invImgRect, guy.centerpos, lambda: guy.inventory[i].toggleBigView(True),1600)
			if guy.inventory[i].bigView == True:
				newest = i
				gamestate = "sub-inventory2"
				# guy.inventory[i].caughtDisplay(screen)
				# ct.playerInteract(guy.inventory[i].close, guy.centerpos, lambda: guy.inventory[i].toggleBigView(False), 1600)
				# if get_pressed()[pygame.K_ESCAPE]:
				# 	guy.inventory[i].toggleBigView(False)
		if get_pressed()[pygame.K_ESCAPE] or ct.playerInteract(Rect(20,20,65,65), guy.centerpos, doNothing, 1600):
			gamestate = "main"


	ct.customCursor()
	pygame.display.flip()
pygame.quit()