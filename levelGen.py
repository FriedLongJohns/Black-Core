from helpers import *
from levelUnits import *
from gridClasses import *
from random import randint
from gridGeo import dist

def genBoard(x,y,defCell=".",wallCell="x",empty=.1):
    x_size=x*7
    y_size=y*7
    grid=[[defCell for i in range(x_size)] for i in range(y_size)]
    def push_gunit(gunit,xo,yo):
        for y in range(len(gunit)):
            for x in range(len(gunit[0])):
                cell = gunit[y][x]
                if cell=="x":
                    if cell!=wallCell:
                        cell=wallCell
                    grid[y+yo][x+xo]=cell

    for rx in range(0,x):
        for ry in range(0,y):
            gunit = GUNITS[randint(0,len(GUNITS)-1)]#get random grid peice
            if randint(1,100)/100>empty:#chance of empty to not spawn
                push_gunit(gunit,rx*7,ry*7)

    for row in range(len(grid)):
        if row==0 or row==len(grid)-1:
            for i in range(len(grid[row])):
                grid[row][i]=wallCell
        else:
            grid[row][0]=wallCell
            grid[row][-1]=wallCell
    return grid

def spawnEnemies(crang,amount,canSpawnFunc,grid,minPlayerDist=-1,playerPos=[0,0],bad=[]):
    spawned=[]
    for i in range(amount):
        pos=[randint(crang[0][i],crang[1][i]) for i in range(2)]
        while (not canSpawnFunc(pos[0],pos[1])) or dist(pos,playerPos)<minPlayerDist or pos in bad:
            pos=[randint(crang[0][i],crang[1][i]) for i in range(2)]
        spawned.append(Unit(pos,randFrameName(),[randWeaponName(),randWeaponName()],randArmorName(),displayChar="*",kind="enemy"))
    return spawned

#spawnAllies
def spawnAllies(crang,amount,canSpawnFunc,grid,maxPlayerDist=99999,playerPos=[0,0],bad=[]):
    spawned=[]
    for i in range(amount):
        pos=[randint(crang[0][i],crang[1][i]) for i in range(2)]
        while (not canSpawnFunc(pos[0],pos[1])) or (dist(pos,playerPos)>maxPlayerDist) or (pos in bad):
            pos=[randint(crang[0][i],crang[1][i]) for i in range(2)]
        spawned.append(Unit(pos,randFrameName(),[randWeaponName(),randWeaponName()],randArmorName(),displayChar="+",kind="ally"))
    return spawned

def get_free_loc(crang,grid,canSpawnFunc,bad=[],playerPos=[0,0],dist_range=[-1,99999]):
    loc=[randint(crang[0][i],crang[1][i]) for i in range(2)]
    while (not canSpawnFunc(loc[0],loc[1])) or loc in bad or (not dist_range[0]<dist(loc,playerPos)<dist_range[1]):
        loc=[randint(crang[0][i],crang[1][i]) for i in range(2)]
    return loc
