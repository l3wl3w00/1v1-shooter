import pygame
Rect = pygame.Rect
class Bullet:
    def __init__(self,game,shooter,dmg, pos,score,lifetime = 10):
        self.game = game
        self.shooter = shooter
        self.damagedPlayer = None
        self.active = True
        self.deactivate = False
        self.exists = True
        self.lifetime = lifetime*self.game.fps
        self.facing = self.shooter.facing
        self.vel = 30
        self.score = score
        
        self.pos = pos
        self.dmg = dmg
    def hitEffect(self,player):
        pass
    def tick(self):
        self.lifetime -= 1
        self.move()
        for block in self.game.map.blocks:
            if self.pos.colliderect(block.extend()):
                self.exists = False
        for player in self.game.players:
            if self.pos.colliderect(player.pos) and player is not self.shooter:
                self.damagedPlayer = player
                self.exists = False
        if self.lifetime == 0:
            self.exists = False