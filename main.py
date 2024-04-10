import pygame
from pygame import Vector2
from globals import FPS, SCREEN_SIZE, CursorTools, TextDisplay
from player import Player
from interactables import FishingHole
from fishgen import fishgen
from fishgen import speciesGen
from fishes import Fishes
pygame.init()

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

opadna = [



]

while not doExit:
	delta = clock.tick(FPS) / 1000
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True #lets you quit program
	screen.fill((70, 130, 10))
	
	whatfish = fishgen()
	if ct.playerInteract(lake.rect,guy.centerpos, lambda: lake.quicktime(screen,delta,whatfish[1])):
		print(whatfish)
		guy.inventory.append(speciesGen(whatfish[0]))
		for i in range(len(guy.inventory)-1):
			guy.inventory[i].toggleInventoryView()
		print(guy.inventory)

	lake.draw(screen)
	guy.update(delta,screen)
	# inv.update(screen,guy.inventory,32,(0,0,0))
	for i in range(len(guy.inventory)):
		guy.inventory[i].caughtDisplay(screen)
		ct.playerInteract(guy.inventory[i].close, guy.centerpos, lambda: guy.inventory[i].toggleInventoryView(), 1600)

	ct.customCursor()
	pygame.display.flip()
pygame.quit()