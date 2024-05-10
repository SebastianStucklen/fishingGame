gameVersion = "1.1.3.2"

import pickle

import pygame
from globals import FPS, SCREEN_SIZE, CursorTools, SCREEN_RECT
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE))

from pygame import Rect
from pygame.key import get_pressed
from pygame import mixer as Music

from player import Player
from interactables import FishingHole, tutorial, SellStation, invTutorial, Home, mute
from fishgen import fishgen
from fishgen import speciesGen
from fishes import Fishes

# from pygame import mixer
Music.init()



doExit = False
clock = pygame.time.Clock()

close = pygame.image.load('resources/close.png').convert_alpha()
yes = pygame.image.load('resources/yes.png').convert_alpha()
cornerX = Rect(20,20,65,65)

interactImg = pygame.image.load("resources/interact.png").convert_alpha()
bgImage 	= pygame.image.load("resources/grass5.png").convert()

shopImg		= pygame.image.load("resources/shop1.png").convert_alpha()
titleImg	= pygame.image.load("resources/title.png").convert()

invImg		= pygame.image.load("resources/sack.png").convert()
statsImg	= pygame.image.load("resources/stats.png").convert()
settingImg 	= pygame.image.load("resources/settings.png").convert()
menuImg 	= pygame.image.load("resources/menuBG.png").convert()
invBgImg	= pygame.image.load("resources/menuBG2.png").convert()
setMenuImg	= pygame.image.load('resources/menuBG_lazy.png').convert()
menuRect	= Rect(400,200,800,500)
menuRect2	= Rect(300,50,1000,600)
unmuted		= pygame.image.load("resources/unmuted.png").convert_alpha()
muted		= pygame.image.load("resources/muted.png").convert_alpha()
muteRect	= Rect(870,140,260,260)
quitButton	= pygame.image.load("resources/close_game.png").convert()
quitRect	= Rect(360,140,480,260)

shop = Music.Sound('resources/elevator.mp3')
waves = Music.Sound('resources/waves.wav')
Music.music.load('resources/thejazzpiano.mp3')
isMuted = False

font = pygame.font.Font(None, 52)
fontBig = pygame.font.Font(None, 80)
temp7 = font.render(f"V {gameVersion}",1,(0,0,0))

ct = CursorTools(interactImg)

guy = Player(1)

lake = FishingHole()
market = SellStation()
marketpage = 0
home = Home()
newest = 0
sellwhat = 0

def doNothing():
	return True


titlepage = True
Music.Sound.play(waves,-1)
Music.Sound.play(waves,-1)
while titlepage:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			titlepage = False
	screen.blit(titleImg,(0,0))
	pygame.display.flip()

try:
	with open("playersave.txt", "rb") as load_file:
		temp4 = pickle.load(load_file)
	guy.loadData(temp4)
except:
	pass


screen.fill((153,217,234))

tutorial(screen)
tutorials = [False,False,False]
Music.Sound.stop(waves)

pressDown = False
unpress = False

gameTime = 0 
deltaList = []
quitTick = 0

Music.music.play(-1)
Music.music.set_volume(0.7)

gamestate = "main"

