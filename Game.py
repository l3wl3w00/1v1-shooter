from Button import Button
from PlayerSpawner import PlayerSpawner
from Shotgun import Shotgun
from RocketLauncher import RocketLauncher
from ShieldCollectible import ShieldCollectible
from SpeedUpCollectible import SpeedUpCollectible
from HealCollectible import HealCollectible
from WeaponBoxSpawner import WeaponBoxSpawner
from CollectibleSpawner import CollectibleSpawner
from View import View
from Collectible import Collectible
from MapSelectButton import MapSelectButton
from InputText import InputText
from Camera import Camera
from TextButton import TextButton
from ImgButton import ImgButton
from Menu import Menu
from Lazer import Lazer
from Pistol import Pistol
from WeaponBox import WeaponBox
import pygame
import random
from pygame.image import load
from EventHandler import EventHandler
from Player import Player
from Block import Block
from GrenadeLauncher import GrenadeLauncher
from Vector import Vector
from AK import AK
from Map import Map

Rect = pygame.Rect
def loadImage(fileName, convert = False):
    if convert:
        return pygame.image.load("Pics/"+fileName).convert()
    else:
        return pygame.image.load("Pics/"+fileName)
def midpoint(p1, p2):
    return (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
def strBool(str):
    if str == "True":
        return True
    elif str == "False":
        return False

class Game:
    def __init__(self):
        self.fps = 60
        self.run = True
        self.view = View.menu
        self.tempView = View.menu
        self.handler = EventHandler()
        self.clock = pygame.time.Clock()
        self.bgColor = (70,150,50)
        #self.win = pygame.display.set_mode((1280,720))
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.w, self.h = pygame.display.get_surface().get_size()
        self.middle = Vector(self.w/2,self.h/2)
        
        self.gravity = Vector(0,60/self.fps)
        self.fluidRes = Vector(0.03,0)
        self.weaponSpawnTime = 10*self.fps
        self.weaponTypes = [GrenadeLauncher,Lazer,AK,RocketLauncher,Shotgun]
        self.playerSpawners = [
            PlayerSpawner(Rect(800,300,44,83),0,self),
            PlayerSpawner(Rect(100,300,44,83),1,self)
        ]
        blocks = [
            Block(pygame.Rect(-5000,541,10000,100),self),Block(pygame.Rect(300,400,100,300),self),
            Block(pygame.Rect(500,300,600,100),self),Block(pygame.Rect(500,150,100,40),self,True,True,False,True)
        ]
        
        self.maps = []
        self.loadMaps()
        if self.maps == []:
            self.map = Map(self,"",blocks,[],[PlayerSpawner(Rect(100,300,44,83),0,self),PlayerSpawner(Rect(800,300,44,83),1,self)])
        else:
            self.map = self.maps[0]
        self.loadimages()
        self.initMenus()
        self.initGame()
   
    def initMapSelectMenu(self):
        self.mapSelectMenu = Menu(self,[TextButton(Rect(self.w-200,self.h-100,150,40),"Back",self.toMenu)])
        for i,map in enumerate(self.maps):
            self.mapSelectMenu.buttons.append(
                MapSelectButton(
                    self,Rect(100,100+i*100,200,40),map
                )
            )
        self.mapSelectMenu.buttons.append(
            TextButton(
                    Rect(self.h-200,self.w-200,100,40),"Edit",self.toMapMakerEdit
                )
            )
    
    def loadMaps(self):
        self.maps = []
        with open("files/maps.txt","r") as maps:
            for line in maps:
                line = line.split("_")
                name = line[0]
                line[1] = line[1].split("|") #blocks
                line[2] = line[2].split("|") #spawners
                if len(line) == 4:
                    line[3] = line[3].split("|") #player spawners
                blocks = []
                for block in line[1][1:]:
                    block = block.split()
                    newBlock = Block(
                        Rect(
                            int(block[0]),int(block[1]),
                            int(block[2]),int(block[3])
                        ),
                        self,strBool(block[4]),strBool(block[5]),strBool(block[6]),strBool(block[7])
                    )
                    blocks.append(newBlock)
                spawners = []
                for spawner in line[2][1:]:
                    spawner = spawner.split()
                    if spawner[6] == "weaponbox":
                        newSpawner = WeaponBoxSpawner(self,Rect(
                            int(spawner[0]),int(spawner[1]),
                            int(spawner[2]),int(spawner[3])
                            ),strBool(spawner[4]),float(spawner[5])
                        )
                    elif spawner[6] == "heal":
                        coll = HealCollectible(self,Rect(
                                int(spawner[0]),int(spawner[1]),
                                int(spawner[2]),int(spawner[3])
                            ))
                        newSpawner = CollectibleSpawner(
                            self,Rect(
                                int(spawner[0]),int(spawner[1]),
                                int(spawner[2]),int(spawner[3])
                            ),coll,strBool(spawner[4]),float(spawner[5])
                        )
                    elif spawner[6] == "speedup":
                        coll = SpeedUpCollectible(self,Rect(
                                int(spawner[0]),int(spawner[1]),
                                int(spawner[2]),int(spawner[3])
                            ))
                        newSpawner = CollectibleSpawner(
                            self,Rect(
                                int(spawner[0]),int(spawner[1]),
                                int(spawner[2]),int(spawner[3])
                            ),coll,strBool(spawner[4]),float(spawner[5])
                        )
                    elif spawner[6] == "shield":
                        coll = ShieldCollectible(self,Rect(
                                int(spawner[0]),int(spawner[1]),
                                int(spawner[2]),int(spawner[3])
                            ))
                        newSpawner = CollectibleSpawner(
                            self,Rect(
                                int(spawner[0]),int(spawner[1]),
                                int(spawner[2]),int(spawner[3])
                            ),coll,strBool(spawner[4]),float(spawner[5])
                        )
                    spawners.append(newSpawner)
                playerSpawns = []
                for spawn in line[3][1:]:
                    spawn = spawn.split()
                    newSpawn = PlayerSpawner(Rect(
                            int(spawn[0]),int(spawn[1]),
                            int(spawn[2]),int(spawn[3])
                        ),int(spawn[4]),self
                    )
                    playerSpawns.append(newSpawn)
                self.maps.append(Map(self,name,blocks,spawners,playerSpawns))

    def initGame(self):
        self.camera = Camera()
        self.bgCamera = Camera()
        self.weaponSpawnCounter = self.weaponSpawnTime
        self.players = [
            Player(0,self.char1Imgs,self,self.map.playerSpawns[0].pos.copy()),
            Player(1,self.char2Imgs,self,self.map.playerSpawns[1].pos.copy())
        ]
        
        self.bullets = []
        self.collectibles = []
    def initMenus(self):
        buttons = [ 
            TextButton(Rect(100,100,150,40),"Play",self.toGame),
            TextButton(Rect(100,200,150,40),"Map Maker",self.toMapMaker),
            TextButton(Rect(100,300,150,40),"Select Map",self.toMapSelect),
            TextButton(Rect(100,400,150,40),"Quit",self.quit)
        ]
        self.mainMenu = Menu(self,buttons)
        buttons2 = [ImgButton(
                        Rect(50,self.h-85,50,50),self.blockButtonImg,
                        lambda: self.newBlock(Block(
                            Rect(500,620,100,100),self,False,False,False,False,True,False
                            )
                        ),
                        False
                    ),
                    # Az inputtext gombnak mindig a 2. helyen kell lennie ebben a listában
                    InputText(self,Rect(self.w-450,self.h-100,200,40),self.saveMap),
                    ImgButton(
                        Rect(120,self.h-85,50,50),self.healButtonImg,
                        lambda: self.newCollSpawner(CollectibleSpawner(
                            self,Rect(500,620,50,50),
                            HealCollectible(self,Rect(300,self.h-100,50,50)))
                        ),
                        False
                    ),
                    ImgButton(
                        Rect(190,self.h-85,50,50),self.speedUpButtonImg,
                        lambda: self.newCollSpawner(CollectibleSpawner(
                            self,Rect(500,620,50,50),
                            SpeedUpCollectible(self,Rect(300,self.h-100,50,50)))
                        ),
                        False
                    ),
                    ImgButton(
                        Rect(260,self.h-85,50,50),self.shieldButtonImg,
                        lambda: self.newCollSpawner(CollectibleSpawner(
                            self,Rect(500,620,50,50),
                            ShieldCollectible(self,Rect(300,self.h-100,50,50)))
                        ),
                        False
                    ),
                    ImgButton(
                        Rect(330,self.h-85,50,50),self.weaponBoxButtonImg,
                        lambda: self.newCollSpawner(WeaponBoxSpawner(
                            self,Rect(500,620,50,50)
                        )),
                        False
                    ),
                    TextButton(Rect(self.w-200,self.h-100,150,40),"Back",self.toMenu)
        ]


        self.mapMakerMenu = Menu(self,buttons2)
        buttons3 = [TextButton(Rect(self.w-200,self.h-100,150,40),"Back",self.toMenu)]
        self.gameMenu = Menu(self,buttons3)
        self.initMapSelectMenu()
    def loadimages(self):

        self.bgImg = loadImage("bg_nagy.png",True)
        self.bgRect = self.bgImg.get_rect()
        self.blockButtonImg = loadImage("Interface/newBlock.png",True)
        self.weaponBoxButtonImg = loadImage("Interface/weapon.png",True)
        self.healButtonImg = loadImage("Interface/heal.png",True)
        self.speedUpButtonImg = loadImage("Interface/speedUp.png",True)
        self.shieldButtonImg = loadImage("Interface/shield.png",True)

        self.shotgunImg = loadImage("weapons/shotgun.png")
        self.rpgImg = loadImage("weapons/RocketLauncher.png")
        self.rocketImg = pygame.transform.scale(loadImage("weapons/rocket.png"),(33,11))
        self.lazerImg = loadImage("weapons/lazerGunBig.png")
        self.akImg =  loadImage("weapons/ak47.png")
        self.pistolImg = loadImage("weapons/pistol.png")
        self.grenadeLauncherImg = loadImage("weapons/grenadeLauncher.png")
        self.char1Imgs = {
                        "arm":(loadImage("Player1/arm.png"),),
                        "moving":(loadImage("Player1/sprite_0.png"),loadImage("Player1/sprite_1.png"),loadImage("Player1/sprite_2.png"),
                        loadImage("Player1/sprite_3.png"),loadImage("Player1/sprite_4.png"),loadImage("Player1/sprite_5.png"),
                        loadImage("Player1/sprite_2.png")),

                        "idle":(loadImage("Player1/sprite_6.png"),)

                        }
        self.char2Imgs = {
                        "arm":(loadImage("Player2/arm.png"),),
                        "moving":(loadImage("Player2/sprite_0.png"),loadImage("Player2/sprite_1.png"),loadImage("Player2/sprite_2.png"),
                        loadImage("Player2/sprite_3.png"),loadImage("Player2/sprite_4.png"),loadImage("Player2/sprite_5.png"),
                        loadImage("Player2/sprite_2.png")),

                        "idle":(loadImage("Player2/sprite_6.png"),)

                        }
        self.shieldEffectImg = loadImage("effects/shield.png")


    def speedUp(self,player):
        player.speedUp(10,5)
    
    def saveMap(self):
        self.map.save()
        self.loadMaps()
    def quit(self):
        self.run = False
    def setMap(self,map):
        self.map = map
    def healPlayer(self,player,hp = 25):
        if player.hp + hp > player.maxHp:
            player.setHp(player.maxHp)
        else:
            player.changeHp(hp)
    def shieldPlayer(self,player,duration = 4):
        player.shielded = True
        player.shieldDuration += duration*self.fps

    def toMapMaker(self):
        self.tempView = View.mapMaker
        self.map = Map(self,"temp",[Block(pygame.Rect(-5000,541,10000,100),self)],[],self.playerSpawners)
    def toMapMakerEdit(self):
        for block in self.map.blocks:
            block.final = False
        self.tempView = View.mapMaker
    def toMapSelect(self):
        self.initMapSelectMenu()
        self.tempView = View.mapSelect
    def toMenu(self):
        self.tempView = View.menu
    def toGame(self):
        self.tempView = View.game
        if len(self.maps) > 0 and self.map not in self.maps:
            self.map = self.maps[0]
        self.initGame()
        
    def newBlock(self,block):
        self.map.blocks.append(block)
    def newCollSpawner(self,spawner):
        self.map.collSpawners.append(spawner)
    def reset(self):
        self.camerapos = (0,0)
        for block in self.map.blocks:
            block.final = True
    def setView(self):
        if self.tempView == View.menu and self.tempView != self.view:
            self.reset()
        self.view = self.tempView
    def eventHandle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.MOUSEBUTTONUP:
                self.handler.mouseUp = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handler.mouseDown = True
            if event.type == pygame.KEYDOWN:
                self.handler.currEvent = event
                if event.key == pygame.K_LEFT:
                    self.handler.leftHold = True
                if event.key == pygame.K_RIGHT:
                    self.handler.rightHold = True
                if event.key == pygame.K_UP:
                    self.handler.upDown = True
                if event.key == pygame.K_RETURN:
                    self.handler.spaceDown = True
                    self.handler.spaceHold = True
                
                if event.key == pygame.K_w:
                    self.handler.wDown = True
                if event.key == pygame.K_a:
                    self.handler.aHold = True
                if event.key == pygame.K_s:
                    pass
                if event.key == pygame.K_d:
                    self.handler.dHold = True
                if event.key == pygame.K_t:
                    self.handler.tDown = True
                    self.handler.tHold = True
                if event.key == pygame.K_p:
                    self.initGame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.handler.leftHold = False
                if event.key == pygame.K_RIGHT:
                    self.handler.rightHold = False

                if event.key == pygame.K_w:
                    self.handler.wUp = True
                if event.key == pygame.K_a:
                    self.handler.aHold = False
                if event.key == pygame.K_s:
                    pass
                if event.key == pygame.K_d:
                    self.handler.dHold = False
                if event.key == pygame.K_t:
                    self.handler.tUp = True
                    self.handler.tHold = False
                if event.key == pygame.K_RETURN:
                    self.handler.spaceHold = False
        
    def playerEventHandle(self):
        self.players[0].left = self.handler.aHold
        self.players[0].right = self.handler.dHold
        self.players[0].jump = self.handler.wDown
        self.players[0].shoot = self.handler.tDown
        self.players[0].autoShoot = self.handler.tHold

        self.players[1].left = self.handler.leftHold
        self.players[1].right = self.handler.rightHold
        self.players[1].jump = self.handler.upDown
        self.players[1].shoot = self.handler.spaceDown
        self.players[1].autoShoot = self.handler.spaceHold
        
    def weaponBoxSpawn(self):
        if self.weaponSpawnCounter == 0:
                self.weaponSpawnCounter = self.weaponSpawnTime
                if self.weaponBoxes[0] == None:
                    self.weaponBoxes[0] = WeaponBox(self,Rect(200,490,50,50),random.choice(self.weaponTypes)(self,None))
                    self.weaponBoxes[0] = Collectible(self,Rect(200,490,50,50),self.healPlayer)
        if self.weaponSpawnCounter == self.weaponSpawnTime//3:
            if self.weaponBoxes[1] == None:
                self.weaponBoxes[1] = WeaponBox(self,Rect(700,490,50,50),random.choice(self.weaponTypes)(self,None))
        if self.weaponSpawnCounter == 2*self.weaponSpawnTime//3:
            if self.weaponBoxes[2] == None:
                self.weaponBoxes[2] = WeaponBox(self,Rect(1200,490,50,50),random.choice(self.weaponTypes)(self,None))
            
    def setCameraPos(self):

        P1camerapos = self.players[0].pos.x-self.w//2+self.players[0].pos.w//2,self.players[0].pos.y-self.h//2+self.players[0].pos.h//2
        P2camerapos = self.players[1].pos.x-self.w//2+self.players[1].pos.w//2,self.players[1].pos.y-self.h//2+self.players[1].pos.h//2
        self.camera.pos = Vector.fromTuple(midpoint(P1camerapos,P2camerapos))
        #set the camera pos of the background to the midpoint between the camerapos and the middle
        self.bgCamera.pos = Vector.fromTuple(midpoint(self.camera.pos.toTuple(),self.middle.toTuple())) * -1
  
    def gameViewTick(self):
        self.gameMenu.tick()
        self.map.tick()
        self.playerEventHandle()
        
        for bullet in self.bullets:
            bullet.tick()
        for player in self.players:
            player.tick()
            
        self.setCameraPos()
        for coll in self.collectibles:
            coll.tick()
            if not coll.exists:
                self.collectibles.pop(self.collectibles.index(coll))
        for bullet in self.bullets:
            if not bullet.exists:
                self.bullets.pop(self.bullets.index(bullet))
    def menuViewTick(self):
        self.mainMenu.tick()
    def mapSelectViewTick(self):
        self.mapSelectMenu.tick()
    def mapMakerViewTick(self):
        self.mapMakerMenu.tick()
        self.map.tick()
        for playerSpawner in self.playerSpawners:
            playerSpawner.tick()
        if self.handler.mx > self.w-70:
            self.camera.vel.x = 5
        if self.handler.mx < 70:
            self.camera.vel.x = -5
        if 70 < self.handler.mx < self.w-70:
            self.camera.vel.x = 0

        if self.handler.my > self.h-30:
            self.camera.vel.y = 5
        if self.handler.my < 70:
            self.camera.vel.y = -5
        if 70 < self.handler.my < self.h-30:
            self.camera.vel.y = 0
        self.camera.tick()
    def main(self):
        while self.run:
            self.handler.mx = pygame.mouse.get_pos()[0]
            self.handler.my = pygame.mouse.get_pos()[1]
            self.handler.relativeMx = self.handler.mx+self.camera.pos.x
            self.handler.relativeMy = self.handler.my+self.camera.pos.y
            
            self.clock.tick(self.fps)
            self.eventHandle()
            if self.view == View.game:
                self.gameViewTick()
            elif self.view == View.menu:
                self.menuViewTick()
            elif self.view == View.mapSelect:
                self.mapSelectViewTick()
            elif self.view == View.mapMaker:
                self.mapMakerViewTick()
            self.handler.setAllFalse()
            self.render()
            self.setView()
    def render(self):
        self.win.fill(self.bgColor)
        if self.view == View.game:
            
            self.win.blit(self.bgImg,(self.bgCamera.pos.x-self.bgRect.w/2,self.bgCamera.pos.y-self.bgRect.h/2-500))
            self.map.render(self.win)
            for coll in self.collectibles:
                coll.render(self.win)

            for player in self.players:
                player.render(self.win)
            for bullet in self.bullets:
                bullet.render(self.win)
            self.gameMenu.render()
        elif self.view == View.menu:
            self.mainMenu.render()
        elif self.view == View.mapSelect:
            
            self.mapSelectMenu.render()
        elif self.view == View.mapMaker:
            self.map.render(self.win)
            for playerSpawner in self.playerSpawners:
                playerSpawner.render(self.win)
            pygame.draw.rect(self.win,(255,0,0),(self.w//2 - self.camera.pos.x,self.h//2 - self.camera.pos.y,5,5))
            pygame.draw.rect(self.win,(100,100,100),(0,self.h-120,self.w,120))
            self.mapMakerMenu.render()
        pygame.display.update()