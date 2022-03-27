from random import randint
from helpers import *
from equipment import *
from gridGeo import pathGrid,dist,rayCast,tryPathFind
import re
from classtypes import vec2,inf
# dex = [re.compile("\{name\}"),re.compile("\{pos\}"),re.compile("\{kind\}"),re.compile("\{health\}")]

class ClassCell:
    def __init__(self,coords,kind,health=-1,name="",displayChar="?"):
        self.pos = vec2(coords[0],coords[1])
        self.health = health
        self.kind = kind
        self.name = name
        self.displayChar=displayChar

    def damage(self,amount,enemy):
        self.health-=amount
        mess = "{} unit was damaged to {} hp by {}".format(self.name,self.health,enemy.name)
        return mess

class Unit:
    def __init__(self,coords,frame,weapons,armor,kind="enemy",displayChar="o",displayColor=0,aimode="rand"):

        assert frame in FRAMES.keys()
        assert armor in ARMORS.keys()
        assert len(weapons)<3
        for wep in weapons:
            assert wep in WEAPONS.keys()

        self.frm = FRAMES[frame]
        self.arm = ARMORS[armor]

        self.health=self.frm["hp"]+self.arm["hp"]
        self.damage_multiplier = self.arm["damage_multiplier"]
        self.act_time = self.frm["act_time"]*self.arm["act_time_multiplier"]
        self.wait_time = self.act_time

        self.wps = [[name,WEAPONS[name],WEAPONS[name]["use_time_speed"]*self.act_time,0] for name in weapons]
        self.move_max = self.frm["move"]

        self.pos = vec2(coords[0],coords[1])
        self.kind = kind
        self.name = self.kind
        self.displayChar=displayChar
        self.displayColor=displayColor

        self.id=hash(frame+armor+str(coords))

        if kind in ["enemy","ally"]:
            self.name+="_"+forcefit(self.id,4,pos="r")

        self.aimode = aimode
        if aimode=="rand":
            self.aimode=["assault","kite","angry"][randint(0,2)]

    # def aiDynamicMove(player=None)
    def __equals__(self,other):
        if self.id==other.id:
            return True
        return False

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

    def damage(self,amount,enemy):
        self.health-=amount
        mess = "{} unit was damaged to {} hp by {}".format(self.name,self.health,enemy.name)
        return mess

    def get_enemy(self,units):
        poss=[]
        checks=(self.kind=="ally",self.kind=="enemy")
        for unit in units:
            if (checks[0] and unit.kind=="enemy") or (checks[1] and unit.kind!=self.kind):
                poss.append([unit,dist(self.pos,unit.pos)*unit.health/self.health])
        min=inf()
        selected=None
        for p in poss:
            if p[1]<min:
                selected=p[0]
                min=p[1]
        return selected

    def evalPositions(self,enemy,checks,fireFunc,grid):
        out=[]
        for pos in checks:
            dis = dist(pos,enemy.pos)

            block={
                "pos": pos.copy(),
                "dist": dis,
                "los": enemy.pos in rayCast([pos,enemy.pos],grid,fireFunc,method="line"),
            }
            out.append(block)
        return out

    def think(self,enemy,fireFunc,moveFunc,grid,mode="self"):
        md=mode
        if mode=="self":
            md=self.aimode
        else:
            assert mode in ["assault","kite","angry"]
        #assault : goto most possible weapon damage range or run away
        #kite : stay at max range, prioritize moving over firing
        #angry : pathfinds to the player and then fires or waits. no retreating.


        optimal_range=0
        sr=[self.wps[0][1]["range"],self.wps[1][1]["range"]]
        cf=[self.wps[0][3]<=0,self.wps[1][3]<=0]

        cf_dam = [-1,0]
        cf_range = [-1,0]
        for i in cf:
            if i==True:
                if self.wps[cf_dam[0]][1]["damage"]<self.wps[i][1]["damage"] and self.wps[i][3]<=0:
                    cf_dam = [i,self.wps[i][1]["damage"]]
                if self.wps[cf_range[0]][1]["range"]<self.wps[i][1]["range"] and self.wps[i][3]<=0:
                    cf_range = [i,self.wps[i][1]["range"]]

        ecf=[enemy.wps[0][3]<=0,enemy.wps[1][3]<=0]
        ecf_dam = 0
        ecf_range = 0
        for i in cf:
            if i==True:
                ecf_dam = max(ecf_dam,self.wps[i][1]["damage"])
                ecf_range = max(ecf_range,self.wps[i][1]["range"])


        chosen=0
        if mode=="angry":
            optimal_range=0

        #if not anrgy, not able to fire, and either not kiting or out of enemy range if kiting, retreat
        elif cf_dam==-1 and (mode!="kite" or dist(self.pos,enemy.pos)<ecf_range):
                optimal_range=inf()
                chosen=1

        elif mode=="kite":
            optimal_range=self.wps[cf_range[0]][1]["range"]-.5#stay just in range

        else:#assault
            optimal_range = self.wps[cf_dam[0]][1]["range"]-.5

        moves = pathGrid(self.move_max,moveFunc,grid,self.pos)
        posbs = self.evalPositions(enemy,moves,fireFunc,grid)
        bests = [self.pos,self.pos]#attack,retreat
        beste = [inf(),inf()]
        los=[enemy.pos in rayCast([self.pos,enemy.pos],grid,fireFunc,method="line") for i in range(2)]

        for pos in posbs:
            error = absol(dist(pos["pos"],enemy.pos)-optimal_range)

            if pos["los"]:
                if not los[0]:
                    los[0]=True
                if error<beste[0]:
                    beste[0]=error
                    bests[0]=pos["pos"]

                if los[1] and error<beste[1]:
                    beste[1]=error
                    bests[1]=pos["pos"]

            else:
                if los[1]:
                    los[1]=False
                if error<beste[1]:
                    beste[1]=error
                    bests[1]=pos["pos"]

        best=bests[chosen]


        if (chosen==0 and los[0]==False):#can't move into LOS, plan ahead to touch them (too lazy for smart planning)
            path=tryPathFind(100,moveFunc,grid,self.pos)
            return ["move",path[self.move_max-1]]

        elif (chosen==1 and los[1]==True):#do the same for escaping
            point=vec2(0,0)
            for p in lineGrid(self.pos,self.pos+5*(self.pos-enemy.pos)):
                if moveFunc(p[0],p[1]):
                    path=tryPathFind(100,moveFunc,grid,p)
                    return ["move",path[self.move_max-1]]
            return ["wait"]

        has_los=enemy.pos in rayCast([pos["pos"],enemy.pos],grid,fireFunc,method="line")
        diste=dist(self.pos,enemy.pos)

        # if mode=="kite":
        #     if -1<dist(self.pos,enemy.pos)-optimal_range<1 and has_los:
        #         return ["fire",cf_dam[0]]
        #     else:
        #         return ["move",best]
        # elif mode=="assault":
        #     if has_los and cf_dam[0]!=-1 and self.wps[cf_dam[0]][1]["range"]<=dist(self.pos,enemy.pos):
        #         return ["fire",cf_dam[0]]
        #     else:
        #         return ["move",best]
        # else:
        #     if has_los and cf_dam[0]!=-1 and self.wps[cf_dam[0]][1]["range"]<=dist(self.pos,enemy.pos):
        #         return ["fire",cf_dam[0]]
        #     else:
        #         return ["wait"]

        #compression
        if has_los:
            if mode=="kite" and -1<dist(self.pos,enemy.pos)-optimal_range<1:
                if self.wps[cf_range[0]][1]["range"]<=dist(self.pos,enemy.pos):
                    return ["fire",cf_range[0]]
                else:
                    return ["wait"]
            elif cf_dam[0]!=-1 and self.wps[cf_dam[0]][1]["range"]<=dist(self.pos,enemy.pos):
                return ["fire",cf_dam[0]]
        else:
            if mode=="angry":
                return ["wait"]
            else:
                return ["move", best]