while not doExit:
	delta = clock.tick(FPS) / 1000
	deltaList.append(delta)
	gameTime += delta
	if round(gameTime,3) % 0.5 < delta:
		deltaList.sort()
		print(
			"GAMETIME: ", round(gameTime,1), " --- ",
			"MIN: ", deltaList[0], " --- ",
			"MED: ", deltaList[(len(deltaList)//2)-1], " --- ",
			"MAX: ", deltaList[len(deltaList)-1], " --- ",
			"GAMESTATE: ", gamestate, " --- ",
		)
		deltaList.clear()
	if round(gameTime,4) % 30 < delta:
		savestate = guy.saveData()
		print("AUTOSAVING...")

	pressDown = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gamestate = "quit" #lets you quit program
			quitTick+=1
		if event.type == pygame.KEYDOWN and get_pressed()[pygame.K_e]:
			gamestate = "inventory"
		if event.type == pygame.MOUSEBUTTONDOWN:
			pressDown = True
			
	if gamestate == "quit":
		pygame.draw.rect(screen,(239,228,176),(400,200,800,600))
		pygame.draw.rect(screen,(0,0,0),(400,200,800,600),20)
		quitText = font.render("Would you like to quit?",1,(235,0,0),(239,228,176))
		temp1 = quitText.get_rect()
		temp1.center = SCREEN_RECT.center
		quitText2 = font.render("All the fish in your inventory will be sold",1,(0,0,0))
		temp2 = close.get_rect()
		temp3 = temp2.copy()
		temp2.center = (SCREEN_RECT.centerx-200,SCREEN_RECT.centery+100)
		temp3.center = (SCREEN_RECT.centerx+200,SCREEN_RECT.centery+100)
		screen.blit(quitText,(temp1.x,temp1.y-60))
		screen.blit(quitText2,(temp1.x-150,temp1.y))
		screen.blit(close,temp2)
		screen.blit(yes,temp3)
		if ct.clickInteract(temp2):
			gamestate = "main"
			quitTick = 0
			pygame.mouse.set_pos(800,500)
		if ct.clickInteract(temp3):
			doExit = True
	if quitTick >=2:
		doExit = True
	
	if gamestate == "wipe":
		pygame.draw.rect(screen,(239,228,176),(400,200,800,600))
		pygame.draw.rect(screen,(0,0,0),(400,200,800,600),20)
		quitText = font.render("Are you sure you want to wipe your save?",1,(235,0,0),(239,228,176))
		temp1 = quitText.get_rect()
		temp1.center = SCREEN_RECT.center
		quitText2 = font.render("Consider deeply, brainiac",1,(0,0,0))
		temp2 = close.get_rect()
		temp3 = temp2.copy()
		temp2.center = (SCREEN_RECT.centerx-200,SCREEN_RECT.centery+100)
		temp3.center = (SCREEN_RECT.centerx+200,SCREEN_RECT.centery+100)
		screen.blit(quitText,(temp1.x,temp1.y-60))
		screen.blit(quitText2,(temp1.x+120,temp1.y))
		screen.blit(close,temp2)
		screen.blit(yes,temp3)
		if ct.clickInteract(temp2):
			gamestate = "main"
			quitTick = 0
			pygame.mouse.set_pos(800,500)
		if ct.clickInteract(temp3):
			open("playersave.txt", "w").close()
			quit()

	#-------------------------------------- MAIN ----------------------------------------
	if gamestate == "main":
		screen.blit(bgImage,(0,0))

		if guy.bait > 0 and len(guy.inventory) < guy.bagsize:
			if ct.playerInteract(lake.rect,guy.centerpos, doNothing, 400, pressDown):
				guy.bait-=1
				gamestate = "lake"

		# lake.draw(screen)


		market.draw(screen)
		home.draw(screen)

		if lake.rect.colliderect(guy.rect) or home.rect.colliderect(guy.rect):
			guy.reverseVel()

		guy.update(delta,screen)

		screen.blit(invImg,(640,800))
		screen.blit(settingImg,(750,800))
		screen.blit(statsImg,(860,800))
		if ct.clickInteract(Rect(640,800,100,100)):
			gamestate = "inventory"
		if ct.clickInteract(Rect(860,800,100,100)):
			gamestate = "statscreen"
		if ct.clickInteract(Rect(750,800,100,100)):
			gamestate = "settings"
		if ct.playerInteract(market.rect,guy.centerpos, lambda: market.select(True), 400, pressDown):
			gamestate = "market"


		if len(guy.inventory) >= guy.bagsize:
			if lake.rect.collidepoint(pygame.mouse.get_pos()):
				text = font.render("you're out of space!",1,(0,0,0))
				screen.blit(close, pygame.mouse.get_pos())
				screen.blit(text,(pygame.mouse.get_pos()[0]+80,pygame.mouse.get_pos()[1]))
		elif guy.bait < 1:
			if lake.rect.collidepoint(pygame.mouse.get_pos()):
				text = font.render("you're out of bait!",1,(0,0,0))
				screen.blit(close, pygame.mouse.get_pos())
				screen.blit(text,(pygame.mouse.get_pos()[0]+80,pygame.mouse.get_pos()[1]))

		
		screen.blit(temp7,(760,10))		
	
	#-------------------------------------- MARKET ----------------------------------------
	if gamestate == "market":
		Music.music.pause()
		screen.fill((176, 115, 82))
		if Music.get_busy() == False:
			Music.Sound.play(shop, -1)

		market.drawButtons(screen)
		
		screen.blit(close, (20,20))

		if ct.clickInteract(market.upgRect, True, market.upgButton):
			gamestate = "upgrading"
		if ct.clickInteract(market.sellRect, True, market.sellButton):
			gamestate = "selling"
		if get_pressed()[pygame.K_ESCAPE] or ct.clickInteract(Rect(20,20,65,65), pressDown):
			gamestate = "main"	
	#-------------------- upgrades -------------------
	elif gamestate == "upgrading":
		screen.fill((151, 70, 23))
		screen.blit(shopImg,(0,0))

		if marketpage == 0:
			market.baitPage(screen)
			ct.clickInteract(market.buyRect, pressDown, lambda: guy.baitUp(market.baitPrice))
			if ct.clickInteract(market.nextRect, pressDown):
				marketpage = 1
		elif marketpage == 1:
			market.bonusBaitPage(screen)
			if ct.clickInteract(market.buyRect, pressDown, lambda: guy.bonusUp(market.bonusBaitPrice[market.bonusBaitBought])):
				market.bonusBaitBought -= 1

			if ct.clickInteract(market.nextRect, pressDown):
				marketpage = 2

		elif marketpage == 2:
			market.chancePage(screen)
			if market.chanceBought >= -4:
				if ct.clickInteract(market.buyRect, pressDown, lambda: guy.upgradeChance(market.chancePrice[market.chanceBought])):
					market.chanceBought-=1
			if ct.clickInteract(market.nextRect, pressDown):
				marketpage = 3
		elif marketpage == 3:
			market.bagPage(screen)
			if market.bagBought >= -4:
				if ct.clickInteract(market.buyRect, pressDown, lambda: guy.upgradeBag(market.bagPrice[market.bagBought])):
					market.bagBought-=1
			if ct.clickInteract(market.nextRect, pressDown):
				marketpage = 0

		

		if get_pressed()[pygame.K_ESCAPE] or ct.clickInteract(market.close, pressDown):
			market.select(True)
			gamestate = "market"
	#-------------------- selling -------------------
	elif gamestate == "selling":
		screen.blit(invBgImg,(0,0))
		screen.blit(close, (20,20))
		if len(guy.inventory)>0:
			temp5 = [100,1]
			temp6 = 0
			while temp6 < len(guy.inventory):
				guy.inventory[temp6].invDisplay(screen,temp5)
				if temp5[0] < 1300:
					temp5[0]+=200
				else: 
					temp5[0] = 1
					temp5[1] += 120
				market.drawButtons(screen)
				if ct.clickInteract(guy.inventory[temp6].invImgRect, pressDown):
					market.selling(True)
					sellwhat = temp6
				if market.isSelling and ct.clickInteract(market.sharedRect, pressDown):
					guy.money+=guy.inventory[sellwhat].price
					guy.inventory.pop(sellwhat)
					market.selling(False)
					sellwhat = 0
					temp6=-1
				temp6+=1
				ct.customCursor(screen)

		if get_pressed()[pygame.K_ESCAPE] or ct.clickInteract(cornerX):
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
			for temp6 in range(len(guy.inventory)-1):
				guy.inventory[temp6].toggleBigView(False)
			newest = len(guy.inventory)-1
			gamestate = "sub-inventory1"
		else:
			gamestate = "main"

	#-------------------------------------- INVENTORY ----------------------------------------
	if gamestate == "sub-inventory1":
		screen.fill((70, 130, 10))
		if guy.inventory[newest].bigView == True:
				guy.inventory[newest].caughtDisplay(screen)
				ct.clickInteract(guy.inventory[newest].close, True, lambda: guy.inventory[newest].toggleBigView(False))
				if get_pressed()[pygame.K_ESCAPE]:
					guy.inventory[newest].toggleBigView(False)
		else:
			gamestate = "main"	
	if gamestate == "sub-inventory2":	
		screen.fill((70, 130, 10))
		if guy.inventory[newest].bigView == True:
				guy.inventory[newest].caughtDisplay(screen)
				ct.clickInteract(guy.inventory[newest].close, True, lambda: guy.inventory[newest].toggleBigView(False))
				if get_pressed()[pygame.K_ESCAPE]:
					guy.inventory[newest].toggleBigView(False)
					gamestate = "inventory"
		else:
			gamestate = "inventory"
	if gamestate == "inventory":
		screen.blit(invBgImg,(0,0))
		screen.blit(close, (20,20))
		if len(guy.inventory) > 0:
			temp5 = [100,1]
			for temp6 in range(len(guy.inventory)):
				guy.inventory[temp6].invDisplay(screen,temp5)
				if temp5[0] < 1300:
					temp5[0]+=200
				else: 
					temp5[0] = 1
					temp5[1] += 120
				if tutorials[0] == True:
					if ct.clickInteract(guy.inventory[temp6].invImgRect, True, lambda: guy.inventory[temp6].toggleBigView(True)):
						newest = temp6
						gamestate = "sub-inventory2"
				ct.customCursor(screen)
		if get_pressed()[pygame.K_ESCAPE] or ct.clickInteract(Rect(20,20,65,65)):
			gamestate = "main"
		if tutorials[0] == False:
			tutorials[0] = invTutorial(screen)
	#-------------------------------------- MENUS -------------------------------------------
	if gamestate == "statscreen":
		screen.blit(menuImg,menuRect)
		screen.blit(close,(1120,220))
		guy.statDisplay(screen,gamestate)
		if ct.clickInteract(Rect(1120,220,60,60)) or get_pressed()[pygame.K_ESCAPE]:
			gamestate = "main"
	else:
		guy.statDisplay(screen)
	
	if gamestate == "settings":
		version = fontBig.render(gameVersion,1,(0,0,0))

		screen.blit(setMenuImg,menuRect2)
		screen.blit(close,(1180,100))
		screen.blit(version,(490,525))
		screen.blit(quitButton,quitRect)
		if isMuted:
			screen.blit(muted,muteRect)
		else:
			screen.blit(unmuted,muteRect)


		if ct.clickInteract(muteRect,pressDown) and isMuted == False:
			Music.Sound.set_volume(shop,0)
			Music.music.set_volume(0)
			mute(True)
			isMuted = True
		elif ct.clickInteract(muteRect,pressDown) and isMuted:
			Music.Sound.set_volume(shop,1)
			Music.music.set_volume(0.7)
			mute(False)
			isMuted = False
		
		if ct.clickInteract(Rect(555,655,480,56)):
			gamestate = "wipe"


		if ct.clickInteract(quitRect,pressDown):
			gamestate = "quit"

		if ct.clickInteract(Rect(1180,100,60,60)) or get_pressed()[pygame.K_ESCAPE]:
			gamestate = "main"

	ct.customCursor(screen)
	ct.canClick = False
	pygame.display.flip()



for temp6 in range(len(guy.inventory)):
	guy.money+=guy.inventory[temp6].price
guy.inventory.clear()

savestate = guy.saveData()
with open('playersave.txt','wb') as store_file:
	pickle.dump(savestate,store_file)
store_file.close()

pygame.quit()