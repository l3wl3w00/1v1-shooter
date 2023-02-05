from Vector import Vector
from View import View
from pygame.rect import Rect


class CollectibleSpawner:
    def __init__(self,game,pos,coll, drag = True,frequency = 30.0):
        self.game = game
        self.pos = pos
        self.coll = coll
        self.inAir = False
        self.frequency = game.fps*frequency
        self.counter = self.frequency - 5*self.game.fps
        self.airTime = 0
        self.drag = drag
        self.currVel = Vector(0,0)
        
    def mouseOver(self):
        return self.pos.collidepoint((self.game.handler.relativeMx,self.game.handler.relativeMy))

    def render(self,surface):

        self.coll.render(surface)

    def collideAnyBlock(self):
        res = False
        for block in self.game.map.blocks:
            if self.pos.colliderect(block.pos):
                res = True
        return res
    def nextFrameCollide(self):
        newRect = Rect(self.pos.x+self.currVel.x,
                       self.pos.y + self.currVel.y,
                       self.pos.w,self.pos.h)

        for block in self.game.map.blocks:
            # make it 1 pixel wider cos it doesnt detect collision on the borders otherwise
            blockPos = block.pos.inflate(1,1)
            #blockPos = block.pos
            if newRect.colliderect(blockPos):
                if not block.topAccesable:
                    # if the current pos is above the block, but the next is inside
                    if self.pos.bottom < block.pos.y and newRect.bottom >= block.pos.y:
                        self.inAir = False
                        self.pos.y = block.pos.y-self.pos.h+1
                        self.currVel.y = 0
                if not block.botAccesable:
                    # if the current pos is below the block, but the next is inside
                    if self.pos.top > block.pos.bottom and newRect.top <= block.pos.bottom:
                        self.pos.y = block.pos.bottom+1
                        self.currVel.y = 0
                if not block.rightAccesable:
                    # if the current pos is on the right the block, but the next is inside
                    if self.pos.right < block.pos.x and newRect.right >= block.pos.x:
                        self.pos.x = block.pos.x-self.pos.w-1
                        self.currVel.x = 0
                if not block.leftAccesable:
                    # if the current pos is on the left the block, but the next is inside
                    if self.pos.x > block.pos.right and newRect.x <= block.pos.right:
                        self.pos.x = block.pos.right+1
                        self.currVel.x = 0
    def move(self):
        self.pos.move_ip(self.currVel.x,self.currVel.y)
    def spawn(self):
        self.coll.pos = self.pos
        self.game.collectibles.append(self.coll.copy())
    
    def tick(self):
        if self.game.view ==  View.game:
            self.counter += 1
            if self.counter  >= self.frequency:
                self.counter = 0
                self.spawn()
        elif self.game.view == View.mapMaker:
            if self.coll != None:
                self.coll.pos = self.pos
            if self.game.handler.mouseDown:
                if self.mouseOver():
                    self.drag = True
            if self.game.handler.mouseUp:
                self.drag = False
            if self.drag:
                self.pos.center = self.game.handler.relativeMx,self.game.handler.relativeMy
            else:
                if not self.collideAnyBlock():
                    self.inAir = True
            if self.inAir:
                self.airTime += 1
                self.currVel.y += self.game.gravity.y
            else:
                self.currVel.y = 0
                self.airTime = 0
            self.nextFrameCollide()
            self.move()
