import pygame
from Bullet import Bullet
class Ray(Bullet):
    def __init__(self,game,shooter,dmg,pos,score = 3,lifetime = 0.2):
        super().__init__(game,shooter,dmg, pos,score,lifetime)
    def render(self, surface):
        renderpos = self.pos.copy()
        renderpos.x -= self.game.camera.pos.x
        renderpos.y -= self.game.camera.pos.y
        pygame.draw.rect(surface,(255,0,0),renderpos)
    def hitEffect(self,player):
        player.changeHp(-self.dmg)
        self.shooter.score += self.score
    def tick(self):
        self.lifetime -= 1
        self.pos.y += 1
        self.pos.h -= 2
        if self.deactivate:
            self.active = False
        for player in self.game.players:
            if self.pos.colliderect(player.pos) and player is not self.shooter:
                self.damagedPlayer = player
        self.deactivate = True
        if self.lifetime == 0:
            self.exists = False