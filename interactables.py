import pygame
from pygame.math import Vector2
import math
import random

from pygame import Rect
from pygame import draw
from globals import SCREEN_RECT, WHITE, GREEN, BLACK
from pygame import mixer
# mixer	.init()

correct = mixer.Sound("resources/correct.wav")
close = pygame.image.load('resources/close.png')
tutorialBg = pygame.image.load('resources/tutorial.png')
minigameBg = pygame.image.load('resources/minigameBg.png').convert_alpha()
searchBg = pygame.image.load('resources/search.png').convert_alpha()
searchBorder = pygame.image.load('resources/searchBorder.png').convert_alpha()
shadow = pygame.image.load('resources/fishShadow.png').convert_alpha()
rareShadow = pygame.image.load('resources/rareFishShadow.png').convert_alpha()
font = pygame.font.Font(None, 52)

mixer.Sound.set_volume(correct,0.8)

def mute(bewl:bool):
	if bewl:
		mixer.Sound.set_volume(correct,0)
	else:
		mixer.Sound.set_volume(correct,0.8)

class FishingHole:
	
	def __init__(self):
		self.rect = Rect(90,470,520,360)

	def quicktime(self,screen,delta,length) -> bool:
		letterData = []
		player = []
		fish = []
		timer = 0
		fail = False
		screen.fill((0,0,0))
		screen.blit(minigameBg,(0,0))
		font = pygame.font.Font(None, 200)
		font2 = pygame.font.Font(None,100)
		for i in range(length):
			prompt = random.choice(["F","I","S","H"])
			if i > 0:
				while prompt == letterData[i-1][-1]:
					prompt = random.choice(["F","I","S","H"])
			fish.append(prompt)
			letterData.append([font.render(prompt,1,BLACK), int((640//length) + i * ((SCREEN_RECT.w - 100) // length)), SCREEN_RECT.centery, prompt])

			alert = font2.render("PRESS THE KEYS! CATCH THE FISH!",1,(BLACK))
			screen.blit(alert,(200,200))

			screen.blit(letterData[i][0],(letterData[i][1],letterData[i][2]))
			
		for j in range(length):
			finput = 'void'
			while True:
				maxtime = length*1.8
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						doExit = True

				finput = self.inputs()

				timer += delta/10

				draw.rect(screen, (255,0,0), ((0 + SCREEN_RECT.w / 4), (SCREEN_RECT.centery - 100), (SCREEN_RECT.w / 2), 50))
				draw.rect(screen, (GREEN), ((0 + SCREEN_RECT.w / 4 +timer * ((SCREEN_RECT.w / 2)/maxtime)), (SCREEN_RECT.centery - 100), (SCREEN_RECT.w / 2 - timer * ((SCREEN_RECT.w / 2)/maxtime)), 50))

				pygame.display.flip()

				if timer >= maxtime:
					fail = True
					break

				if finput == letterData[j][-1]:
					letterData[j][0] = font.render(letterData[j][-1],1,GREEN)
					screen.blit(letterData[j][0],(letterData[j][1],letterData[j][2]))
					correct.play()
					break
				
			if fail:
				break

			player.append(finput)
		if fail:
			return False	
		if player == fish:
			mixer.stop()
			return True
		
		else:
			return False
				
		
	def inputs(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_f]:
			return "F"
		elif keys[pygame.K_i]:
			return "I"
		elif keys[pygame.K_s]:
			return "S"
		elif keys[pygame.K_h]:
			return "H"
		else:
			return "void"
	
	def fishSearch(self,screen, spotlight = 60):
		caughtFish = False
		caughtRare = False
		fishPos = Rect(random.randrange(300,980),random.randrange(50,580),160,72)
		rareFishPos = Rect(random.randrange(300,980),random.randrange(50,580),120,60)
		tempText = font.render("find a fish!",1,(255,255,255))
		temp1 = tempText.get_rect()
		temp1.center = SCREEN_RECT.center
		pygame.mouse.set_visible(False)
		while not caughtFish:
			for event in pygame.event.get():
					if event.type == pygame.QUIT:
						quit()

			screen.blit(searchBg,(300,50))
			screen.blit(shadow,fishPos)
			screen.blit(rareShadow,rareFishPos)
			draw.circle(screen,(0,0,0),pygame.mouse.get_pos(),1900,(1900-spotlight))
			screen.blit(searchBorder,(300,50))
			screen.blit(tempText,(temp1.x,temp1.y+300))

			if fishPos.collidepoint(pygame.mouse.get_pos()):
				caughtFish = True
				break
			if rareFishPos.collidepoint(pygame.mouse.get_pos()):
				caughtFish = True
				caughtRare = True
				break
			
			pygame.display.flip()
		if caughtFish:
			pygame.mouse.set_visible(True)
			if caughtRare:
				return [True, True]
			else:
				return [True, False]
		else:
			return [False, False]
		

			


def tutorial(screen):
	running = 0
	description = [
	    #4 lines maximum
	    "WELCOME TO FISHFISHFISH",
	    "use ( W A S D ) to move, and use ( E ) to open your inventory",
	    "use mouse to interact with objects when your cursor displays ( ! )",
	    "click on the lake to begin your fishing journey",
	    "happy fishing!",
	]

	font = pygame.font.Font(None, 60)

	imgRect = Rect(1200,100,70,70)
	while running < 10**10:
		running+=1
		for event in pygame.event.get():
			pass
		line = 250-100
		for i in range(len(description)):
			text = font.render(description[i],0,(0,0,0))
			line+=100
			textRect = text.get_rect()
			textRect.centerx = SCREEN_RECT.centerx
			screen.blit(text, (textRect.x,line))
		if running > 3000:
			screen.blit(close, (1200,100))
		if imgRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
			running = 10**10
		pygame.display.flip()

def invTutorial(screen):
	running = True
	description = [
	    #4 lines maximum
	    "this is your inventory",
	    'you can see all of your fish here',
	    "you can see each fishes price and size",
	    "click on a fish to see more info on them",
		"happy fishing!"
	]

	font = pygame.font.Font(None, 60)

	screen.blit(close, (1200,100))
	imgRect = Rect(1200,100,70,70)
	screen.blit(tutorialBg,(0,0))
	while running:
		
		for event in pygame.event.get():
			pass
		line = 250-100
		for i in range(len(description)):
			text = font.render(description[i],0,(255,255,255))
			line+=100
			textRect = text.get_rect()
			textRect.centerx = SCREEN_RECT.centerx
			screen.blit(text, (textRect.x,line))
		# draw.rect(screen,(255,255,255),imgRect)
		screen.blit(close, (1200,100))
		if imgRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
			running = False
		pygame.display.flip()
	return True

class SellStation:

	def __init__(self):
		self.rect = Rect(1150,50,340,340)
		self.upgRect = Rect(300,350,300,170)
		self.sellRect = Rect(1000,350,300,170)
		self.sharedRect = Rect(650,370,300,170)
		self.image = pygame.image.load('resources/market.png')
		self.upgImg = pygame.image.load('resources/upg.png')
		self.sellImg = pygame.image.load("resources/sell.png")

		self.nextImg = pygame.image.load("resources/next.png")
		self.nextRect = Rect(1450,50,100,100)
		self.buyImg = pygame.image.load("resources/buy.png")
		self.buyRect = Rect(285,690,240,135)

		self.posterRect = Rect(165,40,480,600)

		self.chanceImg = pygame.image.load("resources/luck.png")
		self.chanceDesc = [
			#4 lines maximum
			"upgrade your luck",
			"catch rarer fish",
			# "placeholder line, dont blit, place cost here",
			# "placeholder line, dont blit, place upgrade purchase count here",
		]
		self.chanceBought = 0
		self.chancePrice = [240, "SOLD OUT", 19440, 6480, 2160, 720]
		# self.chancePrice = [240, "SOLD OUT",1920, 960, 480]

		self.bagImg = pygame.image.load("resources/bag.png")
		self.bagDesc = [
			"upgrade your bag",
			"carry more fish",
		]
		self.bagBought = 0
		self.bagPrice = [150,"SOLD OUT", 12150, 4050,1350,450]
		# self.bagPrice = [180, "SOLD OUT",1440,720,360]

		self.baitImg = pygame.image.load("resources/bait.png")
		self.baitPrice = 15
		self.baitDesc = [
			"buy some bait",
			"catch fish (maybe)",
			f"cost: {self.baitPrice}",
		]
		self.bonusBaitImg = pygame.image.load("resources/bonusBait.png")
		self.bonusBaitPrice = [120,"SOLD OUT", 9720, 3240,1080,360]
		self.bonusBaitDesc = [
			"get more bait for the same price",
			"too many worms :(",
			# f"cost: {self.bonusBaitPrice}",
		]
		self.bonusBaitBought = 0

		self.selecting = False
		self.isSelling = False
		self.isUpgrading = False

	def saveData(self):
		return [self.chanceBought, self.bagBought, self.bonusBaitBought]
	
	def loadData(self,save):
		self.chanceBought = save[0]
		self.bagBought = save[1]
		self.bonusBaitBought = save[2]
		
	
	def draw(self,screen):
		screen.blit(self.image,self.rect)
	
	def select(self,bewl):
		self.selecting = bewl
		return True

	def drawButtons(self,screen):
		if self.selecting:
			screen.blit(self.upgImg, self.upgRect)
			screen.blit(self.sellImg, self.sellRect)
		elif self.isUpgrading:
			screen.blit(self.upgImg,self.sharedRect)
		elif self.isSelling:
			screen.blit(self.sellImg,self.sharedRect)

	def upgrading(self,bewl: bool):
		self.isUpgrading = bewl
		return True

	def selling(self, bewl: bool):
		self.isSelling = bewl
		return True
	

	def upgButton(self):
		self.selecting = False
		return True
	
	def sellButton(self):
		self.selecting = False
		return True
	
	def chancePage(self,screen: pygame.Surface):
		self.close = Rect(15, 15, 75,75)
		screen.blit(self.chanceImg, self.posterRect)
		screen.blit(self.nextImg,self.nextRect)
		screen.blit(self.buyImg,self.buyRect)

		font = pygame.font.Font(None, 60)
		line = 250-100

		text = font.render(self.chanceDesc[0],1,(255,250,190))
			

		for i in range(len(self.chanceDesc)):
			text = font.render(self.chanceDesc[i],1,(255,250,190))
			line+=64
			textRect = text.get_rect()
			textRect.centerx = 1000
			screen.blit(text, (textRect.x,line))
		
		text = font.render(f"Cost: {self.chancePrice[self.chanceBought]}",1,(255,250,190))
		line+=64
		textRect = text.get_rect()
		textRect.centerx = 1000
		screen.blit(text, (textRect.x,line))

		text = font.render(f"# purchased: {abs(self.chanceBought)}",1,(255,250,190))
		line+=64
		textRect = text.get_rect()
		textRect.centerx = 1000
		screen.blit(text, (textRect.x,line))
			
		screen.blit(close, (15, 15))
	
	def bagPage(self,screen: pygame.Surface):
		self.close = Rect(15, 15, 75,75)
		screen.blit(self.bagImg, self.posterRect)
		screen.blit(self.nextImg,self.nextRect)
		screen.blit(self.buyImg,self.buyRect)

		font = pygame.font.Font(None, 60)
		line = 250-100

		text = font.render(self.bagDesc[0],1,(255,250,190))
			

		for i in range(len(self.bagDesc)):
			text = font.render(self.bagDesc[i],1,(255,250,190))
			line+=64
			textRect = text.get_rect()
			textRect.centerx = 1000
			screen.blit(text, (textRect.x,line))
		
		text = font.render(f"Cost: {self.bagPrice[self.bagBought]}",1,(255,250,190))
		line+=64
		textRect = text.get_rect()
		textRect.centerx = 1000
		screen.blit(text, (textRect.x,line))

		text = font.render(f"# purchased: {abs(self.bagBought)}",1,(255,250,190))
		line+=64
		textRect = text.get_rect()
		textRect.centerx = 1000
		screen.blit(text, (textRect.x,line))
			
		screen.blit(close, (15, 15))


	def baitPage(self,screen: pygame.Surface):
		self.close = Rect(15, 15, 75,75)
		screen.blit(self.baitImg, self.posterRect)
		screen.blit(self.nextImg,self.nextRect)
		screen.blit(self.buyImg,self.buyRect)

		font = pygame.font.Font(None, 60)
		line = 250-100

		text = font.render(self.baitDesc[0],1,(255,250,190))
			

		for i in range(len(self.baitDesc)):
			text = font.render(self.baitDesc[i],1,(255,250,190))
			line+=64
			textRect = text.get_rect()
			textRect.centerx = 1000
			screen.blit(text, (textRect.x,line))
			
		screen.blit(close, (15, 15))

	def bonusBaitPage(self,screen: pygame.Surface):
		self.close = Rect(15, 15, 75,75)
		screen.blit(self.bonusBaitImg, self.posterRect)
		screen.blit(self.nextImg,self.nextRect)
		screen.blit(self.buyImg,self.buyRect)

		font = pygame.font.Font(None, 60)
		line = 250-100

		text = font.render(self.bonusBaitDesc[0],1,(255,250,190))
			

		for i in range(len(self.bonusBaitDesc)):
			text = font.render(self.bonusBaitDesc[i],1,(255,250,190))
			line+=64
			textRect = text.get_rect()
			textRect.centerx = 1000
			screen.blit(text, (textRect.x,line))
			
		text = font.render(f"Cost: {self.bonusBaitPrice[self.bonusBaitBought]}",1,(255,250,190))
		line+=64
		textRect = text.get_rect()
		textRect.centerx = 1000
		screen.blit(text, (textRect.x,line))

		text = font.render(f"# purchased: {abs(self.bonusBaitBought)}",1,(255,250,190))
		line+=64
		textRect = text.get_rect()
		textRect.centerx = 1000
		screen.blit(text, (textRect.x,line))
			
		screen.blit(close, (15, 15))

		



	
class Home:
	def __init__(self):
		self.image = pygame.image.load("resources/home.png").convert_alpha()
		self.rect = Rect(-120,-120,self.image.get_rect().w,self.image.get_rect().h)

	def draw(self, screen: pygame.Surface):
		screen.blit(self.image,self.rect)
	

	

		


	
