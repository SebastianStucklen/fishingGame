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
grass3 = pygame.image.load("resources/grass.png")
bgImage2 = pygame.transform.scale2x(grass3)
bgImage = bgImage2

ct = CursorTools(screen,defaultImg,interactImg)

guy = Player(1)
lake = FishingHole()
deltalist = []
teste1 = Fishes()
inv = TextDisplay(guy.inventory,5,5,32)
market = SellStation()
viewInv = False

def doNothing():
	return True
gamestate = "main"

tutorial(screen)

pressDown = False

while not doExit:
	delta = clock.tick(FPS) / 1000
	pressDown = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True #lets you quit program
		if event.type == pygame.KEYDOWN and get_pressed()[pygame.K_e]:
			gamestate = "inventory"
		if event.type == pygame.MOUSEBUTTONDOWN:
			pressDown = True

		
	screen.blit(bgImage,(0,0))
	#--------------------------------- MAIN ----------------------------------------
	if gamestate == "main":
		
		whatfish = fishgen()
		if ct.playerInteract(lake.rect,guy.centerpos, lambda: doNothing()):
			gamestate = "lake"

		lake.draw(screen)

		guy.update(delta,screen)

		market.draw(screen)


		ct.playerInteract(market.rect,guy.centerpos, lambda: market.select(True), 400, pressDown)
		market.drawButtons(screen)
	#--------------------------------- LAKE ----------------------------------------
	if gamestate == "lake":
		whatfish = fishgen()
		if lake.quicktime(screen,delta,whatfish[1]):
			guy.inventory.append(speciesGen(whatfish[0]))
			for i in range(len(guy.inventory)-1):
				guy.inventory[i].toggleBigView(False)
				viewInv = False
			gamestate = "sub-inventory"
	#--------------------------------- INVENTORY ----------------------------------------
	if gamestate == "sub-inventory":
		screen.fill((70, 130, 10))
		newest = len(guy.inventory)-1
		if guy.inventory[newest].bigView == True:
				guy.inventory[newest].caughtDisplay(screen)
				ct.playerInteract(guy.inventory[newest].close, guy.centerpos, lambda: guy.inventory[newest].toggleBigView(False), 1600)
				if get_pressed()[pygame.K_ESCAPE]:
					guy.inventory[newest].toggleBigView(False)
		else:
			gamestate = "main"

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
				guy.inventory[i].caughtDisplay(screen)
				ct.playerInteract(guy.inventory[i].close, guy.centerpos, lambda: guy.inventory[i].toggleBigView(False), 1600)
				if get_pressed()[pygame.K_ESCAPE]:
					guy.inventory[i].toggleBigView(False)
		if get_pressed()[pygame.K_ESCAPE] or ct.playerInteract(Rect(20,20,65,65), guy.centerpos, lambda: doNothing(), 1600):
			gamestate = "main"


	ct.customCursor()
	pygame.display.flip()
pygame.quit()