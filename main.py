import pygame
from pygame import Vector2
from pygame.key import get_pressed
from globals import FPS, SCREEN_SIZE, CursorTools, TextDisplay
from player import Player
from interactables import FishingHole, tutorial, SellStation
from fishgen import fishgen
from fishgen import speciesGen
from fishes import Fishes
from pygame import mixer
pygame.init()
# mixer.init()

doExit = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE))

defaultImg = pygame.image.load("default.png")
# clickableImg = pygame.image.load("clickable.png")
interactImg = pygame.image.load("interact.png")

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

tutorial(screen)

teste3 = False

while not doExit:
	delta = clock.tick(FPS) / 1000
	teste3 = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True #lets you quit program
		if event.type == pygame.KEYDOWN and get_pressed()[pygame.K_e]:
			viewInv = not viewInv
		if event.type == pygame.MOUSEBUTTONDOWN:
			teste3 = True

		
	screen.fill((70, 130, 10))
	
	whatfish = fishgen()
	if ct.playerInteract(lake.rect,guy.centerpos, lambda: lake.quicktime(screen,delta,whatfish[1])):
		guy.inventory.append(speciesGen(whatfish[0]))
		for i in range(len(guy.inventory)-1):
			guy.inventory[i].toggleBigView(False)
			viewInv = False

	lake.draw(screen)

	guy.update(delta,screen)

	market.draw(screen)
	

	ct.playerInteract(market.rect,guy.centerpos, lambda: market.select(True), 400, teste3)
	market.drawButtons(screen)


	teste2 = [1,1]
	for i in range(len(guy.inventory)):
		if guy.inventory[i].bigView == True:
			guy.inventory[i].caughtDisplay(screen)
			ct.playerInteract(guy.inventory[i].close, guy.centerpos, lambda: guy.inventory[i].toggleBigView(False), 1600)
			if get_pressed()[pygame.K_ESCAPE]:
				guy.inventory[i].toggleBigView(False)
		if viewInv:
			guy.inventory[i].invDisplay(screen,teste2)
			if teste2[0] < 1300:
				teste2[0]+=200
			else: 
				teste2[0] = 1
				teste2[1] += 120

	ct.customCursor()
	pygame.display.flip()
pygame.quit()