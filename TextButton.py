import pygame
pygame.font.init()
from Button import Button
class TextButton(Button):
    def __init__(self,pos,text,func,reactToUp = True,bgColor = (100,100,100),borderColor = (0,0,0),font = pygame.font.SysFont('Arial',25,1)):
        super().__init__( pos,func,reactToUp,bgColor,borderColor)
        self.text = text
        self.font = font
        self.textColor = (0,0,0)
    def render(self,surface):
        self.textSurface = self.font.render( self.text, True, self.textColor)
        rect = self.textSurface.get_rect()
        rect.center = self.pos.center
        
        pygame.draw.rect(surface,self.bgColor,self.pos)
        pygame.draw.rect(surface,self.borderColor,self.pos,2)
        surface.blit(self.textSurface,rect)
