from typing import Text
import pygame
pygame.font.init()
from TextButton import TextButton
class MapSelectButton(TextButton):
    def __init__(self,game,pos,map,reactToUp = True,bgColor = (100,100,100),borderColor = (0,0,0),font = pygame.font.SysFont('Arial',25,1)):
        func = lambda: game.setMap(map)
        super().__init__( pos,map.name,func,reactToUp,bgColor,borderColor)
        