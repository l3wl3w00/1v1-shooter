
from Collectible import Collectible
class HealCollectible(Collectible):
    def __init__(self,game,pos,lifetime = 15):
        super().__init__(game,pos,game.healPlayer,(0,100,0),lifetime)
    def copy(self):
        return HealCollectible(self.game,self.pos, self.lifetime/self.game.fps)