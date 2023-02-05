from Weapon import Weapon
from PistolBullet import PistolBullet
class AK(Weapon):
    def __init__(self,game, owner):
        super().__init__(game,8,owner,game.akImg,8.0,True)
    def shoot(self,pos):
        pos.y += 3
        self.game.bullets.append(PistolBullet(self.game,self.owner,self.dmg,pos))