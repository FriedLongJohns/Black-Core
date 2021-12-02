from helpers import *
import curses

#CUSTOMS

def gf(cell):
    return forcefit(cell,1)

#END CUSTOMS

class cursedgrid():
    def __init__(self,size,screen,textSize=5,defaultCell=" ",defaultColor=1,resize=True):#textboxes[height,height,height]
        #speed vars
        self.gridSize=size
        self.screenSize=[size[0]*2+2,size[1]+1]
        self.textbox={"size":textSize,"text":[" " for j in range(textSize)]}
        self.textSize=textSize
        self.defColor=defaultColor
        self.defCell=defaultCell

        if resize:
            screen.resize(self.screenSize[1]+self.textSize,self.screenSize[0])

        self.grid = [[[mapl(defaultCell),defaultColor] for j in range(self.gridSize[0]+1)] for i in range(self.gridSize[1]+1)]
        self.scr=screen

    def __str__(self):
        return "\n".join([str(i) for i in self.grid])

    def initScr(size,screen,defaultCell=[" ",1],resize=False):
        #speed vars
        self.defCell=defaultCell
        self.gridSize=size
        self.screenSize=[size[0]*2+2,size[1]+1]
        self.textbox={"size":textSize,"text":[" " for j in range(textSize)]}
        self.textSize=textSize

        if resize:
            screen.resize(self.screenSize[1]+self.textSize,self.screenSize[0])

        self.grid = [[[mapl(defaultCell),defaultColor] for j in range(self.gridSize[0]+1)] for i in range(self.gridSize[1]+1)]
        self.scr=screen

    def repRange(self,borders,clearCell="˜¨¬¬"):#˜¨¬¬ is null but holding option down >:)
        repCell=clearCell

        if clearCell=="˜¨¬¬":
            repCell=self.defCell

        for x in range(borders[0][0],borders[1][0]+1):
            for y in range(borders[0][1],borders[1][1]+1):
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


    def rollText(self,text):
        self.textbox["text"].append(str(text))
        if len(self.textbox["text"])>self.textbox["size"]:
            del self.textbox["text"][0]

    def push_text(self,getFunc=gf):
        for i in range(self.screenSize[1],self.screenSize[1]+self.textSize-1):
            index=i-self.screenSize[1]+1
            if index<self.textbox["size"]:
                text = self.textbox["text"][index]
                self.scr.addstr(i,0," "+forcefit(text,self.screenSize[0]-1,pos="r"))
            else:
                self.scr.addstr(i,0," "+forcefit("",self.screenSize[0]-1,pos="r"))
        self.scr.refresh()

    def push_grid(self,getFunc=gf):
        for y in range(self.screenSize[1]):
            for x in range(self.screenSize[0]):
                self.scr.addch(y,x," ")
                if x%2==0:
                    cell = self.grid[y][x//2]
                    self.scr.addch(y,x,getFunc(cell[0]),curses.color_pair(cell[1]))
        self.scr.refresh()

class cursedcam():
    def __init__(self,viewSize,screen,cgrid,viewportOffset=[0,0],pos=[0,0]):
        #speed vars
        self.viewSize = viewSize
        self.viewportOffset = viewportOffset
        self.pos = pos

        self.scr=screen
        self.grid=cgrid.grid
        self.cgrid=cgrid

        self.colclears=[]
        self.celclears=[]

    def push_view(self,getFunc=gf):
        for y in range(self.pos[1],self.pos[1]+self.viewSize[1]):
            for x in range(self.pos[0],self.pos[0]+self.viewSize[0]):
                if -1<y<len(self.grid) and -1<x<len(self.grid[0]):
                    cell = self.grid[y][x]
                    self.scr.addch(y-self.pos[1]+self.viewportOffset[1],(x-self.pos[0]+self.viewportOffset[0])*2,getFunc(cell[0]),curses.color_pair(cell[1]))
                    if [x,y] in self.colclears:
                            self.grid[y][x][1]=self.cgrid.defColor
                    if [x,y] in self.celclears:
                            self.grid[y][x][0]=self.cgrid.defCell
                else:
                    self.scr.addch(y-self.pos[1]+self.viewportOffset[1],(x-self.pos[0]+self.viewportOffset[0])*2," ")
        self.colclears=[]
