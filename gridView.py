from helpers import *
import curses
from classtypes import vec2

#CUSTOMS

def gf(cell):
    return forcefit(cell,1)

#END CUSTOMS

class cursedgrid():
    def __init__(self,crdRang,screen,defaultCell=" ",defaultColor=0):
        #speed vars
        self.range=crdRang
        self.gridSize=vec2(crdRang[1][0]-crdRang[0][0],crdRang[1][1]-crdRang[0][1])
        self.bigSize=vec2(self.gridSize.x*2+2,self.gridSize.y+1)
        self.defColor=defaultColor
        self.defCell=defaultCell

        self.grid = [[[mapl(defaultCell),defaultColor] for j in range(self.gridSize.x+1)] for i in range(self.gridSize.y+1)]
        self.scr=screen

    def __str__(self):
        return "\n".join([str(i) for i in self.grid])

    def initScr(self,crdRang,screen,defaultCell=" ",defaultColor=1):
        #speed vars
        self.rang=crdRang
        self.bigSize=vec2(crdRang[1][0]-crdRang[0][0]+1,crdRang[1][1]-crdRang[0][1]+1)
        self.gridSize=vec2(int(self.gridSize.x/2)+self.gridSize.x%2,self.gridSize.y)
        self.defColor=defaultColor
        self.defCell=defaultCell

        self.grid = [[[mapl(defaultCell),defaultColor] for j in range(self.gridSize.x+1)] for i in range(self.gridSize.y+1)]
        self.scr=screen

    def repRange(self,rang,clearCell="˜¨¬¬",clearColor=-1):#˜¨¬¬ is null but holding option down >:)
        repCell=[clearCell,clearColor]

        if clearCell=="˜¨¬¬":
            repCell[0]=self.defCell
        if clearColor==-1:
            repCell[1]=self.defColor

        for x in range(rang[0][0],rang[1][0]+1):
            for y in range(rang[0][1],rang[1][1]+1):
                self.grid[y][x]=repCell

    def cellSwap(self,poso,post,way=0):#ways: 0-all 1-no color 2-only colors
        temp = self.grid[poso[1]][poso[0]]
        if way==0:
            self.grid[poso[1]][poso[0]] = self.grid[post[1]][post[0]]
            self.grid[post[1]][post[0]] = temp
        elif way==1:
            self.grid[poso[1]][poso[0]][0] = self.grid[post[1]][post[0]][0]
            self.grid[post[1]][post[0]][0] = temp[0]
        else:
            self.grid[poso[1]][poso[0]][1] = self.grid[post[1]][post[0]][1]
            self.grid[post[1]][post[0]][1] = temp[1]

    def push(self,getFunc=gf):
        for y in range(self.gridSize.y):
            for x in range(self.gridSize.x):
                self.scr.addch(y,x," ")
                if x%2==0:
                    cell = self.grid[y][x//2]
                    self.scr.addch(y,x,getFunc(cell[0]),curses.color_pair(cell[1]))

class cursedcam():
    def __init__(self,viewSize,screen,cgrid,outOffset=[0,0],pos=[0,0]):
        #speed vars
        self.viewSize = viewSize
        self.outOffset = outOffset
        self.pos = pos

        self.scr=screen
        self.grid=cgrid.grid
        self.cgrid=cgrid

        self.color_overrides={}#"[5,2]": 2, etc
        self.cell_overrides={}

    def push(self,getFunc=gf):
        for y in range(self.pos[1],self.pos[1]+self.viewSize[1]):
            for x in range(self.pos[0],self.pos[0]+self.viewSize[0]):
                # self.scr.addch(y-self.pos[1]+self.outOffset[1],(x-self.pos[0]+self.outOffset[0])*2,"x")
                if -1<y<len(self.grid) and -1<x<len(self.grid[0]):
                    cell = self.grid[y][x]
                    dicell = getFunc(cell[0])
                    colr = curses.color_pair(cell[1])
                    pch = str(vec2(x,y))
                    if pch in self.color_overrides.keys():
                        colr = self.color_overrides[pch]
                        # filePrint("[cam] pos: {} color: {}".format((x,y),colr))
                    if pch in self.cell_overrides.keys():
                        dicell = self.cell_overrides[pch]
                    self.scr.addch(y-self.pos[1]+self.outOffset[1],(x-self.pos[0]+self.outOffset[0])*2,dicell,curses.color_pair(colr))
                else:
                    self.scr.addch(y-self.pos[1]+self.outOffset[1],(x-self.pos[0]+self.outOffset[0])*2," ")

class cursedtext():
    def __init__(self,posrang,screen,text=[],rolling=True):
        self.rang=posrang
        self.size=[posrang[1][0]-posrang[0][0]+1,posrang[1][1]-posrang[0][1]+1]
        self.rolling=rolling
        self.text=text
        self.scref=screen
        if not rolling and text==[]:
            self.text=[""*self.size[0] for i in range(self.size[1])]

    def addText(self,text):
        self.text.append(str(text))
        if len(self.text)>self.size[1]:
            del self.text[0]

    def push(self):
        for i in range(self.rang[0][1],self.rang[1][1]+1):
            index=i-self.rang[0][1]
            if index<len(self.text):
                text = self.text[index]
                self.scref.addstr(i,self.rang[0][0]," "+forcefit(self.text[index],self.size[0],pos="r"))
            else:
                self.scref.addstr(i,self.rang[0][0]," "+forcefit("",self.size[0],pos="r"))
