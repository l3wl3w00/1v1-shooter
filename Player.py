
from RocketLauncher import RocketLauncher
from Shotgun import Shotgun
import pygame
from pygame import math
from pygame.sprite import collide_circle
from GrenadeLauncher import GrenadeLauncher
from Pistol import Pistol
from Vector import Vector
from AK import AK

class PlayerState:
    def __init__(self):
        self.jumping = False
        self.squatting = False
        self.inAir = False

Rect = pygame.Rect
class Player:
    def __init__(self, id,imgs:dict,game,pos:Rect,vel = 10, jumpVel = 20, dmg = 1, hp = 250, facing = 1):
        self.pos:Rect = pos
        self.id = id
        self.game = game
        self.imgs = imgs
        self.vel = vel
        self.jumpVel = jumpVel
        self.velBoost = 0

        if id == 0:
            self.hpColor = (200,0,0)
        elif id == 1:
            self.hpColor = (0,200,0)

        self.weapon = RocketLauncher(self.game,self)
        self.acc = Vector(0,0)
        self.velFromOther = Vector(0,0)
        self.velFromControl = Vector(0,0)
        self.velFromExplosion = Vector(0,0)
        self.explosionTime = 0

        self.dmg = dmg
        self.hp = hp
        self.maxHp = hp
        self.facing = facing
        self.maxjumps = 2
        self.jumpCount = 0
        self.shieldDuration = 0
        self.score = 0
        self.scoreTime = 2*self.game.fps
        self.scoreCountDown = self.scoreTime
        self.scoreFont = pygame.font.SysFont('Consolas',25,1)

        self.left = False
        self.right = False
        self.jump = False
        self.shoot = False
        self.readyToAtk = False
        self.autoShoot = False
        self.shielded = False

        self.exists = True

        self.walkCount = 0
        self.airTime = 0
        self.atkTime = 0
        self.fastCount = 0
        self.state = PlayerState()
    def speedUp(self,amount,time):
        if self.fastCount <= 0:
            self.vel += amount
        else:
            self.fastCount += time
        self.velBoost = amount
        self.fastCount = time*self.game.fps
    def stop(s,x = True,y = True):
        if x:
            s.velFromExplosion.x = 0
            s.velFromControl.x = 0
            s.velFromOther.x = 0
        if y:
            s.velFromExplosion.y = 0
            s.velFromControl.y = 0
            s.velFromOther.y = 0
    def getVel(self):
        return self.velFromControl + self.velFromOther
                #+ self.velFromExplosion
    def getBottom(self):
        return self.bottomleft,self.bottomright
    
    def move(self):
        
        self.pos.move_ip(self.getVel().x,self.getVel().y)
        #self.pos.move_ip(self.velFromControl,0)
    
    def hitByExplosion(self,explosion):
        self.changeHp(-explosion.dmg)
        xDiff = self.pos.center[0]-explosion.pos.x
        yDiff = self.pos.center[1]-explosion.pos.y
        lenght = ((xDiff**2+yDiff**2)**0.5)
        if lenght == 0:
            unitVector = Vector(0,0)
        else:
            unitVector = Vector(xDiff/lenght,yDiff/lenght)
        self.velFromOther += unitVector*explosion.knockback
        self.velFromExplosion += unitVector*explosion.knockback
        self.explosionTime = explosion.knockbackTime*self.game.fps

    def collideAnyBlock(self):
        res = False
        for block in self.game.map.blocks:
            # if self.id == 1:
            #     print("block pos:", block.extend())
            #     print("self.pos:",self.pos)
            if self.pos.colliderect(block.extend(2)):
                res = True
                # print("collide")
        return res

    def nextFrameCollide(self):
        newRect = Rect(self.pos.x+self.getVel().x,
                       self.pos.y + self.getVel().y,
                       self.pos.w,self.pos.h)

        for block in self.game.map.blocks:
            # make it 1 pixel wider cos it doesnt detect collision on the borders otherwise
            blockPos = block.extend(2)
            #blockPos = block.pos
            if newRect.colliderect(blockPos):
                if not block.topAccesable:
                    # if the current pos is above the block, but the next is inside
                    if self.pos.bottom < block.pos.y and newRect.bottom >= block.pos.y:
                        self.state.inAir = False
                        print("not in air")
                        self.jumpCount = 0
                        self.pos.y = block.pos.y-self.pos.h-1
                        self.stop(x = False)
                if not block.botAccesable:
                    # if the current pos is below the block, but the next is inside
                    if self.pos.top > block.pos.bottom and newRect.top <= block.pos.bottom:
                        self.pos.y = block.pos.bottom+1
                        self.stop(x = False)
                if not block.rightAccesable:
                    # if the current pos is on the right the block, but the next is inside
                    if self.pos.right < block.pos.x and newRect.right >= block.pos.x:
                        self.pos.x = block.pos.x-self.pos.w-1
                        self.stop(y = False)
                if not block.leftAccesable:
                    # if the current pos is on the left the block, but the next is inside
                    if self.pos.x > block.pos.right and newRect.x <= block.pos.right:
                        self.pos.x = block.pos.right+1
                        self.stop(y = False)
    def shootBullet(self):
        if self.readyToAtk:
            self.readyToAtk = False
            w = 8
            if self.facing == 1:
                #self.game.bullets.append(Bullet(self.game,self,10,Rect(self.pos.right, self.pos.centery-10,w,4)))
                self.weapon.shoot(Rect(self.pos.right, self.pos.centery-10,w,4))
            else:
                self.weapon.shoot(Rect(self.pos.left+w, self.pos.centery-10,w,3))
                #self.game.bullets.append(Bullet(self.game,self,10,Rect(self.pos.left+w, self.pos.centery-10,w,3)))
    def control(self):
        self.setVel()
        if self.weapon.auto:
            if self.autoShoot:
                self.shootBullet()
        else:
            if self.shoot:
                self.shootBullet()
    def handleTimers(self):
        if self.shieldDuration > 0:
            self.shieldDuration -= 1
        else:
            self.shielded = False
        # if self.score > 0:
        #     self.scoreCountDown -= 1
        # if self.scoreCountDown <= 0:
        #     self.score -= 1
        #     self.scoreCountDown = self.scoreTime
        if self.fastCount > 0:
                self.fastCount -= 1
        else:
            self.vel -= self.velBoost
            self.velBoost = 0
    def setVel(self):
        
        self.velFromControl.x = 0
        if self.left:
            self.facing = -1
            self.velFromControl.x -= self.vel
        if self.right:
            self.facing = 1
            self.velFromControl.x += self.vel

        if self.jump:
            # limitáljuk a levegőben ugrálások számát
            if not(self.state.inAir and self.jumpCount >= self.maxjumps):
                self.state.inAir = True
                self.jumpCount += 1
                self.velFromOther.y = -self.jumpVel
    def setHp(self,value):
        if value < self.hp and self.shielded:
            pass
        else:
            self.hp = value
        
    def changeHp(self,value):
        if value < 0 and self.shielded:
            pass
        else:
            self.hp += value
    def handleAtk(self):
        self.atkTime += 1
        if self.atkTime >= self.weapon.timeBtwAttacks:
            self.readyToAtk = True
            self.atkTime = 0
    def drawHpBar(self,surface ):
        pygame.draw.rect(surface,self.hpColor,(self.renderpos.x-50+self.renderpos.w//2,self.renderpos.y-30,round((self.hp/self.maxHp)*100),20))
        pygame.draw.rect(surface,(0,0,0),(self.renderpos.x-50+self.renderpos.w//2,self.renderpos.y-30,100,20),3)
    def drawRank(self,surface):
        rank = "##"
        if 0 <= self.score < 15:
            rank = "hurka"
        elif 15 <= self.score < 30:
            rank = "rigófütty"
        elif 30 <= self.score < 45:
            rank = "gyászhuszár"
        elif 45 <= self.score < 60:
            rank = "tűzegér"
        elif 60 <= self.score < 75:
            rank = "csillagromboló"
        elif self.score >= 75:
            rank = "Pityke őrmester"
        self.scoreSurface = self.scoreFont.render( rank+" "+str(self.score), True, (70,70,70))
        rect = self.scoreSurface.get_rect()
        
        rect.center = self.renderpos.center[0], self.renderpos.center[1]-self.pos.h
        
        surface.blit(self.scoreSurface,rect)
    def tick(self):
        #self.checkGround()
        if self.exists:
            
            if not self.collideAnyBlock():
                print("in air")
                self.state.inAir = True
            if self.state.inAir:
                self.airTime += 1
                self.acc.y = self.game.gravity.y
            else:
                self.acc.y = 0
                self.velFromOther.y = 0
                self.airTime = 0
            self.velFromOther += self.acc
            
            self.control()
            for bullet in self.game.bullets:
                if bullet.damagedPlayer == self:
                    if bullet.active:
                        bullet.hitEffect(self)
            self.nextFrameCollide()
            if self.state.inAir:
                print("inAir:", self.state.inAir)
                fluidRes = self.game.fluidRes.x*self.velFromOther.x
                self.velFromOther.x -= fluidRes
            self.move()
            
            self.handleAtk()
            for block in self.game.map.blocks:
                if block.extend(2).colliderect(self.pos):
                    self.velFromOther.x -= block.friction.x*self.velFromOther.x
            if abs(self.velFromOther.x) < 1:
                self.velFromOther.x = 0


            self.handleTimers()
            if self.hp <= 0:
                self.exists = False
    def render(self,surface):
        if self.exists:
            if self.getVel().x != 0:
                self.walkCount += 1
            
            if self.walkCount == 7*6:
                self.walkCount = 0

            self.renderpos = self.pos.copy()
            self.renderpos.x -= self.game.camera.pos.x
            self.renderpos.y -= self.game.camera.pos.y
            if self.facing == 1:
                if self.getVel().x != 0:
                    surface.blit(pygame.transform.flip(self.imgs["moving"][self.walkCount//6],True,False),(self.renderpos.x-30,self.renderpos.y-10))
                    self.weapon.render(self.game.win,True)
                    surface.blit(pygame.transform.flip(self.imgs["arm"][0],True,False),(self.renderpos.x-30,self.renderpos.y-10))
                else:
                    surface.blit(pygame.transform.flip(self.imgs["idle"][0],True,False),(self.renderpos.x-30,self.renderpos.y-10))
                    self.weapon.render(self.game.win,True)
                    surface.blit(pygame.transform.flip(self.imgs["arm"][0],True,False),(self.renderpos.x-30,self.renderpos.y-10))
            else:
                if self.getVel().x != 0:
                    surface.blit(self.imgs["moving"][self.walkCount//6],(self.renderpos.x-30,self.renderpos.y-10))
                    self.weapon.render(self.game.win)
                    surface.blit(self.imgs["arm"][0],(self.renderpos.x-30,self.renderpos.y-10))
                else:
                    surface.blit(self.imgs["idle"][0],(self.renderpos.x-30,self.renderpos.y-10))
                    self.weapon.render(self.game.win)
                    surface.blit(self.imgs["arm"][0],(self.renderpos.x-30,self.renderpos.y-10))
            if self.shielded:
                rect = self.game.shieldEffectImg.get_rect()
                rect.center = self.renderpos.center
                surface.blit(self.game.shieldEffectImg,(rect.x,rect.y))
            self.drawHpBar(surface)
            self.drawRank(surface)
        #ygame.draw.rect(surface,(255,0,0),renderpos,2)

        
        
        
        
        
        
        