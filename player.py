import pygame
from pygame.math import Vector2
import math
import random
from math import atan2
from pygame import Rect


class Player:
	''':)'''
	def __init__(self,scale):
		self.delta:float
		self.screen: pygame.Surface
		###load image
		self.baseImage = pygame.image.load('resources/guyNice.png')
		self.baseImageRight = pygame.image.load('resources/guyNiceRight.png')
		self.baseBlaster = pygame.image.load('resources/bigfist.png')
		###give images correct sizes (96 pixels and 75 pixels respectively)
		#/1200
		self.defaultSizeImage = pygame.transform.smoothscale_by(self.baseImage,96/1100)#self.baseImage.get_rect().height)
		self.defaultSizeImageRight = pygame.transform.smoothscale_by(self.baseImageRight,96/1100)#self.baseImage.get_rect().height)
		self.defaultSizeBlaster = pygame.transform.smoothscale_by(self.baseBlaster, 95/self.baseBlaster.get_rect().width)

		
		###scales images to resolution
		# self.image = pygame.transform.smoothscale_by(self.defaultSizeImage,scale)
		# self.BlasterImage = pygame.transform.smoothscale_by(self.defaultSizeBlaster,scale)
		self.BlasterImage = self.defaultSizeBlaster
		self.image = self.defaultSizeImage

		
		#self.transformed_image = pygame.transform.rotate(self.image, 0)
		self.transformed_Blaster = pygame.transform.rotate(self.BlasterImage, 0)
		
		self.vel = Vector2(0,0)
		self.centerpos = Vector2(400,400)

		self.newMousePos = Vector2(0,0)

		self.handAngle: float
		
		self.inventory = []

		self.chance = 0
		self.money = 0
		# self.controller: object

	def mouseMove(self):
		self.newMousePos = Vector2(pygame.mouse.get_pos())

	
	def rotate(self):
		self.handAngle = math.degrees(math.atan2( self.newMousePos.x-self.centerpos.x, self.newMousePos.y-self.centerpos.y))+180
		
		self.transformed_Blaster = pygame.transform.rotate(self.BlasterImage, self.handAngle)
	
	def draw(self):
		rect_to_draw = Rect(self.image.get_rect())
		rect_to_draw.center = (int(self.centerpos.x), int(self.centerpos.y))

		rect_to_fish = Rect(self.transformed_Blaster.get_rect())
		rect_to_fish.center = (int(self.centerpos.x), int(self.centerpos.y))

		self.screen.blit(
			self.transformed_Blaster,
			rect_to_fish
		)
		self.screen.blit(
			self.image,
			rect_to_draw 
		)

	def playerInput(self):
		'''Gets Input from keyboard
		| Movement is pixels per second'''
		keys = pygame.key.get_pressed()
		###LEFT AND RIGHT
		if keys[pygame.K_a]:
			self.vel.x = -220
			self.image = self.defaultSizeImage
		if keys[pygame.K_d]:
			self.vel.x = 220
			self.image = self.defaultSizeImageRight
		if not keys[pygame.K_a] and not keys[pygame.K_d]:
			self.vel.x = 0
		###UP AND DOWN
		if keys[pygame.K_w]:
			self.vel.y = -220
		if keys[pygame.K_s]:
			self.vel.y = 220
		if not keys[pygame.K_w] and not keys[pygame.K_s]:
			self.vel.y = 0
		if keys[pygame.K_SPACE]:
			pass

		# if pygame.joystick.get_count() > 0:
		# 	if self.controller != pygame.joystick.Joystick(0):
		# 		self.controller = pygame.joystick.Joystick(0)
			
		
	def move(self):
		'''Applies velocity to position'''
		# if self.vel.length() != 0:
		# 	self.vel.normalize()
		self.centerpos+=self.vel*self.delta

	
	
	def update(self,delta,screen):
		'''Runs specific player functions every frame'''
		self.delta = delta
		self.screen = screen

		self.playerInput()
		self.move()
		self.mouseMove()
		self.rotate()
		self.draw()

	def upgrade(self):
		self.chance += 1
		return True
