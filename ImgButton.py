from Button import Button
import pygame
from Button import Button

class ImgButton(Button):
    def __init__(self,pos,img,func,reactToUp = True,bgColor = (100,100,100),borderColor = (0,0,0)):
        super().__init__(pos,func,reactToUp,bgColor,borderColor)
        self.img = img

    def render(self,surface):
        rect = self.img.get_rect()
        rect.center = self.pos.center
        pygame.draw.rect(surface,self.borderColor,self.pos.inflate(2,2),4)
        surface.blit(self.img,rect)
    