import pygame
from pygame import image
from pygame import transform
from globals import SCREEN_RECT
from pygame import draw

placeholder = image.load('resources/placeholder.png')
common1 = image.load('resources/common1.png')
common2 = image.load('resources/common2.png')
common3 = image.load('resources/common3.png')
common4 = image.load('resources/common4.png')
common5 = image.load('resources/common5.png')


class Fishes:
    baseImg = placeholder

    def __init__(self, size: float = 1.00):
        self.delta:float
        self.screen: pygame.Surface

        self.size = size #percent
        self.price = 0*size

        self.caughtImg = self.baseImg #transform.scale_by(self.baseImg,self.size)
        self.inventoryImg = transform.scale_by(self.baseImg,0.2)

        self.bigView = True

        self.description = [
            #4 lines maximum
            "this is a placeholder fish",
            "if youve caught this something",
            "has gone wrong",
            "testtest"
        ]
    def caughtDisplay(self,screen:pygame.Surface):
        if self.bigView:
            font = pygame.font.Font(None, 60)
            line = 450-100 #out of 800
            imgRect = self.caughtImg.get_rect()
            imgRect.centerx = SCREEN_RECT.centerx
            screen.blit(self.caughtImg,(imgRect.x,50))

            text = font.render(self.description[0],1,(255,255,230))
            textrect = text.get_rect()
            textrect.centerx = SCREEN_RECT.centerx

            for i in range(len(self.description)):
                text = font.render(self.description[i],1,(255,255,230))
                line+=100
                screen.blit(text, (textrect.x,line))
            
            draw.rect(screen, (255,0,0), (imgRect.right+20, imgRect.top, 50,50))
            return 
    


    def toggleInventoryView(self):
        self.bigView = not self.bigView

class Common1(Fishes):
    baseImg = common1

    def __init__(self, size: float):
        super().__init__(size)

        self.price = 0*size

        self.description = [
            #4 lines maximum
            f"Size: {round(size)}     Price: {self.price}",
            "this is a NORMAL fish",
            "it's a nice shade of lavender",
        ]

class Common2(Fishes):
    baseImg = common2

    def __init__(self, size: float):
        super().__init__(size)

        self.price = 0*size

        self.description = [
            #4 lines maximum
            f"Size: {round(size)}     Price: {self.price}",
            "this is a NORMAL fish",
            "it's an odd shade of green",
        ]

class Common3(Fishes):
    baseImg = common3

    def __init__(self, size: float):
        super().__init__(size)

        self.price = 0*size

        self.description = [
            #4 lines maximum
            f"Size: {round(size)}     Price: {self.price}",
            "this is a NORMAL fish",
            "it's a bright silver color",
        ]

class Common4(Fishes):
    baseImg = common4

    def __init__(self, size: float):
        super().__init__(size)

        self.price = 0*size

        self.description = [
            #4 lines maximum
            f"Size: {round(size)}     Price: {self.price}",
            "this is a NORMAL fish",
            "it's a bright yellow color",
        ]

class Common5(Fishes):
    baseImg = common5

    def __init__(self, size: float):
        super().__init__(size)

        self.price = 0*size

        self.description = [
            #4 lines maximum
            f"Size: {round(size)}     Price: {self.price}",
            "this is a NORMAL fish",
            "it's a pleasant orange color",
        ]