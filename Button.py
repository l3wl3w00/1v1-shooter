import pygame

class Button:
    def __init__(self,pos,func,reactToUp = True,bgColor = (100,100,100),borderColor = (0,0,0)):
        self.pos = pos        
        self.bgColor= bgColor
        self.borderColor = borderColor
        self.func = func
        self.reactToUp = reactToUp

    def mouseOver(self):
        return self.pos.collidepoint(pygame.mouse.get_pos())

    def tick(self):
        pass

    
    