from Bullet import Bullet
import pygame
from Vector import Vector

class Explosion(Bullet):
    def __init__(self,pos,game,shooter,dmg,lifetime = 0.5):
        super().__init__(game,shooter,dmg, pos,lifetime)
        self.knockback = 15
        self.knockbackTime = 0.2
    def render(self, surface):
        renderpos = Vector(self.pos.x,self.pos.y)
        renderpos.x -= self.game.camera.pos.x
        renderpos.y -= self.game.camera.pos.y
        pygame.draw.circle(surface,(255,0,0),(renderpos.x,renderpos.y),self.pos.r)
    def hitEffect(self,player):
        player.hitByExplosion(self)
    def tick(self):
        self.lifetime -= 1
        self.pos.r -= 4
        if self.deactivate:
            self.active = False
        for player in self.game.players:
            if self.pos.collideRect(player.pos):
                #if player not in self.damaged:
                self.damagedPlayer = player
        self.deactivate = True
                    
        if self.lifetime == 0:
            self.exists = False