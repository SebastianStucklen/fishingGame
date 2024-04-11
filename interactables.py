import pygame
from pygame.math import Vector2
import math
import random

from pygame import Rect
from pygame import draw
from globals import SCREEN_RECT, WHITE, GREEN
from pygame import mixer
mixer.init()

correct = mixer.Sound("resources/correct.wav")
finish = mixer.Sound("resources/success2.mp3")
close = pygame.image.load('resources/close.png')
class FishingHole:
	
	def __init__(self):
		self.rect = Rect(50,400,700,400)
		self.text = []
	
	def draw(self,screen):
		draw.rect(screen, (0, 162, 232), self.rect)

	def collide(self,coord: Vector2):
		if self.rect.collidepoint(coord):
			return True


	def quicktime(self,screen,delta,length) -> bool:
		letterData = []
		player = []
		fish = []
		timer = 0
		screen.fill((0,0,0))
		font = pygame.font.Font(None, 200)
		mixer.stop()
		for i in range(length):
			prompt = random.choice(["Z","X","C","V"])
			if i > 0:
				while prompt == letterData[i-1][-1]:
					prompt = random.choice(["Z","X","C","V"])
			fish.append(prompt)
			letterData.append([font.render(prompt,1,WHITE), int((640//length) + i * ((SCREEN_RECT.width - 100) // length)), SCREEN_RECT.centery, prompt])
			# print(SCREEN_RECT.x + i * ((SCREEN_RECT.width - 100) / length))
			# print(letterData[i][1])
			screen.blit(letterData[i][0],(letterData[i][1],letterData[i][2]))
		for j in range(length):
			IPUT = 'void'
			while True:
				maxtime = length*2
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						doExit = True

				IPUT = self.inputs()

				timer += delta/10

				draw.rect(screen, (255,0,0), ((0 + SCREEN_RECT.width / 4), (SCREEN_RECT.centery - 100), (SCREEN_RECT.width / 2), 50))
				draw.rect(screen, (255,255,255), ((0 + SCREEN_RECT.width / 4 +timer * ((SCREEN_RECT.width / 2)/maxtime)), (SCREEN_RECT.centery - 100), (SCREEN_RECT.width / 2 - timer * ((SCREEN_RECT.width / 2)/maxtime)), 50))

				pygame.display.flip()

				if IPUT == letterData[j][-1]:
					letterData[j][0] = font.render(letterData[j][-1],1,GREEN)
					screen.blit(letterData[j][0],(letterData[j][1],letterData[j][2]))
					correct.play()
					break
				if timer >= maxtime:
					print("FAIL")
					break

			player.append(IPUT)
		print(player)
		print(fish)
		if player == fish:
			finish.play()
			return True
			
		else:
			# print(fish, player)
			return False
				
		
	def inputs(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_z]:
			return "Z"
		elif keys[pygame.K_x]:
			return "X"
		elif keys[pygame.K_c]:
			return "C"
		elif keys[pygame.K_v]:
			return "V"
		else:
			return "void"
	
def tutorial(screen):
	running = True
	description = [
	    #4 lines maximum
	    "WELCOME TO FISHFISHFISH",
	    'heres a quick tutorial',
	    "use ( W A S D ) to move, and use ( E ) to open your inventory",
	    "use mouse to interact with objects when your cursor displays ( ! )",
		"press on the lake to fish"
	]

	font = pygame.font.Font(None, 60)

	screen.blit(close, (1200,100))
	imgRect = Rect(1200,100,70,70)
	while running:
		for event in pygame.event.get():
			pass
		line = 250-100
		for i in range(len(description)):
			text = font.render(description[i],0,(255,255,255))
			line+=100
			screen.blit(text, (100,line))
		draw.rect(screen,(255,255,255),imgRect)
		screen.blit(close, (1200,100))
		if imgRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
			running = False
		pygame.display.flip()

