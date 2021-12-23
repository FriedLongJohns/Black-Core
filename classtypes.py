# from math import cos,sin
# import numpy as np

class vec2():
    def __init__(self,x,y):
        self.pos=[x,y]
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
        return self/self.dist

    def normalize(self):
        self.pos[0]/=self.dist
        self.pos[1]/=self.dist
        self.dist=1

    def copy(self):
        return vec2(self.pos[0],self.pos[1])

    def __str__(self):
        return "vec2({},{})".format(self.pos[0],self.pos[1])



    def __mul__(self, value):
        assert isinstance(value, (int, float, complex, vec2,list,tuple))

        if isinstance(value, (int, float, complex)):
            return vec2(*(e*value for e in self))

        return vec2(self.x*value[0], self.y*value[1])

    def __truediv__(self, value):
        assert isinstance(value, (int, float, complex, vec2,list,tuple))

        if isinstance(value, (int, float, complex)):
            return vec2(*(e/value for e in self))

        return vec2(self.x/value[0], self.y/value[1])

    def __add__(self,value):
        assert isinstance(value, (int, float, complex, vec2,list,tuple))

        if isinstance(value, (int, float, complex)):
            return vec2(*(e+value for e in self))

        return vec2(self.x+value[0], self.y+value[1])

    def __sub__(self,value):
        assert isinstance(value, (int, float, complex, vec2,list,tuple))

        if isinstance(value, (int, float, complex)):
            return vec2(*(e-value for e in self))

        return vec2(self.x-value[0], self.y-value[1])

    def __neg__(self):
        return vec2(-1*self.x, -1*self.y)

    def __getitem__(self,index):
        return self.pos[index]

    def __setitem__(self,index,value):
        self.pos[index]=value
        reload()

    def __eq__(self,value):
        assert isinstance(value, (vec2,list,tuple))
        return self.pos[0]==value[0] and self.pos[1]==value[1]

    def __round__(self):
        return vec2(round(self.x), round(self.y))

class polydict:
    def __init__(self,axii=["key","value"],data=[]):#data = [{"key": 5,"value": 10}] and use non-axii for non-access ones
        self.stored = {hash(str(d)):d for d in data}
        self.refs = {axis:{str(data[i][axis]):hash(str(data[i])) for i in range(len(data))} for axis in axii}
        #speed var
        self.len = len(self.stored)

    def __len__(self):
        return self.len

    def __str__(self):
        return "axii: "+str([i for i in self.refs.keys()])+"\n"+"\n".join(["poly ID "+str(i[0])+": "+str(i[1]) for i in self.stored.items()])

    def criteriaID(self,criteria):
        for id,data in self.stored.items():
            keys = [i for i in data.keys()]

            i=0

            for s in range(len(keys)):#clean out non-criteria checks
                if not keys[i] in [i for i in criteria.keys()]:
                    del keys[i]
                    i-=1
                i+=1
            i=0

            if len(keys)!=0:
                continue

            for s in range(len(keys)):
                if not data[keys[i]]==criteria[keys[i]]:#make sure each check is true, if yes return it
                    break
                i+=1
            if i==len(criteria)-1:
                return id

        return 0.1#hashes don't return decimals

    def set(self, set, criteria={}):#turns into add element by default
        if criteria!={}:
            id = self.criteriaID(criteria)
            if id!=0.1:
                for k,v in set.items():
                    self.stored[id][k] = v
                return

        for axis in set.keys():
            if axis in self.refs.keys():
                self.refs[axis][str(set[axis])]=len(self.stored)

        self.stored[hash(str(set))]=set
        self.len = len(self.stored)


    def get(self, criteria):
        assert type(criteria)==dict
        id = self.criteriaID(criteria)
        if id==.1:
            raise KeyError("Could not find poly with criteria "+str(criteria))
        return self.stored[id]

    def rem(self,criteria):
        id = self.criteriaID(criteria)
        if id!=.1:
            del self.stored[id]
            for axis in self.refs.keys():
                if id in self.refs[axis].values() and axis in criteria.keys():
                    del self.refs[axis][str(criteria[axis])]
            self.len = len(self.stored)