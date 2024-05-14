import pygame
from pygame.math import Vector2
import math
from pygame import Rect
from particles import ParticleEmitter


class Player:
	''':)'''
	def __init__(self,scale):
		self.delta:float
		###load image
		self.baseImage = pygame.image.load('resources/guy.png').convert_alpha()
		self.baseImageRight = pygame.image.load('resources/guyR.png').convert_alpha()
		self.baseBlaster = pygame.image.load('resources/bigfist2.png').convert_alpha()
		self.defaultSizeBlaster = pygame.transform.smoothscale_by(self.baseBlaster, 95/self.baseBlaster.get_rect().width)
		###scales images to resolution
		self.BlasterImage = self.defaultSizeBlaster
		self.image = self.baseImage
		self.transformed_Blaster = pygame.transform.rotate(self.BlasterImage, 0)
		#player states
		self.vel = Vector2(0,0)
		self.direction = 1
		self.centerpos = Vector2(500,400)
		self.rect = Rect(int(self.centerpos.x-50), int(self.centerpos.y-80), 100, 70)
		self.feetpos = Vector2(0,0) #122.181818182  height of guy
		#fishing rod
		self.newMousePos = Vector2(0,0)
		self.handAngle: float
		#stats
		self.inventory = []
		self.money = 20
		self.bait = 4
		#upgrade variables
		self.chance = 0 # add 3
		self.bagsize = 3 # add 3
		self.maxspeed = 240 #add 60
		self.baitBonus = 1

		#Particle System by Twice_
		self.dirt = ParticleEmitter(
			particleLifetime = 0.45,
			initAttributes = [
				["randYVelo", [-1800,0]],
				["randColorChoice", [(92, 39, 17), (207, 187, 155),(116, 49, 19)]],
				["randSize", [8,16]]
			],
			updateAttributes = [
				["sizeOverLife", [10, 8, 1]],
				["deleteOnSize", [0, 1]],
			],
			ppf = 1,
			maxParticles = 50,
			spawnType = "onMove",
			ppfMaxVelo = 0.001,

		)
		
		self.font = pygame.font.Font(None, 52)
		self.font2 = pygame.font.Font(None, 80)

	def saveData(self):
		playerSave = {1:self.money,2:self.bait,3:self.chance,4:self.bagsize}
		return playerSave	
	def loadData(self, save: dict):
		self.money = save[1]
		self.bait = save[2]
		self.chance = save[3]
		self.bagsize = save[4]
		

	def mouseMove(self):
		self.newMousePos = Vector2(pygame.mouse.get_pos())	
	def rotate(self):
		self.handAngle = math.degrees(math.atan2( self.newMousePos.x-self.centerpos.x, self.newMousePos.y-self.centerpos.y))+180
		
		self.transformed_Blaster = pygame.transform.rotate(self.BlasterImage, self.handAngle)	
	def draw(self,screen):
		rect_to_draw = Rect(self.image.get_rect())
		rect_to_draw.center = (int(self.centerpos.x), int(self.centerpos.y))

		rect_to_fish = Rect(self.transformed_Blaster.get_rect())
		rect_to_fish.center = (int(self.centerpos.x), int(self.centerpos.y))

		screen.blit(
			self.transformed_Blaster,
			rect_to_fish
		)
		screen.blit(
			self.image,
			rect_to_draw 
		)
	def playerInput(self):
		'''Gets Input from keyboard
		| Movement is pixels per second'''
		keys = pygame.key.get_pressed()
		###LEFT AND RIGHT
		if keys[pygame.K_a]:
			if self.vel.x > -self.maxspeed:
				self.vel.x -= 15
			self.image = self.baseImage
			self.direction = -1

		if keys[pygame.K_d]:
			if self.vel.x < self.maxspeed:
				self.vel.x += 15

			self.image = self.baseImageRight
			self.direction = 1

		if not keys[pygame.K_a] and not keys[pygame.K_d]:
			self.vel.x *= 0.9
		###UP AND DOWN
		if keys[pygame.K_w]:
			if self.vel.y > -self.maxspeed:
				self.vel.y -= 15

		if keys[pygame.K_s]:
			if self.vel.y < self.maxspeed:
				self.vel.y += 15

		if not keys[pygame.K_w] and not keys[pygame.K_s]:
			self.vel.y *= 0.9		
	def move(self):
		'''Applies velocity to position'''
		self.centerpos+=self.vel*self.delta
		if self.direction == 1:
			self.feetpos.update(self.centerpos.x-35, self.centerpos.y+35)
		else:
			self.feetpos.update(self.centerpos.x+35, self.centerpos.y+35)
	def reverseVel(self):
		self.vel = -self.vel*1.2
		self.direction = -self.direction
	

	def update(self,delta,screen):
		'''Runs specific player functions every frame'''
		self.delta = delta

		self.playerInput()
		self.move()
		self.mouseMove()
		self.rotate()

		self.rect = Rect(int(self.centerpos.x-50), int(self.centerpos.y-50), 100, 100)
		self.dirt.update(screen, delta, self.feetpos,self.vel)

		self.draw(screen)


	def statDisplay(self, screen, gamestate = "main"):
		if gamestate == "main":
			wallet	= self.font.render(f"Fishens: {str(round(self.money))}", 1, (20, 30, 0))
			fish	= self.font.render(f"Fish:    {str(len(self.inventory))}/{str(self.bagsize)}", 1, (20, 30, 0))
			bait	= self.font.render(f"Bait:    {str(self.bait)}", 1, (20, 30, 0))
			screen.blit(wallet,	(15,775))
			screen.blit(fish,	(15,815))
			screen.blit(bait,	(15,855))
		if gamestate == "statscreen":
			wallet	= self.font2.render(f"Fishens: {str(round(self.money))}", 1, (20, 30, 0))
			fish	= self.font2.render(f"Fish:    {str(len(self.inventory))}/{str(self.bagsize)}", 1, (20, 30, 0))
			bait	= self.font2.render(f"Bait:    {str(self.bait)}", 1, (20, 30, 0))
			chance	= self.font2.render(f"Luck: {str(self.chance)}", 1, (20,30,20))
			screen.blit(wallet,	(580,270))
			screen.blit(fish,	(580,360))
			screen.blit(bait,	(580,450))
			screen.blit(chance,	(580,540))



	def upgradeChance(self, cost):
		if self.money >= cost:
			self.money -= cost
			self.chance+=4
			return True
		else:
			return False
	
	def upgradeBag(self, cost):
		if self.money >= cost:
			self.money -= cost
			self.bagsize+=3
			return True
		else:
			return False
	
	def upgradeSpeed(self, cost):
		if self.money >= cost:
			self.money -= cost
			self.maxspeed+=60
			return True
		else:
			return False
	
	def baitUp(self,cost):
		if self.money >= cost:
			self.money -= cost
			self.bait+=self.baitBonus
			return True
		else:
			return False

	def bonusUp(self,cost):
		if self.money >= cost:
			self.money -= cost
			self.baitBonus+=1
			return True
		else:
			return False