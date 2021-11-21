from gridHelpers import *
import curses

#CUSTOMS

def gf(cell):
    return forcefit(cell,1)

#END CUSTOMS

def filePrint(text,file="output.txt"):
    with open(file,"r") as s:
        pre=s.read()
    with open(file,"w") as fl:
        if type(text) == list:
            fl.write(pre+"\n"+" ".join([str(e) for e in text]))
            fl.close()
        else:
            fl.write(pre+"\n"+str(text))
            fl.close()

class cursedgrid():
    def __init__(self,size,screen,textBoxes=[5],defaultCell=" ",resize=True):#textboxes[height,height,height]
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

    def __str__(self):
        return "\n".join([str(i) for i in range(self.grid)])

    def initScr(size,screen,defaultCell=" ",resize=False):
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

    def cellSwap(self,poso,post):
        temp = self.grid[poso[1]][poso[0]]
        self.grid[poso[1]][poso[0]] = self.grid[post[1]][post[0]]
        self.grid[post[1]][post[0]] = temp

    def rollText(self,text,index=0):
        assert index<len(self.textBoxes)

        self.textBoxes[index]["text"].append(str(text))
        box=self.textBoxes[index]
        if len(box["text"])>box["size"]:
            del self.textBoxes[index]["text"][0]

    def render(self,getFunc=gf):
        self.push_to_screen(getFunc=getFunc)
        for i in range(self.screenSize[1],self.screenSize[1]+self.textSize-1):
            index=i-self.screenSize[1]
            if len(self.text)>index:
                self.scr.addstr(i,0," "+forcefit(self.text[index],self.screenSize[0]-1,pos="r"))
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
                    self.scr.addch(y,x,getFunc(self.grid[y][x//2]))

if __name__ == "__main__":
    filePrint("______NEW______")
    def main(stdscr):
        stdscr.start_color()
        # stdscr.resize(51,101)
        cg = cursedgrid([10,10],stdscr,defaultCell=" ")
        cg.grid = [
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
        ]

        curses.noecho()#terminal doesn't get keypresses
        curses.cbreak()#take keypresses
        curses.curs_set(0)# Hide the cursor
        stdscr.keypad(True)#make arrow keys not be escape sequences

        lpos=[0,0]
        pos=[0,0]
        cg.grid[0][0]="x"
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

            cg.cellSwap(lpos,pos)
            lpos = [pos[0],pos[1]]

    curses.wrapper(main)
