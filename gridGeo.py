import time as t
from helpers import *

def dist(pos1,pos2):
    return sqrt(square[abs(pos1[0]-pos2[0])],square[abs(pos1[1]-pos2[1])])

def circleGrid(radius,start_coords=[0,0],bordersOnly=False):
    assert type(radius)==int and -1<radius<101 #stored squares only go from 0-100
    assert type(start_coords[0]) == int
    assert type(start_coords[1]) == int

    outGrid = []

    rad = abs(radius)

    if bordersOnly:
        dex=-1
        for y in range(start_coords[1]-rad,start_coords[1]+rad+1):
            outGrid.append([])
            dex+=1
            for x in range(start_coords[0]-radius,start_coords[0]+rad+1):
                if not square[abs(x)]+square[abs(y)]>square[rad]:
                    outGrid[dex].append(x)

        o=[]
        for i in range(len(outGrid)):
            while len(outGrid[i])>2:
                del outGrid[i][1]
            o+=[[outGrid[i][x],start_coords[1]+i] for x in range(len(outGrid[i]))]
        outGrid=o
    else:
        for y in range(start_coords[1]-radius,start_coords[1]+rad+1):
            for x in range(start_coords[0]-radius,start_coords[0]+rad+1):
                if not square[abs(x)]+square[abs(y)]>square[rad]:
                    outGrid.append([x,y])

    return outGrid


def inCircle(radius,start_coords,point):
    if not square[abs(point[0]-start_coords[0])]+square[abs(point[1]-start_coords[1])]>square[abs(radius)+1]:
        return True
    return False

def lineGrid(septs):
    assert len(septs[0])==len(septs[1])==2

    diffs = [septs[1][1]-septs[0][1],septs[1][0]-septs[0][0]]
    steps = max(diffs[0],diffs[1])
    if steps<1:
        return False
    step = [diffs[0]/steps,diffs[1]/steps]
    last=septs[0]
    points=[]

    for x in range(steps):
        last=[last[0]+step[0],last[1]+step[1]]
        check=[round(last[0]),round(last[1])]
        points.append(check)

    return points

def inLine(septs,point):
    assert len(septs[0])==len(septs[1])==2

    diffs = [septs[1][1]-septs[0][1],septs[1][0]-septs[0][0]]
    steps = max(diffs[0],diffs[1])
    if steps<1:
        return False
    step = [diffs[0]/steps,diffs[1]/steps]
    last=septs[0]
    points=[]

    for x in range(steps):
        last=[last[0]+step[0],last[1]+step[1]]
        check=[round(last[0]),round(last[1])]
        if point==check:
            return True

    return False

def rayCast(septs,grid,checkFunc,method="stop",dist=-1):
    assert len(septs[0])==len(septs[1])==2
    assert dist>0 or dist==-1

    diffs = [septs[1][1]-septs[0][1],septs[1][0]-septs[0][0]]
    steps = max(diffs[0],diffs[1])
    if not steps>0:
        return []
    step = [diffs[0]/steps,diffs[1]/steps]
    if dist!=-1:
        steps=dist
    last=septs[0]
    points=[]


    for x in range(steps):
        last=[last[0]+step[0],last[1]+step[1]]
        check=[round(last[0]),round(last[1])]
        if steps==0 or not (-1<check[0]<len(grid[0]) and -1<check[1]<len(grid)):
            break
        chk=checkFunc(grid[check[1]][check[0]])
        if chk:
            points.append(check)
        elif not chk:
            break

        steps-=1
    filePrint(points)
    if method=="stop":
        return points[-1]
    else:
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

def rayCircle(startPos,radius,grid,checkFunc,method="check"):
    points=[]
    borders=circleGrid(radius,start_coords=startPos,bordersOnly=True)
    for end in borders:
        points+=rayCast([startPos,end],grid,checkFunc=checkFunc,method=method)
    filePrint(borders)
    filePrint(points)
    return points

class PathTree:
    def __init__(self,pos=(0,0),children=[],parent=None,name="anon"):
        self.parent=parent
        self.pos=pos
        self.children=children
        self.name=name

    def __str__(self):
        return "<PathTree instance \"{}\">".format(self.name)

    def getTree2Q(self, acc = [], rest = []):
        if not rest:
            rest = self.children
            print(self, rest, self.children)
            acc.append(rest[0])
            return self.getTree2Q(acc, rest[1:])
        else:
            acc.append(self)
            return acc

    def getTree(self):
        print("self: ",self)
        tree=[self,[]]
        if self.children:
            print("children!")
            for child in self.children:
                print("child: ",child)
                tree[1].append(child.getTree())
        return tree

    def addChild(self,pos=(0,0),children=[],name="anon"):
        child=PathTree(pos=pos,children=mapl(children),parent=self,name=name)
        self.children.append(child)
        return child

    def getPath(self,prev=[]):
        prev.append(self.pos)
        if self.parent:
            return getPath(self.parent,prev)
        else:
            return prev

    def funcPath(self,func,prev=[]):
        prev.append(func(self))
        if self.parent:
            return funcPath(func=func,prev=prev)
        else:
            return prev

    def funcTips(self,func):
        results=[]
        if self.children==[]:
            return [func(self)]
        else:
            for child in self.children:
                if child.children!=[]:
                    results+=funcTips(child,func=func)
                else:
                    results.append(func(child))
            return results

    def getChildAt(self,path):
        if path==[]:
            return self
        return self.children[path[0]].getChildAt(path[1:])

    def tryPathFind(steps,canGoFunc,grid,startPos,endPos):#horribly slow, DEFINETLY can be optimized.
        poss = pathGrid(steps,canGoFunc,grid,startPos)
        least=999999
        ls=startPos
        for pos in poss:
            if dist(endPos,pos) < least:
                least = dist(endPos,pos)
                ls=pos
        return ls
