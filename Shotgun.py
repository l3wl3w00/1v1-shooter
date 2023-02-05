from Pellet import Pellet
from Vector import Vector
from PistolBullet import PistolBullet
from Weapon import Weapon
import math
class Shotgun(Weapon):
    def __init__(self,game,owner):
        super().__init__(game,4,owner,game.shotgunImg,1.0)
    def shoot(self,pos):
        pos.w = 4
        pos.h = 4
        r = 30
        if self.owner.facing == 1:
            for angle in range(-20,21,4):
                x = r*math.cos(math.radians(angle))
                y = r*math.sin(math.radians(angle))
                self.game.bullets.append(Pellet(self.game,self.owner,self.dmg,pos,Vector(x,y),1))
        elif self.owner.facing == -1:
            for angle in range(200,159,-4):
                x = r*math.cos(math.radians(angle))
                y = r*math.sin(math.radians(angle))
                self.game.bullets.append(Pellet(self.game,self.owner,self.dmg,pos,Vector(x,y),1))

        