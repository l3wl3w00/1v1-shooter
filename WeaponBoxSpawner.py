from WeaponBox import WeaponBox
import random

import pygame
from CollectibleSpawner import CollectibleSpawner
class WeaponBoxSpawner(CollectibleSpawner):
    def __init__(self,game,pos, drag = True,frequency = 30):
        super().__init__(game,pos,None, drag,frequency)
        self.color = (162,42,42)
    def render(self,surface):
        renderpos = self.pos.copy()
        renderpos.x -= self.game.camera.pos.x
        renderpos.y -= self.game.camera.pos.y
        pygame.draw.rect(surface,self.color,renderpos)
    def spawn(self):
        self.game.collectibles.append(
            WeaponBox(self.game,self.pos,random.choice(self.game.weaponTypes)(self.game,None))
        )
        