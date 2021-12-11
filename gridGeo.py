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
                diff = [abs(x-start_coords[0]),abs(y-start_coords[1])]
                dist = (diff[0]*diff[0] + diff[1]*diff[1])**.5
                if dist<=rad:
                    outGrid[dex].append(x)
        # filePrint(outGrid)
        o=[]
        for x in range(len(outGrid)):
            t = [outGrid[x][0],outGrid[x][-1]]
            if len(outGrid[x])==1:
                del t[1]
            o+=[[t[i],start_coords[1]+x-rad] for i in range(len(t))]
        outGrid=o
        # filePrint(outGrid)
    else:
        for y in range(start_coords[1]-rad,start_coords[1]+rad+1):
            for x in range(start_coords[0]-rad,start_coords[0]+rad+1):
                diff = [abs(x-start_coords[0]),abs(y-start_coords[1])]
                dist = (diff[0]*diff[0] + diff[1]*diff[1])**.5
                if dist<=rad:
                    outGrid.append([x,y])

    return outGrid


def inCircle(radius,start_coords,point):
    if not square[abs(point[0]-start_coords[0])]+square[abs(point[1]-start_coords[1])]>square[abs(radius)+1]:
        return True
    return False

def lineGrid(septs):
    assert len(septs[0])==len(septs[1])==2

    diffs = [septs[1][0]-septs[0][0],septs[1][1]-septs[0][1]]
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

def rayCast(septs,grid,checkFunc,method="check",dist=-1):
    assert len(septs[0])==len(septs[1])==2
    assert dist>0 or dist==-1

    diffs = [septs[1][0]-septs[0][0],septs[1][1]-septs[0][1]]
    steps = max(abs(diffs[0]),abs(diffs[1]))
    if not steps>0:
        return []
    step = [diffs[0]/steps,diffs[1]/steps]

    cd=0
    mulch=0
    if dist!=-1:
        cd=(diffs[0]*diffs[0],diffs[1]*diffs[1])**.5
        mulch=dist/cd
        steps=round(steps*mulch)#what is happening here?

    last=septs[0]
    lcheck=[]
    points=[]

    filePrint("raycast vars: septs {} diffs {} steps {} step {} method \"{}\" dist {}".format(septs,diffs,steps,step,method,dist))

    for x in range(steps):
        last=[last[0]+step[0],last[1]+step[1]]
        check=[round(last[0]),round(last[1])]
        if check!=lcheck:
            filePrint([last,check,grid[check[1]][check[0]]])
            if steps==0 or not (-1<check[0]<len(grid[0]) and -1<check[1]<len(grid)):
                break
            chk=checkFunc(grid[check[1]][check[0]])
            if chk:
                points.append(check)
            elif not chk:
                break
            lcheck=mapl(check)
        steps-=1
    # filePrint(["rayCast points: ",points])
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

def rayCircle(startPos,radius,grid,checkFunc,method="check"):#but what about S Q U A R E?
    points=[]
    # filePrint("startPos {} radius {} method {}".format(startPos,radius,method))
    borders=circleGrid(radius,start_coords=startPos,bordersOnly=True)
    # filePrint(["borders:",borders])
    for end in borders:
        pts = rayCast([startPos,end],grid,checkFunc=checkFunc,method=method)
        # filePrint(["pts: ", pts])
        points+=pts
    # filePrint(points)
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
            return self.parent.getPath(prev)
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

def tryPathFind(steps,canGoFunc,grid,startPos,endPos):
    assert steps>0
    root=PathTree(pos=(startPos[0],startPos[1]),name="root")
    # paf=explore(fp.children[0],steps,grid,endPos,canGoFunc)
    queue=explore_step(root,grid,canGoFunc)
    nq=[]
    while steps>0:
        filePrint(["steps:",steps,"queue:",[i.pos for i in queue]])
        for c in queue:
            if c.pos==endPos:
                f=c.getPath()
                out=[]
                for i in range(len(f)):
                    out.append(f[-1-i])
                filePrint(out)
                return out
            else:
                nq+=explore_step(c,grid,canGoFunc)
        steps-=1
        queue=mapl(nq)
        nq=[]
    return False

    filePrint(["paf: ",paf])

def explore_step(curr,grid,canGoFunc):
    ps = list(curr.pos)
    poss=[[ps[0]+i[0],ps[1]+i[1]] for i in [[-1,0],[1,0],[0,1],[0,-1]]]
    for p in poss:
        if (curr.parent==None or p!=curr.parent.pos) and (-1<p[0]<len(grid[0]) and -1<p[1]<len(grid)) and canGoFunc(grid[p[1]][p[0]]):
            curr.addChild(pos=(p[0],p[1]))
    return curr.children
