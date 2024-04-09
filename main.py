import pygame
from pygame import Vector2
from globals import FPS, SCREEN_SIZE, CursorTools, TextDisplay
from player import Player
from interactables import FishingHole
from fishgen import fishgen
from fishes import Fishes
pygame.init()

doExit = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE))

defaultImg = pygame.image.load("default.png")
clickableImg = pygame.image.load("clickable.png")

ct = CursorTools(screen,defaultImg,clickableImg)

guy = Player(1)
lake = FishingHole()
deltalist = []
teste1 = Fishes()
inv = TextDisplay(guy.inventory,5,5,32)



while not doExit:
	delta = clock.tick(FPS) / 1000
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True #lets you quit program
	screen.fill((70, 130, 10))
	canCLICK = ct.playerInteract(lake.rect,guy.centerpos)
	if canCLICK:
		whatfish = fishgen()
		print(whatfish)
		if lake.quicktime(screen,delta,whatfish[1]):
			guy.inventory.append(whatfish[0])
			print(guy.inventory)
	lake.draw(screen)
	guy.update(delta,screen)
	ct.customCursor()
	teste1.caughtDisplay(screen)
	inv.update(screen,guy.inventory,32,(0,0,0))
	
	pygame.display.flip()
pygame.quit()