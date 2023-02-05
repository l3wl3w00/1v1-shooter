from Grenade import Grenade
from Weapon import Weapon
class GrenadeLauncher(Weapon):
    def __init__(self,game, owner):
        super().__init__(game,10,owner,game.grenadeLauncherImg,1.5)
    def shoot(self,pos):
        pos.w = 20
        pos.h = 20
        self.game.bullets.append(Grenade(self.game,self.owner,self.dmg,pos))