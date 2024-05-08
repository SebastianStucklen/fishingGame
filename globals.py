from pygame.math import Vector2
from pygame import Rect
import pygame
import math
from typing import Callable, Any

SCREEN_SIZE = (1600, 900)
SCREEN_RECT = Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1])
FPS = 60

WHITE = (255,255,255)
GREEN = (20,235,0)


class CursorTools:
	'''Various tools for making clicking on things a little easier'''
	def __init__(self, image:pygame.Surface):
		self.clickable = image
		self.canClick = False


	def clickInteract(self,
				   objPos:Rect, 
				   pressDown: bool = True, 
				   function:Callable[[], Any] = lambda: True):
		'''for use with buttons, etc. / use pressDown(bool) argument if you only want something to run on pygame.mouse.MOUSEBUTTONDOWN / can be given 1 function to run upon click (return value recommended)'''
		if objPos.collidepoint(pygame.mouse.get_pos()):
		#object-mouse collision check
			self.canClick = True
			#for use with custom cursor alert image
			if pygame.mouse.get_pressed()[0] and pressDown:
				return function()#runs and returns function on click

	def playerInteract(self, 
					objPos:Rect, 
					playerPos: Vector2, 
					function:Callable[[], Any], 
					range: int = 400, 
					pressDown: bool = True):
		'''for player specific interaction, with range. can be passed a function to run on click, as well as a bool variable meant to be used with pygame.mouse.MOUSEBUTTONDOWN'''
		if abs(math.dist(pygame.mouse.get_pos(),playerPos)) <= range:
		#player-mouse range check
			if objPos.collidepoint(pygame.mouse.get_pos()):
			#object-mouse collision check
				self.canClick = True
				#for use with custom mouse alert image
				if pygame.mouse.get_pressed()[0] and pressDown:
					return function() #run and return function on click
				
	def customCursor(self, screen: pygame.Surface):
		'''run every loop to draw an alert on mouse whenever something is clickable'''
		if self.canClick:
			temp = pygame.mouse.get_pos()
			screen.blit(self.clickable, (temp[0]-30,temp[1]-30))
