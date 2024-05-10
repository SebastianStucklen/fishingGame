import pygame
from pygame import image
from pygame import transform
from globals import SCREEN_RECT
from pygame import draw
from pygame import Rect
from pygame import mixer


close = image.load('resources/close.png').convert_alpha()
placeholder = image.load('resources/placeholder.png').convert_alpha()
common1 = image.load('resources/common1.png').convert_alpha()
common2 = image.load('resources/common2.png').convert_alpha()
common3 = image.load('resources/common3.png').convert_alpha()
common4 = image.load('resources/common4.png').convert_alpha()
common5 = image.load('resources/common5.png').convert_alpha()

uncommon1 = image.load('resources/uncommon1.png').convert_alpha()
uncommon2 = image.load('resources/uncommon2.png').convert_alpha()
uncommon3 = image.load('resources/uncommon3.png').convert_alpha()

rare1 = image.load('resources/rare1.png').convert_alpha()
rare2 = image.load('resources/rare2.png').convert_alpha()

epic1 = image.load('resources/epic1.png').convert_alpha()
epic2 = image.load('resources/epic2.png').convert_alpha()

legendary1 = image.load('resources/legendary1.png').convert_alpha()
legendary2 = image.load('resources/legendary2.png').convert_alpha()



bg = image.load('resources/gradient2.png').convert_alpha()


#prices
#common: 30
#uncommon: 65
#rare: 120
#epic: 370
#legendary: 850

class Fishes:
	baseImg = placeholder

	def __init__(self, size: float = 1.00):

		self.size = size #percent
		self.price = 30*size

		self.caughtImg = self.baseImg #transform.scale_by(self.baseImg,self.size)
		self.inventoryImg = transform.smoothscale_by(self.baseImg,0.3)
		self.close = Rect(0,0,0,0)
		self.invImgRect = Rect(0,0,0,0)
		self.bigView = True
		self.smallView = True

		self.description = [
			#4 lines maximum
			"this is a placeholder fish",
			"if youve caught this something",
			"has gone wrong",
			"testtest"
		]
	def caughtDisplay(self,screen:pygame.Surface):
		if self.bigView == True:
			screen.fill((0,0,0))
			screen.blit(bg,(0,0))

			font = pygame.font.Font(None, 60)
			line = 450-100 #out of 800
			imgRect = self.caughtImg.get_rect()
			imgRect.centerx = SCREEN_RECT.centerx
			screen.blit(self.caughtImg,(imgRect.x,50))

			text = font.render(self.description[0],1,(0,0,0))
			

			for i in range(len(self.description)):
				text = font.render(self.description[i],1,(0,0,0))
				line+=90
				textRect = text.get_rect()
				textRect.centerx = SCREEN_RECT.centerx
				screen.blit(text, (textRect.x,line))
			line+=90
			text = font.render("press [esc] or the X to close",1,(0,0,0))
			textRect = text.get_rect()
			textRect.centerx = SCREEN_RECT.centerx
			screen.blit(text, (textRect.x, line))

			screen.blit(close, (imgRect.right+20, imgRect.top+50))
			self.close = Rect(imgRect.right+20, imgRect.top+50, 75,75)
	
	def invDisplay(self,screen:pygame.Surface,pos:list = [int,int]):
		if self.smallView == True:
			# screen.blit(bg,(0,0))
			font = pygame.font.Font(None, 20)
			imgRect = self.inventoryImg.get_rect()
			imgRect.topleft = (pos[0],pos[1])

			screen.blit(self.inventoryImg,imgRect)
			
			
			
			text = font.render(self.description[0],1,(0,0,0))
			textrect = text.get_rect()
			textrect.centerx = imgRect.centerx
			textrect.centery = pos[1] + (imgRect.height+10)
			screen.blit(text, textrect)

			self.invImgRect = imgRect

	def toggleBigView(self,bewl: bool):
		self.bigView = bewl
		return True
	
	def toggleSmallView(self,bewl: bool):
		self.smallView = bewl
		return True

class Common1(Fishes):
	baseImg = common1

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 30*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is a COMMON fish",
			"it's a nice shade of lavender",
		]

class Common2(Fishes):
	baseImg = common2

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 30*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is a COMMON fish",
			"it's an odd shade of green",
		]

class Common3(Fishes):
	baseImg = common3

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 30*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is a COMMON fish",
			"it's a bright silver color",
		]

class Common4(Fishes):
	baseImg = common4

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 30*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is a COMMON fish",
			"it's a bright yellow color",
		]

class Common5(Fishes):
	baseImg = common5

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 30*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is a COMMON fish",
			"it's a pleasant orange color",
		]

class Uncommon1(Fishes):
	baseImg = uncommon1

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 64*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is an UNCOMMON fish",
			"it smiles at you, giving you",
			"the feeling that all will be well",
		]

class Uncommon2(Fishes):
	baseImg = uncommon2

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 64*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is an UNCOMMON fish",
			"this isnt a fish!",
			"it looks at you grumpily",
		]
		
class Uncommon3(Fishes):
	baseImg = uncommon3

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 64*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is an UNCOMMON fish",
			"the fish cuddles up next to you",
			"you'd feel really guilty if you sold it",
		]

class Rare1(Fishes):
	baseImg = rare1

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 120*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is a RARE fish",
			"its VERY ugly. perhaps the ugliest.",
			"its trying to give you a kiss on the cheek",
		]

class Rare2(Fishes):
	baseImg = rare2

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 120*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"these are RARE fishes",
			"you caught a bag of 3 fish!",
			"hat trick! nice job.",
		]

class Epic1(Fishes):
	baseImg = epic1

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 370*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is an EPIC fish",
			"theres something deeply wrong with this fish",
			"it wants to look cute, but failing miserably",
		]

class Epic2(Fishes):
	baseImg = epic2

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 370*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is an EPIC fish",
			"it looks like a cave fish that got lost",
			"you can see right through it",
		]

class Legendary1(Fishes):
	baseImg = legendary1

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 850*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is a LEGENDARY fish?",
			"this isnt a fish!",
			"that's a LOT of money though",
		]

class Legendary2(Fishes):
	baseImg = legendary2

	def __init__(self, size: float):
		super().__init__(size)

		self.price = 850*size

		self.description = [
			#4 lines maximum
			f"{round(size*12,2)} inches  |  {round(self.price)} Fishens",
			"this is a LEGENDARY fish",
			"the poor salmon got stuck",
			"its a rare breed, worth tons",
		]