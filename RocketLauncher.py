from Rocket import Rocket
from Weapon import Weapon


class RocketLauncher(Weapon):
    def __init__(self,game,owner):
        super().__init__(game,30,owner,game.rpgImg,0.3)
    def shoot(self,pos):
        if self.owner.facing == 1:
            pos.x += 5
        elif self.owner.facing == -1:
            pos.x -= 40
        pos.w = 15
        pos.h = 15
        self.game.bullets.append(Rocket(self.game,self.owner,self.dmg,pos,2))