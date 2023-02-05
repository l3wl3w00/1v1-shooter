from Collectible import Collectible
class WeaponBox(Collectible):
    def __init__(self,game,pos, weapon):
        super().__init__(game,pos,None,(165,42,42))
        self.weapon = weapon
        print("box weapon type:",type(self.weapon))

    def tick(self):
        for player in self.game.players:
            if player.pos.colliderect(self.pos):
                self.exists = False
                player.weapon = self.weapon
                self.weapon.owner = player