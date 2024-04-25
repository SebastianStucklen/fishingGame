import pygame
from globals import FPS, SCREEN_SIZE, CursorTools, SCREEN_RECT
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE))

from pygame import Rect
from pygame.key import get_pressed
from pygame import mixer as Music

from player import Player
from interactables import FishingHole, tutorial, SellStation, invTutorial
from fishgen import fishgen
from fishgen import speciesGen
from fishes import Fishes
# from pygame import mixer
Music.init()
close = pygame.image.load('resources/close.png')

doExit = False
clock = pygame.time.Clock()

defaultImg = pygame.image.load("default.png")
interactImg = pygame.image.load("interact.png")
bgImage = pygame.image.load("resources/grass3.png").convert()

font = pygame.font.Font(None, 60)

ct = CursorTools(defaultImg,interactImg)
guy = Player(1)
lake = FishingHole()
teste1 = Fishes()
market = SellStation()
newest = 0
sellwhat = 0

def doNothing():
	return True
gamestate = "main"

tutorial(screen)
tutorials = [False,False,False]

pressDown = False
unpress = False


shop = Music.Sound('resources/elevator.mp3')
Music.music.load('resources/thejazzpiano.mp3')
Music.music.play(-1)
Music.music.set_volume(0.7)

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

	#-------------------------------------- MAIN ----------------------------------------
	if gamestate == "main":
		if ct.playerInteract(lake.rect,guy.centerpos, lambda: doNothing(), 200, pressDown):
			gamestate = "lake"

		lake.draw(screen)

		

		market.draw(screen)

		guy.update(delta,screen)

		text = font.render(f"fishbux: {str(round(guy.money))}",1,(20,30,0))
		screen.blit(text,(10,10))

		if ct.playerInteract(market.rect,guy.centerpos, lambda: market.select(True), 200, pressDown):
			gamestate = "market"

	#-------------------------------------- MARKET ----------------------------------------
	if gamestate == "market":
		Music.music.pause()
		if Music.get_busy() == False:
			Music.Sound.play(shop, -1)
		market.drawButtons(screen)
		if ct.playerInteract(market.upgRect, guy.centerpos, market.upgButton, SCREEN_RECT.w):
			gamestate = "upgrading"
		if ct.playerInteract(market.sellRect, guy.centerpos, market.sellButton, SCREEN_RECT.w):
			gamestate = "selling"

	elif gamestate == "upgrading":
		screen.fill((70, 130, 10))
		screen.blit(close, (20,20))
		text = font.render(str(guy.chance),1,(20,30,0))
		textrect = text.get_rect()
		textrect.topleft = (650,450)
		screen.blit(text,(650,450))
		print(unpress)
		ct.playerInteract(textrect, guy.centerpos, guy.upgrade, SCREEN_RECT.w, pressDown)
		if get_pressed()[pygame.K_ESCAPE] or ct.playerInteract(Rect(20,20,65,65), guy.centerpos, doNothing, SCREEN_RECT.w):
			gamestate = "main"

	elif gamestate == "selling":
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
			market.drawButtons(screen)
			if ct.playerInteract(guy.inventory[i].invImgRect, guy.centerpos, doNothing,SCREEN_RECT.w):
				market.selling(True)
				sellwhat = i
			if market.isSelling and ct.playerInteract(market.sharedRect, guy.centerpos, doNothing, SCREEN_RECT.w):
				guy.money+=guy.inventory[sellwhat].price
				guy.inventory.pop(sellwhat)
				market.selling(False)
				sellwhat = 0
				i=-1
			i+=1

		if get_pressed()[pygame.K_ESCAPE] or ct.playerInteract(Rect(20,20,65,65), guy.centerpos, doNothing, SCREEN_RECT.w):
			gamestate = "main"
	else:
		Music.Sound.stop(shop)
		Music.music.unpause()
		
	#-------------------------------------- LAKE ----------------------------------------
	if gamestate == "lake":
		whatfish = fishgen(guy.chance)
		if lake.quicktime(screen,delta,whatfish[1]):
			guy.inventory.append(speciesGen(whatfish[0]))
			for i in range(len(guy.inventory)-1):
				guy.inventory[i].toggleBigView(False)
			newest = len(guy.inventory)-1
			gamestate = "sub-inventory1"

	#-------------------------------------- INVENTORY ----------------------------------------
	if gamestate == "sub-inventory1":
		screen.fill((70, 130, 10))
		if guy.inventory[newest].bigView == True:
				guy.inventory[newest].caughtDisplay(screen)
				ct.playerInteract(guy.inventory[newest].close, guy.centerpos, lambda: guy.inventory[newest].toggleBigView(False), SCREEN_RECT.w)
				if get_pressed()[pygame.K_ESCAPE]:
					guy.inventory[newest].toggleBigView(False)
		else:
			gamestate = "main"
	
	if gamestate == "sub-inventory2":
		screen.fill((70, 130, 10))
		if guy.inventory[newest].bigView == True:
				guy.inventory[newest].caughtDisplay(screen)
				ct.playerInteract(guy.inventory[newest].close, guy.centerpos, lambda: guy.inventory[newest].toggleBigView(False), SCREEN_RECT.w)
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
			if tutorials[0] == True:
				if ct.playerInteract(guy.inventory[i].invImgRect, guy.centerpos, lambda: guy.inventory[i].toggleBigView(True),SCREEN_RECT.w):
					newest = i
					gamestate = "sub-inventory2"
		if get_pressed()[pygame.K_ESCAPE] or ct.playerInteract(Rect(20,20,65,65), guy.centerpos, doNothing, SCREEN_RECT.w):
			gamestate = "main"
		if tutorials[0] == False:
			tutorials[0] = invTutorial(screen)


	ct.customCursor(screen)
	ct.canClick = False
	pygame.display.flip()


pygame.quit()