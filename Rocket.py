import math

import pygame
from Circle import Circle
from Explosion import Explosion
from Bullet import Bullet
class Rocket(Bullet):
    def __init__(self,game,shooter,dmg, pos,score = 3,lifetime = 6):
        super().__init__(game,shooter,dmg, pos,score,lifetime)
        self.img = game.rocketImg
        self.vel = 12
        self.target = None
        self.targetTime = 1*game.fps
        self.goalPos = self.pos
        self.xStep = 0
        self.xStepCount = 0
        self.yStep = 0
        self.yStepCount= 0
        self.yDiff = 0
        self.xDiff = 0
    def setGoalPos(self,pos):
        x,y = pos.center
        self.goalPos = pos.center
        self.xDiff = x - self.pos.x
        self.yDiff = y - self.pos.y
        distance = math.hypot(self.pos.x-x,self.pos.y-y)

        try:
            self.xStep = self.xDiff / (distance/self.vel)
            self.xStepCount = round(self.xDiff / self.xStep)
        except ZeroDivisionError:
            self.xStepCount = 0
        try:
            self.yStep = self.yDiff / (distance/self.vel)
            self.yStepCount = round(self.yDiff / self.yStep)
        except ZeroDivisionError:
            self.yStepCount = 0  
    def move(self):
        if self.target == None:
            self.pos.move_ip(self.vel*self.facing,0)
        else:
            self.setGoalPos(self.target.pos)
            if self.xStepCount > 0:
                self.pos.x += self.xStep
                self.xStepCount -= 1

            if self.yStepCount > 0:
                self.pos.y += self.yStep
                self.yStepCount -= 1

            if self.yStepCount == 0:
                self.pos.y = self.goalPos[1]
            if self.xStepCount == 0:
                self.pos.x = self.goalPos[0]
    
    def render(self, surface):
        renderpos = self.pos.copy()
        renderpos.x -= self.game.camera.pos.x
        renderpos.y -= self.game.camera.pos.y
        if self.target != None:
            if self.yDiff != 0:
                angle = math.degrees(math.atan(self.xDiff/self.yDiff))
                angle += 90
                if self.yDiff < 0:
                    angle += 180

            elif self.yDiff == 0 and self.xDiff != 0:
                if self.xDiff > 0:
                    angle = 180
                else:
                    angle = 0
            surface.blit(pygame.transform.rotate(self.img,angle),(renderpos.x,renderpos.y))
        else:
            if self.facing == -1:
                surface.blit(self.img,(renderpos.x,renderpos.y))
            elif self.facing == 1:
                surface.blit(pygame.transform.flip(self.img,True,False),(renderpos.x,renderpos.y))
    def explode(self):
        self.game.bullets.append(
                    Explosion(Circle(
                        self.pos.x,self.pos.y,70
                        ),self.game,self.shooter,self.dmg*2
                    )
                )
    def distance(self,player):
        x1 = player.pos.center[0]
        x2 = self.pos.center[0]
        y1 = player.pos.center[1]
        y2 = self.pos.center[1]
        return math.sqrt( ((x1-x2))**2+((y1-y2)**2))
    def searchTarget(self):
        for player in self.game.players:
            if self.target == None:
                self.target = player
            if self.distance(player) < self.distance(self.target):
                self.target = player

    def hitEffect(self,player):
        player.changeHp(-self.dmg)
        self.shooter.score += self.score
    def tick(self):
        self.lifetime -= 1
        if self.targetTime > 0:
            self.targetTime -= 1
        elif self.targetTime == 0:
            self.searchTarget()
            self.targetTime -= 1
        self.move()
        for block in self.game.map.blocks:
            if self.pos.colliderect(block.extend()):
                self.explode()
                self.exists = False
        for player in self.game.players:
            if self.pos.colliderect(player.pos):
                self.explode()
                self.damagedPlayer = player
                self.exists = False
        if self.lifetime == 0:
            self.explode()
            self.exists = False