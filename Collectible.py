from Vector import Vector
from View import View
import pygame
Rect = pygame.Rect
class Collectible:
    def __init__(self,game,pos,effect,color = (0,100,0), lifetime = 15):
        self.game = game
        self.pos = pos
        self.exists = True
        self.effect = effect
        self.color = color
        self.age = 0
        self.lifetime = lifetime*game.fps
        
    def render(self,surface):
        renderpos = self.pos.copy()
        renderpos.x -= self.game.camera.pos.x
        renderpos.y -= self.game.camera.pos.y
        pygame.draw.rect(surface,self.color,renderpos)
    def copy(self):
        return Collectible(self.game,self.pos,self.effect,self.color, self.lifetime/self.game.fps)
    
    def tick(self):
        if self.game.view == View.game:
            self.age += 1
            for player in self.game.players:
                if player.pos.colliderect(self.pos):
                    self.exists = False
                    self.effect(player)
            if self.age >= self.lifetime:
                self.exists = False