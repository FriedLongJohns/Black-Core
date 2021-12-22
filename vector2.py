# from math import cos,sin
# import numpy as np

class vec2():
    def __init__(self,pos):
        self.pos=list(pos)
        self.dist=0
        self.reload()

    def reload(self):
        self.dist=(self.x*self.x+self.y*self.y)**.5

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value
        self.reload()

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value
        self.reload()

    # @property
    # def angle(self):
    #     return np.degrees(np.arctan2(self.x, self.y)) % 360.0
    #
    # @angle.setter
    # def angle(self, value):
    #     theta = np.deg2rad(value)
    #     rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
    #     end = np.dot(rot, np.array([0,1]))
    #     self.pos=[end[0],end[1]]
    #     self.reload()
    #
    # def rotate(self, angle):
    #     self.angle=self.angle+angle

    @property
    def normal(self):
        mult = 1/self.dist
        return self*mult

    def normalize(self):
        self.x=self.x/self.m
        self.y=self.y/self.m
        self.reload()

    def __mul__(self, value):
        assert isinstance(value, (int, float, complex, vec2))

        if isinstance(value, (int, float, complex)):
            return vec2(*(e*value for e in self))

        return vec2(self.x*value.x, self.y*value.y)

    def __truediv__(self, value):
        assert isinstance(value, (int, float, complex, vec2))

        if isinstance(value, (int, float, complex)):
            return Vec2(*(e/value for e in self))

        return Vec2(self.x/value.x, self.y/value.y)

    def __add__(self,value):
        assert isinstance(value, (int, float, complex, vec2))

        if isinstance(value, (int, float, complex)):
            return Vec2(*(e+value for e in self))

        return Vec2(self.x+value.x, self.y+value.y)

    def __sub__(self,value):
        assert isinstance(value, (int, float, complex, vec2))

        if isinstance(value, (int, float, complex)):
            return Vec2(*(e-value for e in self))

        return Vec2(self.x-value.x, self.y-value.y)

    def __neg__(self):
        return Vec2(-1*self.x, -1*self.y)

    def __getitem__(self,index):
        return self.pos[index]

    def __setitem__(self,index,value):
        self.pos[index]=value
        reload()

    def __eq__(self,other_vec):
        return self.pos==other_vec.pos

    def __round__(self):
        return Vec2(round(self.x), round(self.y))
