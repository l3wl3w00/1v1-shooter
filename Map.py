from ShieldCollectible import ShieldCollectible
from SpeedUpCollectible import SpeedUpCollectible
from HealCollectible import HealCollectible
from Collectible import Collectible
from WeaponBoxSpawner import WeaponBoxSpawner
from WeaponBox import WeaponBox
from View import View


class Map:
    def __init__(self,game,name,blocks,collSpawners, playerSpawns):
        self.name = name
        self.blocks = blocks
        self.collSpawners = collSpawners
        self.playerSpawns = playerSpawns
        self.game = game
    def tick(self):
        for block in self.blocks:
            block.tick()
        for collSpawn in self.collSpawners:
            collSpawn.tick()
    def render(self, surface):
        for block in self.blocks:
            block.render(surface)
        if self.game.view == View.mapMaker:
            for collSpawn in self.collSpawners:
                collSpawn.render(self.game.win)
    def save(self):
        self.name = self.game.mapMakerMenu.buttons[1].text
        with open("files/maps.txt","a") as maps:
            maps.write(self.name)
            maps.write("_")
            for block in self.blocks:
                maps.write(f"|{block.pos.x} {block.pos.y} {block.pos.w} {block.pos.h}")
                maps.write(f" {block.rightAccesable} {block.leftAccesable} {block.topAccesable} {block.botAccesable}")
            maps.write("_")
            for collSpawn in self.collSpawners:
                maps.write(f"|{collSpawn.pos.x} {collSpawn.pos.y} {collSpawn.pos.w} {collSpawn.pos.h}")
                maps.write(f" {collSpawn.drag} {collSpawn.frequency/self.game.fps} ")
                if isinstance(collSpawn,WeaponBoxSpawner):
                    maps.write("weaponbox")
                elif isinstance(collSpawn.coll,HealCollectible):
                    maps.write("heal")
                elif isinstance(collSpawn.coll,SpeedUpCollectible):
                    maps.write("speed")
                elif isinstance(collSpawn.coll,ShieldCollectible):
                    maps.write("shield")
            maps.write("_")
            for playerSpawn in self.playerSpawns:
                maps.write(f"|{playerSpawn.pos.x} {playerSpawn.pos.y} {playerSpawn.pos.w} {playerSpawn.pos.h}")
                maps.write(f" {playerSpawn.id}")
            maps.write("\n")
