import pygame
from pygame.math import Vector2
from pygame import Rect
pygame.init
from main import ct

class Button:
	def __init__(self, xpos, ypos, width, height, img, clickFunc):
		self.clickFunc = clickFunc
		self.img = img
		#the following code was going to be for being able to display just a colored square or an image, but I couldn't figure it out today.
		if type(img) == tuple:
			self.rect = Rect(xpos, ypos, width, height)
		elif type(img) == str:
			# self.rect = Rect(xpos, ypos, self.img.get_rect().width, self.img.get_rect().height)
			#I was having troubles defining the rect and getting it all running with an image.
			#I got it working with displaying the image originally, but then the rect hitbox was based on the height and width, not the size of the image.
			pass

	def update(self, screen, mouse):
		self.draw(screen)
		self.collisions(mouse)

	def draw(self, screen):
		if type(self.img) == tuple:
			pygame.draw.rect(screen, self.img, self.rect) #self.image here is a tuple, so therefor it's a color value instead of an image.
		elif type(self.img) == str:
			# screen.blit(self.img, (self.rect[0], self.rect[1]))
			#couldn't figure out how to get images working lol. I don't have enough experience with them rn.
			pass

	def collisions(self, mouse):
		if self.rect.collidepoint(mouse): #if your mouse is colliding with the button only.
			for event in pygame.event.get(): #loops through the frame's events.
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #if the left mouse button was pressed (event.button 1 is lmb).
					self.clickFunc() #calls the function for when the button is clicked.