from Collectible import Collectible


class Portal:
    def __init__(self,game,pos1,pos2):
        self.game = game
        self.coll1 = Collectible(game,pos1,None)
        self.pos2 = pos2