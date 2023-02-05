from Vector import Vector
from Circle import Circle
from Explosion import Explosion
from Bullet import Bullet
import pygame
class Grenade(Bullet):
    def __init__(self,game,shooter,dmg, pos,score = 4,lifetime = 10):
        super().__init__(game,shooter,dmg, pos,score,lifetime)
        self.vel = 25
        self.currYVel = -5
    def move(self):
        self.pos.move_ip(self.vel*self.facing,self.currYVel)
    def render(self, surface):
        renderpos = self.pos.copy()
        renderpos.x -= self.game.camera.pos.x
        renderpos.y -= self.game.camera.pos.y
        pygame.draw.rect(surface,(0,0,0),renderpos)
    def explode(self):
        self.game.bullets.append(
                    Explosion(Circle(
                        self.pos.x,self.pos.y,70
                        ),self.game,self.shooter,self.dmg*2
                    )
                )
    def hitEffect(self,player):
        player.changeHp(-self.dmg)
        self.shooter.score += self.score
    def tick(self):
        self.lifetime -= 1
        self.currYVel += 1

        self.move()
        for block in self.game.map.blocks:
            if self.pos.colliderect(block.extend(1)):
                self.explode()
                self.exists = False
        for player in self.game.players:
            if self.pos.colliderect(player.pos) and player is not self.shooter:
                self.explode()
                self.damagedPlayer = player
                self.exists = False
        if self.lifetime == 0:
            self.exists = False