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

from pygame import mixer




class TextDisplay:
	def __init__(self, text, x: float, y: float,size):
		if text == None: text = ""
		self.text = text
		self.x: float = x
		self.y: float = y

	def update(self, screen, text, size, color: tuple = (255,255,255)):
		font = pygame.font.Font(None, size)
		text = font.render(str(text), 1, color)
		screen.blit(text, (self.x, self.y))

class CursorTools:
	def __init__(self, image:pygame.Surface, image2:pygame.Surface):
		self.default = image
		self.clickable = image2
		self.canClick = False


	def clickInteract(self,objPos:Rect):
		if objPos.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
			return True

	def playerInteract(self, objPos:Rect, playerPos: Vector2, function:Callable[[], Any], range: int = 400, pressDown: bool = True):
		if abs(math.dist(pygame.mouse.get_pos(),playerPos)) <= range:
			if objPos.collidepoint(pygame.mouse.get_pos()):
				self.canClick = True
				if pygame.mouse.get_pressed()[0] and pressDown:
					return function()
	def customCursor(self,screen):
		if self.canClick:
			screen.blit(self.clickable, pygame.mouse.get_pos())
