from gridView import *
from gridClasses import *
from equipment import *
from gridGeo import *
from time import sleep

if __name__ == "__main__":
    filePrint("______NEW______")
    #0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
    def main(stdscr):
        curses.start_color()
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_GREEN)
        curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_RED)
        curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_CYAN)
        curses.init_pair(5,curses.COLOR_BLACK,curses.COLOR_WHITE)

        curses.noecho()#terminal doesn't get keypresses
        curses.cbreak()#take keypresses
        curses.curs_set(0)# Hide the cursor
        stdscr.keypad(True)#make arrow keys not be escape sequences

        cg = cursedgrid([30,30],stdscr,defaultCell=".")
        camsize=(10,10)
        cam = cursedcam(camsize,stdscr,cg)
        from random import randint
        za = [[1,1],[1,0],[1,2],[0,4],[1,4]]
        for cell in za:
            cg.grid[cell[1]][cell[0]][0]="#"

        cg.rollText("started")

        cursorPos = [0,0]
        def wcp():
            return [cam.pos[0]+cursorPos[0],cam.pos[1]+cursorPos[1]]

        cam.push_view()
        cg.push_text()

        player = Unit([0,0],"Talus",["Hammer","Burst Rifle"],"Fiber Skeletals",kind="player",gridSize=[30,30])
        def cangf(gc):
            # filePrint(gc)
            if gc[0]==".":
                return True
            return False
        units=[player]

        block = ClassCell([3,3],"terrain",health=1000,name="Jonesy")

        #[filePrint(str(i)+": "+str(getattr(player,i))) for i in dir(player)]

        time=0
        state=0#0: selecting 1: moving 2: shooting
        okays=[]
        #__init__(self,coords,frame,weapons,armor,kind="enemy",gridSize=[99999,99999]):

        #initial render
        cg.grid[player.pos[1]][player.pos[0]][0]="o"
        cam.celclears.append(player.pos)

        cam.push_view()
        cg.push_text()

        while True:
            # Wait for a keystroke before doing anything
            key = stdscr.getkey()


            if key == "KEY_LEFT" and cam.pos[0]!=0:
                cam.pos[0]-=1
            elif key == "KEY_RIGHT" and cam.pos[0]!=cg.gridSize[0]:
                cam.pos[0]+=1
            elif key == "KEY_UP" and cam.pos[1]!=0:
                cam.pos[1]-=1
            elif key == "KEY_DOWN" and cam.pos[1]!=cg.gridSize[1]:
                cam.pos[1]+=1

            elif key=="w" and cursorPos[1]!=0:
                cursorPos[1]-=1
            elif key=="s" and cursorPos[1]!=camsize[1]-1:
                cursorPos[1]+=1
            elif key=="a" and cursorPos[0]!=0:
                cursorPos[0]-=1
            elif key=="d" and cursorPos[0]!=camsize[0]-1:
                cursorPos[0]+=1

            if state==0:
                if key=="m":
                    state=1
                    time=player.act_time
                    player.wait_time=player.act_time
                # elif key=="1":
                #     state=2
                # elif key=="2":
                #     state=2

            if state==1 and key=="\n":
                cusp=wcp()
                if cusp!=player.pos and cusp in okays:
                    state=0
                    okays=[]
                    player.pos=cusp

            if key =="q":
                if state==0:
                    break
                else:
                    state=0

            #colors
            if state==1:
                for p in pathGrid(player.move_max,cangf,cg.grid,player.pos):
                    okays.append(p)
                    cg.grid[p[1]][p[0]][1]=5
                    cam.colclears.append(p)
                pos = wcp()
                cg.grid[pos[1]][pos[0]][1]=4
                cam.colclears.append(pos)
            # if state==2:
            #     pos = wcp()
            #     cg.grid[pos[1]][pos[0]][1]=3
            #     cam.colclears.append(pos)

            #objects
            cg.grid[player.pos[1]][player.pos[0]][0]="o"
            cam.celclears.append(player.pos)

            cam.push_view()
            cg.push_text()

            cg.rollText("")

    curses.wrapper(main)
