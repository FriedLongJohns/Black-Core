from helpers import *
from classtypes import vec2

def dist(pos1,pos2):
    if pos1==pos2:
        return 0
    else:
        xd = pos1[0]-pos2[0]
        yd = pos1[1]-pos2[1]
        return (square[int((xd*xd)**.5)]+square[int((yd*yd)**.5)])**.5

def rdist(pos1,pos2):
    if pos1==pos2:
        return 0
    else:
        xd = pos1[0]-pos2[0]
        yd = pos1[1]-pos2[1]
        return (xd*xd+yd*yd)**.5

def circleGrid(radius,start_pos=None,bordersOnly=False):
    if not start_pos:
        start_pos=vec2(0,0)
    assert type(radius)==int and -1<radius<101 #stored squares only go from 0-100
    outgrid = []
    rad = abs(radius)

    for y in range(start_pos[1]-rad,start_pos[1]+rad+1):
        for x in range(start_pos[0]-rad,start_pos[0]+rad+1):
            point = vec2(x-start_pos[0],y-start_pos[1])
            if point.dist<=rad:
                outgrid.append(point+start_pos)
    realog=[]
    if bordersOnly:
        for pos in outgrid:
            if -.9<dist(pos,start_pos)-rad<.9:#sqrt(2)/2
                realog.append(pos)
        outgrid=realog
    return outgrid


def inCircle(radius,start_coords,point):
    if not square[abs(point[0]-start_coords[0])]+square[abs(point[1]-start_coords[1])]>square[abs(radius)+1]:
        return True
    return False

def lineGrid(septs):
    assert len(septs)==2

    diffs = vec2(septs[1][0]-septs[0][0],septs[1][1]-septs[0][1])
    steps = round(diffs.dist*2)
    if steps<1:
        return [vec2(septs[0][0],septs[0][1])]
    step = diffs/steps
    loc=vec2(septs[0][0],septs[0][1])
    points=[loc]

    for x in range(steps):
        loc+=step#haha custom class go brrr just add them
        point=round(loc)
        if point!=points[-1]:
            points.append(point)
    return points

def inLine(septs,point):
    assert len(septs)==2

    diffs = vec2(septs[1][0]-septs[0][0],septs[1][1]-septs[0][1])
    steps = round(diffs.dist*2)
    if steps<1:
        return False
    step = diffs/steps
    loc=vec2(septs[0][0],septs[0][1])
    points=[loc]

    for x in range(steps):
        loc+=step
        check=round(loc)
        if point!=points[-1] and point==check:
            return True
    return False

def rayCast(septs,grid,checkFunc,method="line",dist=-1):
    assert dist>0 or dist==-1
    assert len(septs)==2

    diffs = vec2(septs[1][0]-septs[0][0],septs[1][1]-septs[0][1])
    steps = round(diffs.dist)+2
    if steps<1:
        return [vec2(septs[0][0],septs[0][1])]
    step = diffs/steps
    loc=vec2(septs[0][0],septs[0][1])
    points=[loc]

    mult=0
    if dist!=-1:
        mult=dist/diffs.dist#get what it needs to be (dist wanted/dist made)
        diffs*=mult#then apply that
        steps = round(diffs.dist)+2
        if not steps>0:
            return [vec2(septs[0][0],septs[0][1])]
        step = diffs/steps

    loc=vec2(septs[0][0],septs[0][1])
    points=[loc]

    for x in range(steps):
        loc+=step
        check=round(loc)
        if check!=points[-1]:
            if steps==0 or not (-1<check[0]<len(grid[0]) and -1<check[1]<len(grid)):
                break
            chk=checkFunc(check.x,check.y)
            if chk:
                points.append(check)
            else:
                break
        steps-=1
    if method=="end":
        return points[-1]
    else:
        return points

def pathGrid(steps,canGoFunc,grid,startPos):
    options=[[startPos[0],startPos[1],steps]]#[x,y,steps left] - DON'T EDIT, NEEDS SPEED!
    moves=[]#all x,y that you can movde to in <steps> steps
    dupe = grid

    while len(options)!=0:
        curr = options[0]

        if curr[2]>0:

            checks = [[curr[0]+i[0],curr[1]+i[1],curr[2]-1] for i in [[-1,0],[0,1],[1,0],[0,-1]]]

            for chk in checks:
                if not (-1<chk[0]<len(dupe[0]) and -1<chk[1]<len(dupe)):
                    continue

                if not chk[:-1] in moves and canGoFunc(chk[0],chk[1]):
                    moves.append(chk[:-1])
                    options.append(chk)

        del options[0]
    moves = [vec2(i[0],i[1]) for i in moves]
    return moves

def rayCircle(sp,radius,grid,checkFunc,method="check"):#raysquare, anyone?
    points=[]
    borders=circleGrid(radius,start_pos=sp,bordersOnly=True)
    for end in borders:
        pts = rayCast([sp,end],grid,checkFunc=checkFunc,method=method)
        points+=pts
    return points

class PathTree:
    def __init__(self,pos=(0,0),children=[],parent=None,name="anon"):
        self.parent=parent
        self.pos=pos
        self.children=children
        self.name=name

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
        tree=[self,[]]
        if self.children:
            for child in self.children:
                tree[1].append(child.getTree())
        return tree

    def addChild(self,pos=(0,0),children=[],name="anon"):
        child=PathTree(pos=pos,children=mapl(children),parent=self,name=name)
        self.children.append(child)
        return child

    def getPath(self,prev=None):
        if not prev:
            prev = []
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
    queue=explore_step(root,grid,canGoFunc)
    nq=[]
    while steps>0:
        for c in queue:
            if c.pos[0]==endPos[0] and c.pos[1]==endPos[1]:
                f=c.getPath()
                f = [vec2(i[0],i[1]) for i in f]
                return [f[-1-i] for i in range(len(f))]
            else:
                nq+=explore_step(c,grid,canGoFunc)
        steps-=1
        queue=mapl(nq)
        nq=[]
    return startPos

def explore_step(curr,grid,canGoFunc):
    ps = list(curr.pos)
    poss=[[ps[0]+i[0],ps[1]+i[1]] for i in [[-1,0],[1,0],[0,1],[0,-1]]]
    curr.children=[]
    for p in poss:
        if (curr.parent==None or p!=curr.parent.pos) and (-1<p[0]<len(grid[0]) and -1<p[1]<len(grid)) and canGoFunc(p[0],p[1]):
            if not ((p[0],p[1]) in curr.getPath()):
                curr.addChild(pos=(p[0],p[1]))
    return curr.children
