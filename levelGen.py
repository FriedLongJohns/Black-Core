from helpers import *
from levelUnits import *
from gridClasses import *
from random import randint
from gridGeo import dist

def genBoard(x_size,y_size,defCell=".",wallCell="x",empty=.1):
    max_x_units=x_size//7
    max_y_units=y_size//7
    grid=[[defCell for i in range(x_size)] for i in range(y_size)]
    def poosh(unit,xo,yo):
        for y in range(len(unit)):
            for x in range(len(unit[0])):
                cell = unit[y][x]
                if cell=="x":
                    if cell!=wallCell:
                        cell=wallCell
                    grid[y+yo][x+xo]=cell
    for ry in range(max_y_units):
        for rx in range(max_x_units):
            gunit = gunits[randint(0,len(gunits)-1)]
            if randint(1,100)/100>empty:
                poosh(gunit,rx*7,ry*7)

    for row in range(len(grid)):
        if row==0 or row==len(grid)-1:
            for i in range(len(grid[row])):
                grid[row][i]=wallCell
        else:
            grid[row][0]=wallCell
            grid[row][-1]=wallCell
    return grid

def spawnUnits(crang,amount,canSpawnFunc,grid,minPlayerDist=-1,playerPos=[0,0]):
    spawned=[]
    for i in range(amount):
        pos=[randint(crang[0][i],crang[1][i]) for i in range(2)]
        while (not canSpawnFunc(pos[0],pos[1])) or dist(pos,playerPos)<minPlayerDist:
            pos=[randint(crang[0][i],crang[1][i]) for i in range(2)]
        spawned.append(Unit(pos,randFrameName(),[randWeaponName(),randWeaponName()],randArmorName(),displayChar="*"))
    return spawned
