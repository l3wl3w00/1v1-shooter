from View import View
import pygame

class PlayerSpawner:
    def __init__(self,pos,id,game):
        self.pos = pos
        
        self.id = id
        self.game = game
        self.drag = False
    def render(self,surface):
        renderpos = self.pos.copy()
        renderpos.x -= self.game.camera.pos.x
        renderpos.y -= self.game.camera.pos.y
        if self.id == 0:
            pygame.draw.rect(surface,(0,0,255),renderpos)
        elif self.id == 1:
            pygame.draw.rect(surface,(255,0,0),renderpos)
        #self.player.render(surface)
    def mouseOver(self):
        mx = self.game.handler.relativeMx
        my = self.game.handler.relativeMy
        return self.pos.collidepoint((mx,my))
    def tick(self):
        if self.game.view == View.mapMaker:
            if self.game.handler.mouseDown:
                if self.mouseOver():
                    self.xDiff = self.game.handler.relativeMx - self.pos.x
                    self.yDiff = self.game.handler.relativeMy - self.pos.y
                    self.drag = True
            if self.game.handler.mouseUp:
                self.drag = False
            if self.drag:
                #self.pos.center = self.game.handler.relativeMx,self.game.handler.relativeMy#mx + self.game.camera.pos.x,my + self.game.camera.pos.y
                self.pos.x = self.game.handler.relativeMx - self.xDiff
                self.pos.y = self.game.handler.relativeMy - self.yDiff
