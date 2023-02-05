from PistolBullet import PistolBullet
from Weapon import Weapon
class Pistol(Weapon):
    def __init__(self,game, owner):
        super().__init__(game,4,owner,game.pistolImg,4.0)
    def shoot(self,pos):
        self.game.bullets.append(PistolBullet(self.game,self.owner,self.dmg,pos,2))
    