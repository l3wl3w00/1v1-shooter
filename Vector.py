class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    @classmethod
    def fromTuple(cls,t):
        if len(t) != 2:
            return None
        return Vector(t[0],t[1])
    def toTuple(self):
        return self.x,self.y
    def copy(self):
        return Vector(self.x,self.y)
    def __add__(self,v2):
        return Vector(self.x+v2.x,self.y+v2.y)
    def __sub__(self,v2):
        return Vector(self.x-v2.x,self.y-v2.y)
    def __mul__(self,num):
        return Vector(self.x*num,self.y*num)
    def __repr__(self) -> str:
        return f"Vector: ({self.x},{self.y})"