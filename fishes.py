import pygame
from pygame import image
from pygame import transform
from globals import SCREEN_RECT

placeholder = image.load('resources/placeholder.png')


class Fishes:
    def __init__(self):
        self.delta:float
        self.screen: pygame.Surface

        self.size = 1.00 #percent


        self.baseImg = placeholder
        self.caughtImg = transform.scale_by(self.baseImg,self.size)
        self.inventoryImg = transform.scale_by(self.baseImg,0.2)


        self.description = [
            #4 lines maximum
            "this is a placeholder fish",
            "if youve caught this something",
            "has gone wrong"
        ]
    def caughtDisplay(self,screen:pygame.Surface):
        font = pygame.font.Font(None, 40)
        line = 450-100 #out of 800
        imgRect = self.caughtImg.get_rect()
        imgRect.centerx = SCREEN_RECT.centerx
        screen.blit(self.caughtImg,(imgRect.x,imgRect.y))

        text = font.render(self.description[0],1,(255,255,230))
        textrect = text.get_rect()
        textrect.centerx = SCREEN_RECT.x // 2
        for i in range(len(self.description)):
            text = font.render(self.description[i],1,(255,255,230))
            line+=100
            screen.blit(text, (text.get_rect().centerx,line))
            
