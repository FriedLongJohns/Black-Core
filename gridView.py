from helpers import *
import curses

#CUSTOMS

def gf(cell):
    return forcefit(cell,1)

#END CUSTOMS

class cursedgrid():
    def __init__(self,size,screen,textSize=5,defaultCell=" ",defaultColor=1,resize=True):#textboxes[height,height,height]
        #speed vars
        self.defCell=defaultCell
        self.gridSize=size
        self.screenSize=[size[0]*2+2,size[1]+1]
        self.textbox={"size":textSize,"text":[" " for j in range(textSize)]}
        self.textSize=textSize

        if resize:
            screen.resize(self.screenSize[1]+self.textSize,self.screenSize[0])

        self.grid = [[[map(defaultCell),defaultColor] for j in range(self.gridSize[0]+1)] for i in range(self.gridSize[1]+1)]
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

        self.grid = [[[map(defaultCell),defaultColor] for j in range(self.gridSize[0]+1)] for i in range(self.gridSize[1]+1)]
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


    def rollText(self,text,index=0):
        assert index<len(self.textbox)

        self.textbox["text"].append(str(text))
        if len(self.textbox["text"])>self.textbox["size"]:
            del self.textbox["text"][0]

    def push_text(self,getFunc=gf):
        for i in range(self.screenSize[1],self.screenSize[1]+self.textSize-1):
            index=i-self.screenSize[1]
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
    def __init__(self,viewSize,screen,grid,viewportOffset=[0,0],pos=[0,0]):
        #speed vars
        self.viewSize = viewSize
        self.viewportOffset = viewportOffset
        self.pos = pos

        self.scr=screen
        self.grid=grid

    def push_view(self,getFunc=gf):
        for y in range(self.pos[1],self.pos[1]+self.viewSize[1]):
            for x in range(self.pos[0],self.pos[0]+self.viewSize[0]):
                if -1<y<len(self.grid) and -1<x<len(self.grid[0]):
                    cell = self.grid[y][x]
                    self.scr.addch(y-self.pos[1]+self.viewportOffset[1],(x-self.pos[0]+self.viewportOffset[0])*2,getFunc(cell[0]),curses.color_pair(cell[1]))
                else:
                    self.scr.addch(y-self.pos[1]+self.viewportOffset[1],(x-self.pos[0]+self.viewportOffset[0])*2," ")

if __name__ == "__main__":
    from gridGeo import *
    from gridClasses import *
    filePrint("______NEW______")
    #0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
    def main(stdscr):
        curses.start_color()
        # stdscr.resize(51,101)
        cg = cursedgrid([10,10],stdscr,defaultCell="x")
        cam = cursedcam([5,5],stdscr,cg.grid)
        curses.init_pair(10,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_GREEN)
        curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_RED)
        curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_CYAN)
        k = [
            [" "," ","x"," ","x"," "," "," "," "," "],
            [" "," ","x"," ","x"," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" ","x"," "," "," ","x"," "," "," "," "],
            [" "," ","x","x","x"," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," ","x"," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
        ]
        for y in range(len(k)):
            for x in range(len(k[0])):
                cg.grid[y][x][0]=k[y][x]


        curses.noecho()#terminal doesn't get keypresses
        curses.cbreak()#take keypresses
        curses.curs_set(0)# Hide the cursor
        stdscr.keypad(True)#make arrow keys not be escape sequences

        cg.rollText("started")
        filePrint(cg)
        cam.push_view()
        cg.push_text()

        while True:
            # cg.render()

            # Wait for a keystroke before doing anything
            key = stdscr.getch()

            if key == curses.KEY_LEFT and cam.pos[0]!=0:
                cam.pos[0]-=1
                cg.rollText("left {} {}".format(cam.pos[0],cam.pos[1]))
            elif key == curses.KEY_RIGHT and cam.pos[0]!=cg.gridSize[0]:
                cam.pos[0]+=1
                cg.rollText("right {} {}".format(cam.pos[0],cam.pos[1]))
            elif key == curses.KEY_UP and cam.pos[1]!=0:
                cam.pos[1]-=1
                cg.rollText("up {} {}".format(cam.pos[0],cam.pos[1]))
            elif key == curses.KEY_DOWN and cam.pos[1]!=cg.gridSize[1]:
                cam.pos[1]+=1
                cg.rollText("down {} {}".format(cam.pos[0],cam.pos[1]))
            elif key == ord('q'):
                break

            # cg.cellSwap(lpos,pos,way=2)
            # lpos = [pos[0],pos[1]]
            cam.push_view()
            cg.push_text()

    curses.wrapper(main)
