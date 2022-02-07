from random import randint
from helpers import *
from equipment import *
from gridGeo import pathGrid,dist,rayCast
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
            self.aimode=["dam","assault","kite","angry"][randint(0,3)]

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
                "LOS": enemy.pos in rayCast([pos,enemy.pos],grid,fireFunc,method="line"),
            }
            out.append(block)
        return out

    def think(self,enemy,fireFunc,moveFunc,grid,mode="self"):
        md=mode
        if mode=="self":
            md=self.aimode
        else:
            assert mode in ["dam","assault","kite","angry"]
        #dam : gets to the range where it has more potential damage compared to the enemy, attempting to kite if possible
        #assault : gets to the average between it's two weapon ranges to the enemy
        #   and running away when fully on cooldown.
        #kite : stays at max range, prioritising moving over firing
        #angry : pathfinds to the player and then fires until it can't. no retreating.
        sr = [self.wps[0][1]["range"],self.wps[1][1]["range"]]
        sd = [self.wps[0][1]["damage"],self.wps[1][1]["damage"]]
        er = [enemy.wps[0][1]["range"],enemy.wps[1][1]["range"]]
        ed = [enemy.wps[0][1]["damage"],enemy.wps[1][1]["damage"]]
        optimal_range=0
        chosen=0
        checks=[False,False,False,False,False]

        if sr[0]>er[0]:
            checks[0]=True#our first weapon has more range than enemy
        if sr[1]>er[1]:
            checks[1]=True#our second weapon has more range than enemy
        if sd[0]>ed[0]:
            checks[2]=True#our first weapon has more damage than enemy
        if sd[1]>ed[1]:
            checks[3]=True#our second weapon has more  damage than enemy
        if sd[1]>sd[0]:
            checks[4]=True#our first weapon has more range

        if mode=="angry":
            optimal_range=2
        elif mode=="kite":
            optimal_range=max(self.wps[0][1]["range"],self.wps[1][1]["range"])
        else:#dam and assault have dynamic ranges
            if checks[0]:#more range in weapon 1 orand and in weapon 2
                optimal_range=sr[0]
                if checks[4] and checks[1]:
                    optimal_range=sr[1]
            elif checks[1]:#more range in weapon 2
                optimal_range=sr[1]

            elif checks[2]:#pure damage face-off
                optimal_range=sr[0]
                if checks[4] and checks[3]:
                    optimal_range=sr[1]
            elif checks[3]:
                optimal_range=sr[1]

            #if we will be vulnerable, stay out of their range!
            if (self.wps[0][3]>0 and self.wps[0][3]>0 and (self.wps[0][3]-self.act_time>0 or self.wps[1][3]-self.act_time>0)):
                optimal_range=max(enemy.wps[0][1]["range"],enemy.wps[1][1]["range"])+1
                chosen=1

        moves = pathGrid(self.move_max,moveFunc,grid,self.pos)
        posbs = self.evalPositions(enemy,moves,fireFunc,grid)
        bests = [self.pos,self.pos]#attack,retreat
        beste = [dist(self.pos,enemy.pos),dist(self.pos,enemy.pos)]
        los=[False,False]
        for pos in posbs:
            error = absol(dist(pos["pos"],enemy.pos)-optimal_range)
            for i in [0,1]:
                bl=bool(i)
                do=False
                if (not bl)==pos["LOS"]:#los, not los
                    #attack
                    if cond==los[i]:
                        los[i]=(not bl)
                        do=True
                    elif error<beste[i]:#and we already have los position possibility
                        do=True

                elif bl==los[i] and error<beste[i]:#not los and not found, los and found (and more optimal position)
                    do=True

                if do:
                    beste[i]=error
                    bests[i]=pos["pos"]

        best=bests[chosen]
        if (mode!="kite" or self.pos==best) and los and max(self.wps[0][1]["range"],self.wps[1][1]["range"])>=dist(self.pos,enemy.pos) and min(self.wps[0][3],self.wps[1][3])<=0:
            #if we can fire, do it (unless kiting and not at best pos)
            if not self.wps[0][3]>0:
                if not self.wps[1][3]>0 and checks[4] and self.wps[0][1]["range"]>=dist(self.pos,enemy.pos):
                    return ["fire",0]
                elif self.wps[0][1]["range"]>=dist(self.pos,enemy.pos):#if not in range, wait
                    return ["fire",1]
            elif not self.wps[1][3]>0 and self.wps[1][1]["range"]>=dist(self.pos,enemy.pos):
                return ["fire",1]
            return ["wait"]#wait .1 time, basically until it needs (or can) do something
        else:
            return ["move",best]
