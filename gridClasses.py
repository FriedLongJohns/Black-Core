from random import randint
from helpers import *
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
            self.aimode=["dam","assault","kite","angry"][random.randint(0,3)]

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

    def think(self,enemy,fireFunc,moveFunc,grid,mode="self"):
        md=mode
        if mode=="self":
            md=self.aimode
        else:
            assert mode in ["dam","assault","kite","angry"]
        #dam : gets to the range where it has more potential damage compared to the enemy, attempting to kite if possible - prioritisies position over firing
        #assault : gets to the average between it's two weapon ranges to the enemy, prioritizing firing over moving,
        #   and running away when fully on cooldown.
        #kite : stays at max range, prioritising moving over firing
        #angry : pathfinds to the player and then fires until it can't. no retreating.
        sr = [self.wps[0][1]["range"],self.wps[1][1]["range"]]
        sd = [self.wps[0][1]["damage"],self.wps[1][1]["damage"]]
        er = [enemy.wps[0][1]["range"],enemy.wps[1][1]["range"]]
        ed = [enemy.wps[0][1]["damage"],enemy.wps[1][1]["damage"]]
        optimal_range=0
        checks=[False,False,False,False,False]

        if sr[0]>er[0]:
            checks[0]=True
        if sr[1]>er[1]:
            checks[1]=True
        if sd[0]>ed[0]:
            checks[2]=True
        if sd[1]>ed[1]:
            checks[3]=True
        if sd[1]>sd[0]:
            checks[4]=True

        if mode=="angry":
            optimal_range=1
        elif mode=="kite"
            optimal_range=max(enemy.wps[0][1]["range"],enemy.wps[1][1]["range"])
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
            if (self.wps[0][3]>0 and self.wps[0][3]>0):
                optimal_range=max(enemy.wps[0][1]["range"],enemy.wps[1][1]["range"])+1

        moves = pathGrid(self.move_max,moveFunc,grid,self.pos)
        posbs = evalPositions(enemy,moves,fireFunc,grid)
        best = self.pos
        beste = dist(self.pos,enemy.pos)
        los=False
        for pos in posbs:
            error = absol(dist(pos,enemy.pos)-optimal_range)
            if pos["LOS"]:
                if not los:
                    los=True
                    beste=error
                    best=pos
                if error<beste:#and we already have los position possibility
                    beste=error
                    best=pos
            elif not los and error<beste:
                beste=error
                best=pos

        if best==self.pos or (mode=="angry" and max(enemy.wps[0][1]["range"],enemy.wps[1][1]["range"])>=dist(self.pos,enemy.pos) and raycast([pos,enemy.pos],grid,fireFunc,method="end")==enemy.pos):
            #either if we don't have to move or we're [angry, in range, and in LOS of enemy]
            if not self.wps[0][3]>0:
                if not self.wps[1][3]>0 and checks[4]:
                    return ["fire",0]
                elif not self.wps[0][1]["range"]<dist(self.pos,enemy.pos):#if not in range, wait
                    return ["fire",1]
            elif not self.wps[1][3]>0 and  not self.wps[1][1]["range"]<dist(self.pos,enemy.pos):
                return ["fire",1]
            return ["wait"]#wait .1 time, basically until it needs (or can) do something
        else:
            return ["move",best]
