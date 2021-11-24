from helpers import *
import curses

#CUSTOMS

def gf(cell):
    return forcefit(cell,1)

#END CUSTOMS

class cursedgrid():
    def __init__(self,size,screen,textBoxes=[5],defaultCell=[" ",1],resize=True):#textboxes[height,height,height]
        #speed vars
        self.defCell=defaultCell
        self.gridSize=size
        self.screenSize=[size[0]*2+2,size[1]+1]
        self.textBoxes=[{"size":i,"text":[" " for j in range(i)]} for i in textBoxes]
        self.textSize=0
        for l in textBoxes:
            self.textSize+=l

        if resize:
            screen.resize(self.screenSize[1]+self.textSize,self.screenSize[0])

        self.grid = [[defaultCell for j in range(self.gridSize[0]+1)] for i in range(self.gridSize[1]+1)]
        self.scr=screen

    def __str__(self):
        return "\n".join([str(i) for i in range(self.grid)])

    def initScr(size,screen,defaultCell=[" ",1],resize=False):
        #speed vars
        self.defCell=defaultCell
        self.gridSize=size
        self.screenSize=[size[0]*2+2,size[1]+1]
        self.textBoxes=[{"size":i,"text":[" " for j in range(i)]} for i in textBoxes]
        self.textSize=sum([textBoxes])

        if resize:
            screen.resize(self.screenSize[1]+self.textSize,self.screenSize[0])

        self.grid = [[defaultCell for j in range(self.gridSize[0]+1)] for i in range(self.gridSize[1]+1)]
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
        assert index<len(self.textBoxes)

        self.textBoxes[index]["text"].append(str(text))
        box=self.textBoxes[index]
        if len(box["text"])>box["size"]:
            del self.textBoxes[index]["text"][0]

    def render(self,getFunc=gf):
        self.push_to_screen(getFunc=getFunc)
        box=0
        minus=0
        for i in range(self.screenSize[1],self.screenSize[1]+self.textSize-1):
            index=i-self.screenSize[1]
            if i>self.textBoxes[box]["size"]:
                box+=1
                if len(self.textBoxes)==box:
                    break
            text = self.textBoxes[box]["text"][i-minus]
            minus+=1
            if len(text)>index:
                self.scr.addstr(i,0," "+forcefit(text,self.screenSize[0]-1,pos="r"))
            else:
                self.scr.addstr(i,0," "*self.screenSize[0])
        self.scr.refresh()

    def push_to_screen(self,getFunc=gf):
        for y in range(self.screenSize[1]):
            for x in range(self.screenSize[0]):
                # if x<5 and y<5:
                #     filePrint(str(x)+","+str(y))
                self.scr.addch(y,x," ")#fill in empty space
                if x%2==0:
                    cell = self.grid[y][x//2]
                    filePrint(cell)
                    self.scr.addch(y,x,getFunc(cell[0]),curses.color_pair(cell[1]))

class cursedcam():
    def __init__(self,out,screen,defaultCell=[" ",1]):
        #speed vars
        self.defCell=defaultCell
        self.outRange = out

        self.grid = [[defaultCell for j in range(self.gridSize[0]+1)] for i in range(self.gridSize[1]+1)]
        self.scr=screen

    def __str__(self):
        return "\n".join([str(i) for i in range(self.grid)])

    def initScr(size,screen,defaultCell=[" ",1],resize=False):
        #speed vars
        self.defCell=defaultCell
        self.gridSize=size
        self.screenSize=[size[0]*2+2,size[1]+1]
        self.textBoxes=[{"size":i,"text":[" " for j in range(i)]} for i in textBoxes]
        self.textSize=sum([textBoxes])

        if resize:
            screen.resize(self.screenSize[1]+self.textSize,self.screenSize[0])

        self.grid = [[defaultCell for j in range(self.gridSize[0]+1)] for i in range(self.gridSize[1]+1)]
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
        assert index<len(self.textBoxes)

        self.textBoxes[index]["text"].append(str(text))
        box=self.textBoxes[index]
        if len(box["text"])>box["size"]:
            del self.textBoxes[index]["text"][0]

    def render(self,getFunc=gf):
        self.push_to_screen(getFunc=getFunc)
        box=0
        minus=0
        for i in range(self.screenSize[1],self.screenSize[1]+self.textSize-1):
            index=i-self.screenSize[1]
            if i>self.textBoxes[box]["size"]:
                box+=1
                if len(self.textBoxes)==box:
                    break
            text = self.textBoxes[box]["text"][i-minus]
            minus+=1
            if len(text)>index:
                self.scr.addstr(i,0," "+forcefit(text,self.screenSize[0]-1,pos="r"))
            else:
                self.scr.addstr(i,0," "*self.screenSize[0])
        self.scr.refresh()

    def push_to_screen(self,getFunc=gf):
        for y in range(self.screenSize[1]):
            for x in range(self.screenSize[0]):
                # if x<5 and y<5:
                #     filePrint(str(x)+","+str(y))
                self.scr.addch(y,x," ")#fill in empty space
                if x%2==0:
                    cell = self.grid[y][x//2]
                    filePrint(cell)
                    self.scr.addch(y,x,getFunc(cell[0]),curses.color_pair(cell[1]))

if __name__ == "__main__":
    from gridGeo import *
    from gridClasses import *
    filePrint("______NEW______")
    #0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
    def main(stdscr):
        curses.start_color()
        # stdscr.resize(51,101)
        cg = cursedgridsq([10,10],stdscr,defaultCell=["x",10])
        curses.init_pair(10,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_GREEN)
        curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_RED)
        curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_CYAN)
        # cg.grid = [
        #     [" "," "," "," "," "," "," "," "," "," "],
        #     [" "," "," "," "," "," "," "," "," "," "],
        #     [" "," "," "," "," "," "," "," "," "," "],
        #     [" "," "," "," "," "," "," "," "," "," "],
        #     [" "," "," "," "," "," "," "," "," "," "],
        #     [" "," "," "," "," "," "," "," "," "," "],
        #     [" "," "," "," "," "," "," "," "," "," "],
        #     [" "," "," "," "," "," "," "," "," "," "],
        #     [" "," "," "," "," "," "," "," "," "," "],
        #     [" "," "," "," "," "," "," "," "," "," "],
        #     [" "," "," "," "," "," "," "," "," "," "],
        # ]

        curses.noecho()#terminal doesn't get keypresses
        curses.cbreak()#take keypresses
        curses.curs_set(0)# Hide the cursor
        stdscr.keypad(True)#make arrow keys not be escape sequences

        lpos=[0,0]
        pos=[0,0]
        filePrint(cg.grid[0])
        # cg.grid[0][0][1]=2
        cg.rollText("start")

        while True:
            cg.render()

            # Wait for a keystroke before doing anything
            key = stdscr.getch()

            if key == curses.KEY_LEFT and pos[0]!=0:
                pos[0]-=1
                cg.rollText("left {} {}".format(pos[0],pos[1]))
            elif key == curses.KEY_RIGHT and pos[0]!=cg.gridSize[0]:
                pos[0]+=1
                cg.rollText("right {} {}".format(pos[0],pos[1]))
            elif key == curses.KEY_UP and pos[1]!=0:
                pos[1]-=1
                cg.rollText("up {} {}".format(pos[0],pos[1]))
            elif key == curses.KEY_DOWN and pos[1]!=cg.gridSize[1]:
                pos[1]+=1
                cg.rollText("down {} {}".format(pos[0],pos[1]))
            elif key == ord('q'):
                break

            cg.cellSwap(lpos,pos,way=2)
            lpos = [pos[0],pos[1]]

    curses.wrapper(main)
