import pygame
from Bullet import Bullet
class Pellet(Bullet):
    def __init__(self,game,shooter,dmg, pos,vel,score = 1,lifetime = 0.2):
        super().__init__(game,shooter,dmg, pos,score,lifetime)
        self.vel = vel
        self.floatPos = [self.pos.x,self.pos.y]
    def move(self):
        # print("move x:",self.vel.x," y:",self.vel.y)
        self.floatPos[0] += self.vel.x
        self.floatPos[1] += self.vel.y
        self.pos.x = self.floatPos[0]
        self.pos.y = self.floatPos[1]
        # print("vel:",self.vel)
        # print("self.pos before:",self.pos)
        # self.pos.move_ip(self.vel.x,self.vel.y)
        # print("self.pos after:",self.pos)
    def render(self, surface):
        renderpos = self.floatPos.copy()
        renderpos[0] -= self.game.camera.pos.x
        renderpos[1] -= self.game.camera.pos.y
        pygame.draw.rect(surface,(0,0,0),(renderpos[0],renderpos[1],self.pos.w,self.pos.h))
    def hitEffect(self,player):
        player.changeHp(-self.dmg)
        self.shooter.score += self.score
