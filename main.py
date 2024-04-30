import pygame
from globals import FPS, SCREEN_SIZE, CursorTools, SCREEN_RECT
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE))

from pygame import Rect
from pygame.key import get_pressed
from pygame import mixer as Music

from player import Player
from interactables import FishingHole, tutorial, SellStation, invTutorial, Home
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

font = pygame.font.Font(None, 52)

ct = CursorTools(defaultImg,interactImg)
guy = Player(1)
lake = FishingHole()
teste1 = Fishes()
market = SellStation()
marketpage = 0
home = Home()
newest = 0
sellwhat = 0

def doNothing():
	return True
gamestate = "main"

# tutorial(screen)
tutorials = [False,False,False]

pressDown = False
unpress = False


shop = Music.Sound('resources/elevator.mp3')
Music.music.load('resources/thejazzpiano.mp3')
Music.music.play(-1)
Music.music.set_volume(0.7)

gameTime = 0
deltaList = []
teste6 = 0
while not doExit:
	delta = clock.tick(FPS) / 1000
	deltaList.append(delta)
	gameTime += delta
	if round(gameTime,3) % 0.5 < delta:
		teste6+=1
		deltaList.sort()
		print(
			teste6,
			" --- ",
			"GAMETIME: ", round(gameTime,1), " --- ",
			"MIN: ", deltaList[0], " --- ",
			"MED: ", deltaList[(len(deltaList)//2)-1], " --- ",
			"MAX: ", deltaList[len(deltaList)-1]
		)
		deltaList.clear()
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
		if ct.playerInteract(lake.rect,guy.centerpos, lambda: doNothing(), 200, pressDown) and len(guy.inventory) < guy.bagsize:
			gamestate = "lake"

		lake.draw(screen)


		market.draw(screen)
		home.draw(screen)

		if lake.rect.colliderect(guy.rect):
			guy.reverseVel()

		guy.update(delta,screen)


		if ct.playerInteract(market.rect,guy.centerpos, lambda: market.select(True), 200, pressDown):
			gamestate = "market"
		
		if len(guy.inventory) >= guy.bagsize and lake.rect.collidepoint(pygame.mouse.get_pos()):
			screen.blit(close, pygame.mouse.get_pos())
	
	#-------------------------------------- MARKET ----------------------------------------
	if gamestate == "market":
		Music.music.pause()
		if Music.get_busy() == False:
			Music.Sound.play(shop, -1)
		market.drawButtons(screen)
		if ct.playerInteract(market.upgRect, guy.centerpos, market.upgButton, SCREEN_RECT.w, pressDown):
			gamestate = "upgrading"
		if ct.playerInteract(market.sellRect, guy.centerpos, market.sellButton, SCREEN_RECT.w, pressDown):
			gamestate = "selling"
		

	elif gamestate == "upgrading":
		screen.fill((70, 130, 10))
		if marketpage == 0:
			market.chancePage(screen)
			if ct.playerInteract(market.buyRect, guy.centerpos, lambda: guy.upgradeChance(market.chancePrice[market.chanceBought]), SCREEN_RECT.w, pressDown):
				market.chanceBought+=1

		if get_pressed()[pygame.K_ESCAPE] or ct.playerInteract(market.close, guy.centerpos, doNothing, SCREEN_RECT.w):
			market.select(True)
			gamestate = "market"

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
			if ct.playerInteract(guy.inventory[i].invImgRect, guy.centerpos, doNothing,SCREEN_RECT.w, pressDown):
				market.selling(True)
				sellwhat = i
			if market.isSelling and ct.playerInteract(market.sharedRect, guy.centerpos, doNothing, SCREEN_RECT.w, pressDown):
				guy.money+=guy.inventory[sellwhat].price
				guy.inventory.pop(sellwhat)
				market.selling(False)
				sellwhat = 0
				i=-1
			i+=1

		if get_pressed()[pygame.K_ESCAPE] or ct.playerInteract(Rect(20,20,65,65), guy.centerpos, doNothing, SCREEN_RECT.w):
			market.select(True)
			gamestate = "market"
	
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

	guy.statDisplay()
	ct.customCursor(screen)
	ct.canClick = False
	pygame.display.flip()


pygame.quit()