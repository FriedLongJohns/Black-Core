import time as t
from helpers import *

def circleGrid(radius,start_coords=[0,0],bordersOnly=False):
    assert type(radius)==int and -1<radius<101 #stored squares only go from 0-100
    assert type(start_coords[0]) == int
    assert type(start_coords[1]) == int

    outGrid = []

    rad = abs(radius)+1

    for y in range(start_coords[1]-radius,start_coords[1]+rad+1):
        for x in range(start_coords[0]-radius,start_coords[0]+rad+1):
            if not square[abs(x)]+square[abs(y)]>square[rad]:
                outGrid.append([x,y])

    if bordersOnly:
        for i in range(len(outGrid[1:-1])):
            while len(outGrid[i])>2:
                del outGrid[i][2]

    return outGrid

def inCircle(radius,start_coords,point):
    if not square[abs(point[0]-start_coords[0])]+square[abs(point[1]-start_coords[1])]>square[abs(radius)+1]:
        return True
    return False

def lineGrid(septs,diags=True):
    assert len(septs[0])==len(septs[1])==2

    if septs[0]>septs[1]:
        startpt=septs[1]
        endpt=septs[0]
    else:
        startpt=septs[0]
        endpt=septs[1]

    mult = (endpt[1]-startpt[1])/(endpt[0]-startpt[0])
    intercept = startpt[1]-startpt[0]*mult
    points=[]
    lp=startpt

    for x in range(startpt[0],endpt[0]+1):
        newp = [x,round(x*mult+intercept)]
        if not diags:
            if abs(lp[0]-newp[0])==1:
                points.append([newp[0],lp[1]])
            elif abs(lp[1]-newp[1])==1:
                points.append([newp[0],lp[1]])

        points.append(newp)
        lp=newp

    return points

def inLine(septs,point,diags=True):
    if septs[0]>septs[1]:
        startpt=septs[1]
        endpt=septs[0]
    else:
        startpt=septs[0]
        endpt=septs[1]

    mult = (endpt[1]-startpt[1])/(endpt[0]-startpt[0])
    intercept = startpt[1]-startpt[0]*mult
    lp=[point[0]-1,round((point[0]-1)*mult+intercept)]

    for x in range(point[0]-1,point[0]+1):
        newp = [x,round(x*mult+intercept)]
        if point==newp:
            return True
        elif not diags and (abs(lp[0]-newp[0])==1 or abs(lp[1]-newp[1])==1) and point==[newp[0],lp[1]]:
            return True
        lp=newp

    return False

def rayCast(septs,grid,checkFunc,method="stop",diags=True,dist=1000):
    assert len(septs[0])==len(septs[1])==2

    if septs[0]>septs[1]:
        startpt=septs[1]
        endpt=septs[0]
    else:
        startpt=septs[0]
        endpt=septs[1]

    mult = (endpt[1]-startpt[1])/(endpt[0]-startpt[0])
    intercept = startpt[1]-startpt[0]*mult
    lp=startpt
    check=[]
    distLeft=dist

    for x in range(startpt[0],endpt[0]+1):
        check = [x,round(x*mult+intercept)]
        if not diags:
            if abs(lp[0]-newp[0])==1:
                check=[newp[0],lp[1]]
            elif abs(lp[1]-newp[1])==1:
                check=[newp[0],lp[1]]
        if distLeft==0 or not (-1<check[0]<len(grid[0]) and -1<check[1]<len(grid)):
            break
        elif checkFunc(grid[check[1]][check[0]]):
            if method=="stop":
                return check
            elif method=="check":
                return check
        lp=newp
        distLeft-=1

    return points

def pathGrid(steps,canGoFunc,grid,startPos):
    options=[[startPos[0],startPos[1],steps]]#[x,y,steps left]
    moves=[]#all x,y that you can movde to in <steps> steps
    dupe = grid

    while len(options)!=0:
        curr = options[0]

        if curr[2]>0:

            checks = [[curr[0]+i[0],curr[1]+i[1],curr[2]-1] for i in [[-1,0],[0,1],[1,0],[0,-1]]]

            for chk in checks:
                if not (-1<chk[0]<len(dupe[0]) and -1<chk[1]<len(dupe)):
                    continue

                cell = dupe[chk[1]][chk[0]]
                if not chk[:-1] in moves and canGoFunc(cell):
                    moves.append(chk[:-1])
                    options.append(chk)

        del options[0]

    return moves

def rayCircle(startPos,grid,radius,checkFunc,method="stop",diags=True):
    points=[]

    for end in circleGrid(radius,start_coords=startPos,bordersOnly=True):
        points+=rayCast([startPos,end],checkFunc=checkFunc,diags=diags,method=method)

    return points

def tryPathFind(steps,canGoFunc,grid,startPos,endPos):#horribly slow, DEFINETLY can be optimized.
    poss = pathGrid(steps,canGoFunc,grid,startPos)
    least=999999
    ls=startPos
    for pos in poss:
        if dist(endPos,pos) < least:
            least = dist(endPos,pos)
            ls=pos
    return ls

def dist(pos1,pos2):
    return sqrt(square[abs(pos1[0]-pos2[0])],square[abs(pos1[1]-pos2[1])])

# no actual pathfinding, too lazy (also VERY fancy - path joining(dual-loop), path storage, direction selection(quad-logic) + actual pathfinding spread code (dual-loop) + best selection (loop))




# if __name__ == "__main__":
