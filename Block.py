import pygame
from Vector import Vector
Rect = pygame.Rect
class Block:
    def __init__(self,pos,game,rightAccesable = False,leftAccesable = False, topAccesable = False, botAccesable = False ,drag = False, final = True):
        self.pos = pos
        self.game = game
        self.rightAccesable = rightAccesable
        self.leftAccesable = leftAccesable
        self.topAccesable = topAccesable
        self.botAccesable = botAccesable

        self.friction = Vector(0.1,0)
        # only in mapmaker view
        self.drag = drag
        self.final = final
        self.adjustLeft = False
        self.adjustRight = False
        self.adjustTop = False
        self.adjustBottom = False
        self.minimalW = 15
        self.minimalH = 15
        self.adjustColor = (100,100,100)
        self.activeColor = (50,50,50)
        self.fixRight = self.pos.right
        self.fixBottom = self.pos.bottom
        self.xDiff = self.pos.w//2
        self.yDiff = self.pos.h//2
        
    def mouseOver(self):
        mx = self.game.handler.relativeMx
        my = self.game.handler.relativeMy
        return self.pos.collidepoint((mx,my))

    def mouseOnRight(self,epsilon = 7):
        
        rect = Rect(self.pos.x+self.pos.w-epsilon,
                    self.pos.y, epsilon, self.pos.h)
        mx = self.game.handler.relativeMx
        my = self.game.handler.relativeMy
        return rect.collidepoint((mx,my))
    def mouseOnLeft(self,epsilon = 7):
        rect = Rect(self.pos.x,self.pos.y, epsilon, self.pos.h)
        mx = self.game.handler.relativeMx
        my = self.game.handler.relativeMy
        return rect.collidepoint((mx,my))
    def mouseOnBottom(self,epsilon = 7):
        rect = Rect(self.pos.x, self.pos.y + self.pos.h - epsilon, 
                    self.pos.w, epsilon)
        mx = self.game.handler.relativeMx
        my = self.game.handler.relativeMy
        return rect.collidepoint((mx,my))
    def mouseOnTop(self,epsilon = 7):
        rect = Rect(self.pos.x, self.pos.y, self.pos.w, epsilon)
        mx = self.game.handler.relativeMx
        my = self.game.handler.relativeMy
        return rect.collidepoint((mx,my))    
    def leftAdjust(self):
        if self.adjustLeft:
            prevX = self.pos.x
            if self.game.handler.relativeMx <= self.fixRight-self.minimalW:
                self.pos.x = self.game.handler.relativeMx
            diff = self.pos.x - prevX
            if self.pos.w - diff >= self.minimalW:
                self.pos.w -= diff
    def rightAdjust(self):
        if self.adjustRight:
            diff =  self.game.handler.relativeMx - self.pos.x
            if diff >= self.minimalW:
                self.pos.w = diff
            else:
                self.pos.w = self.minimalW

    def topAdjust(self):
        if self.adjustTop:
            prevY = self.pos.y
            if self.game.handler.relativeMy <= self.fixBottom-self.minimalH:
                self.pos.y = self.game.handler.relativeMy
            diff = self.pos.y - prevY
            if self.pos.h - diff >= self.minimalH:
                self.pos.h -= diff

    def bottomAdjust(self):
        if self.adjustBottom:
            diff =  self.game.handler.relativeMy - self.pos.y
            if diff > self.minimalH:
                self.pos.h = diff
            else:
                self.pos.h = self.minimalH
    def extend(self,w = 1):
        return Rect(self.pos.x-w, self.pos.y-w,self.pos.w+2*w,self.pos.h+2*w)
    def tick(self):
        if not self.final:
            if self.game.handler.mouseDown:
                if self.mouseOnLeft():
                    self.adjustLeft = True
                    self.fixRight = self.pos.right
                if self.mouseOnRight():
                    self.adjustRight = True
                if self.mouseOnTop():
                    self.adjustTop = True
                    self.fixBottom = self.pos.bottom
                if self.mouseOnBottom():
                    self.adjustBottom = True
                    
                if not self.adjustLeft and not self.adjustRight and not self.adjustTop and not self.adjustBottom:
                    if self.mouseOver():
                        self.xDiff = self.game.handler.relativeMx - self.pos.x
                        self.yDiff = self.game.handler.relativeMy - self.pos.y
                        self.drag = True
            if self.game.handler.mouseUp:
                self.adjustLeft = False
                self.adjustRight = False
                self.adjustTop = False
                self.adjustBottom = False
                self.drag = False
        self.leftAdjust()
        self.rightAdjust()
        self.topAdjust()
        self.bottomAdjust()
        if self.drag:
            #self.pos.center = self.game.handler.relativeMx,self.game.handler.relativeMy#mx + self.game.camera.pos.x,my + self.game.camera.pos.y
            self.pos.x = self.game.handler.relativeMx - self.xDiff
            self.pos.y = self.game.handler.relativeMy - self.yDiff

            
    def render(self,surface):
        renderpos = self.pos.copy()
        renderpos.move_ip(-self.game.camera.pos.x, -self.game.camera.pos.y)
        pygame.draw.rect(surface,(0,0,0),renderpos)
        if self.final:
            return
        epsilon = 7
        adjust = False
        if self.mouseOnLeft(epsilon):
            adjust = True
            rect = Rect(self.pos.x,self.pos.y, epsilon, self.pos.h)
            rect.move_ip(-self.game.camera.pos.x, -self.game.camera.pos.y)
            pygame.draw.rect(surface,self.adjustColor,rect)
        if self.mouseOnRight(epsilon):
            adjust = True
            rect = Rect(self.pos.x+self.pos.w-epsilon,
                    self.pos.y, epsilon, self.pos.h)
            rect.move_ip(-self.game.camera.pos.x, -self.game.camera.pos.y)  
            pygame.draw.rect(surface,self.adjustColor,rect)
        if self.mouseOnTop(epsilon):
            adjust = True
            rect = Rect(self.pos.x, self.pos.y, self.pos.w, epsilon)
            rect.move_ip(-self.game.camera.pos.x, -self.game.camera.pos.y)           
            pygame.draw.rect(surface,self.adjustColor,rect)
        if self.mouseOnBottom(epsilon):
            adjust = True
            rect = Rect(self.pos.x, self.pos.y + self.pos.h - epsilon, 
                    self.pos.w, epsilon)
            rect.move_ip(-self.game.camera.pos.x, -self.game.camera.pos.y)           
            pygame.draw.rect(surface,self.adjustColor,rect)
        if not adjust and self.mouseOver():
            pygame.draw.rect(surface,self.activeColor,renderpos)
            pygame.draw.rect(surface,(0,0,0),renderpos.inflate(-epsilon,-epsilon),epsilon)

        