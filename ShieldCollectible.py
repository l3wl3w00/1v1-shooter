from Collectible import Collectible
class ShieldCollectible(Collectible):
    def __init__(self,game,pos,lifetime = 15):
        super().__init__(game,pos,game.shieldPlayer,(0,100,100),lifetime)
    def copy(self):
        return ShieldCollectible(self.game,self.pos, self.lifetime/self.game.fps)
