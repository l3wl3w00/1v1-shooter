from Collectible import Collectible
class SpeedUpCollectible(Collectible):
    def __init__(self,game,pos,lifetime = 15):
        super().__init__(game,pos,game.speedUp,(0,0,100),lifetime)
    def copy(self):
        return SpeedUpCollectible(self.game,self.pos, self.lifetime/self.game.fps)
