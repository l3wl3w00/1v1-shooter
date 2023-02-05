import pygame
from Bullet import Bullet
class PistolBullet(Bullet):
    def __init__(self,game,shooter,dmg, pos,score = 1,lifetime = 10):
        super().__init__(game,shooter,dmg, pos,score,lifetime)
    def move(self):
        self.pos.move_ip(self.vel*self.facing,0)
    def render(self, surface):
        renderpos = self.pos.copy()
        renderpos.x -= self.game.camera.pos.x
        renderpos.y -= self.game.camera.pos.y
        pygame.draw.rect(surface,(0,0,0),renderpos)
    def hitEffect(self,player):
        player.changeHp(-self.dmg)
        self.shooter.score += self.score
