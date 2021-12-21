from random import randint
from equipment import *
import re
gridJects = []
# dex = [re.compile("\{name\}"),re.compile("\{pos\}"),re.compile("\{kind\}"),re.compile("\{health\}")]

class ClassCell:
    def __init__(self,coords,kind,health=-1,name="",displayChar="?"):
        assert kind in ["terrain","enemy","player","ignoreKind"]
        self.pos = coords
        self.health = health
        self.kind = kind
        self.name = name
        self.displayChar=displayChar
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
    def __init__(self,coords,frame,weapons,armor,kind="enemy",displayChar="o",aimode="rand"):
        assert kind in ["enemy","player","ignoreKind"]

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

        self.wps = [[name,WEAPONS[name],WEAPONS[name]["use_time_speed"]*self.act_time,0] for name in weapons]

        self.move_max = self.frm["move"]

        self.pos = coords
        self.kind = kind
        self.name = self.kind
        self.displayChar=displayChar

        if kind=="enemy":
            self.name+=str(hash(frame+armor+str(coords)))[2:]

        self.aimode = aimode
        if aimode=="rand":
            self.aimode=["d/h","assault","kite","angry"][random.randint(0,3)]

        gridJects.append(self)

    # def aiDynamicMove(player=None)

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

    def evalPositions(self,enemy,checks,fireFunc,grid):
        out=[]
        for pos in checks:
            dis = dist(pos,enemy.pos)
            block={
                "pos": (pos[0],pos[1]),
                "dist": dis,
                "LOS": raycast([pos,enemy.pos],grid,fireFunc,method="end")==enemy.pos,
                "w1_inrange": dis<self.wps[0][1]["range"],
                "w2_inrange": dis<self.wps[1][1]["range"],
                "w1_canfire": not self.wps[0][3]>self.act_time,
                "w2_canfire": not self.wps[0][3]>self.act_time
            }
            out.append(block)
        return out

    def think(self,mode="self"):
        md=mode
        if mode=="self":
            md=self.aimode
        else:
            assert mode in ["d/h","assault","kite","angry"]
        #d/h : gets to the range where it has more potential damage compared to the enemy
        #assault : gets to the average between it's two weapon ranges to the enemy, prioritizing firing over moving,
        #   and running away when fully on cooldown.
        #kite : stays at max range, prioritising moving over firing
        #angry : pathfinds to the player and then fires until it can't. no retreating.
        if md=="d/h":
