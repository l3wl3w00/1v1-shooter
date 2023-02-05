import pygame
from Weapon import Weapon
from Ray import Ray
class Lazer(Weapon):
    def __init__(self,game,owner):
        super().__init__(game,40,owner,game.lazerImg,0.5)
        self.lenght = 5000
    def render(self, surface, flipped = False):
        renderpos = self.owner.pos.copy()
        renderpos.x -= self.game.camera.pos.x
        renderpos.y -= self.game.camera.pos.y
        if flipped:
            surface.blit(pygame.transform.flip(self.img,True,False),(renderpos.x-20,renderpos.y-10))
        else:
            surface.blit(self.img,(renderpos.x-40,renderpos.y-10))
    def shoot(self,pos):
        
        pos.w = self.lenght
        if self.owner.facing == -1:
            pos.x-= self.lenght

        pos.h = 20
        self.game.bullets.append(Ray(self.game,self.owner,self.dmg,pos))
