# from gridHelpers import *
from equipment import *
import re
gridJects = []
# dex = [re.compile("\{name\}"),re.compile("\{pos\}"),re.compile("\{kind\}"),re.compile("\{health\}")]

class ClassCell:
    def __init__(self,coords,kind,health=-1,gridSize=[99999,99999],name=""):
        assert kind in ["terrain","enemy","player","ignoreKind"]
        assert -1<coords[0]<gridSize[0]
        assert -1<coords[1]<gridSize[1]
        self.pos = coords
        self.health = health
        self.kind = kind
        self.name = name
        gridJects.append(self)

    def damage(self,amount):
        self.health-=amount
        mess = ""
        if not self.health>0:
            mess = "{} unit at {} was damaged to {} hp".format(self.kind,str(self.pos),str(self.health))
        else:
            mess = "{} unit at {} was destroyed".format(self.kind,str(self.pos))

        return mess

class Unit:
    def __init__(self,coords,frame,weapons,armor,kind="enemy",gridSize=[99999,99999]):
        assert kind in ["enemy","player","ignoreKind"]
        assert -1<coords[0]<gridSize[0]
        assert -1<coords[1]<gridSize[1]

        assert frame in FRAMES
        assert armor in ARMORS
        assert len(weapons)<3
        for wep in weapons:
            assert wep in WEAPONS

        self.frm = FRAMES[frame]
        self.arm = ARMORS[armor]

        self.health=self.frm["hp"]+self.arm["hp"]
        self.damage_multiplier = self.arm["damage_multiplier"]
        self.act_time = self.frm["act_time"]*self.arm["act_time_multiplier"]
        self.wait_time = self.act_time

        self.wps = [[wep,WEAPONS[wep],WEAPONS[wep]["use_time_speed"]*self.act_time,0] for wep in weapons]

        self.move_max = self.frm["move"]

        self.pos = coords
        self.kind = kind
        self.name = self.kind
        if kind=="enemy":
            self.name+=str(hash(frame+armor+str(coords)))

        gridJects.append(self)

    def move(pos,cursedGrid):
        cursedGrid.cellSwap(self.pos,pos)
        self.pos = pos
        self.wait_time = self.act_time

    def attack(enemy,weapon):
        assert weapon in [i[0] for i in self.wps]
        chosen = 0

        for dex in range(self.wps):
            if self.wps[dex]==weapon:
                chosen=dex

        dam = self.wps[chosen][1]["dam"]*enemy.damage_multiplier#fire
        self.wps[chosen][3] = self.wps[chosen][1]["cooldown"]#cooldown
        self.wait_time = chosen[2]#time

        mess = "{} attacked {} with {}".format(self.kind,enemy.kind,weapon)
        enemy.damage(dam)

        return chosen[2], mess

    def damage(self,amount):
        self.health-=amount
        mess = ""
        if not self.health>0:
            mess = "{} unit at {} was damaged to {} hp".format(self.kind,str(self.pos),str(self.health))
        else:
            mess = "{} unit at {} was destroyed".format(self.kind,str(self.pos))

        return mess
