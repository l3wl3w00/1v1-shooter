from Vector import Vector
import pygame
class Camera:
    def __init__(self,x = 0,y = 0) -> None:
        self.pos = Vector(x,y)
        self.vel = Vector(0,0)
    def tick(self):
        self.pos += self.vel
    