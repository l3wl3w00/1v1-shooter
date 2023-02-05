import pygame
class Weapon:
    def __init__(self,game,dmg,owner,img, atkSpeed = 1.0, auto = False):
        self.game = game
        self.dmg = dmg
        self.owner = owner
        self.img = img
        self.atkSpeed = atkSpeed
        self.auto = auto
        self.timeBtwAttacks = 1/atkSpeed*self.game.fps
    def render(self, surface, flipped = False):
        renderpos = self.owner.pos.copy()
        renderpos.x -= self.game.camera.pos.x
        renderpos.y -= self.game.camera.pos.y
        if flipped:
            surface.blit(pygame.transform.flip(self.img,True,False),(renderpos.x-30,renderpos.y-10))
        else:
            surface.blit(self.img,(renderpos.x-30,renderpos.y-10))