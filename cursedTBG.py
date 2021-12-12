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

        stdscr.resize(300,300)
        gP = [100,20]
        cg = cursedgrid([[gP[0],gP[1]],[50+gP[0],50+gP[1]]],stdscr,defaultCell=".")#to make things square

        camsize=(10,10)
        cam = cursedcam(camsize,stdscr,cg,outOffset=[int(gP[0]/2),gP[1]])
        ctex=cursedtext([[gP[0],11+gP[1]],[30+gP[0],14+gP[1]]],stdscr,rolling=True)
        ptex=cursedtext([[21+gP[0],gP[1]],[30+gP[0]*2,11+gP[1]]],stdscr,rolling=False)

        # filePrint(cg.grid)

        za = [[1,1],[1,0],[1,2],[0,4],[1,4]]
        for cell in za:
            cg.grid[cell[1]][cell[0]][0]="#"

        ctex.addText("started")
        ptex.text[0]="last turn time: 0s"

        cursorPos = [0,0]
        def wcp():
            return [cam.pos[0]+cursorPos[0],cam.pos[1]+cursorPos[1]]

        player = Unit([0,0],"Talus",["Hammer","Burst Rifle"],"Fiber Skeletals",kind="player")
        def cangf(gc):
            ctex.addText(gc)
            if gc[0]==".":
                return True
            return False
        def canff(gc):
            # filePrint(gc)
            if gc[0] in "#":
                return False
            return True
        def getwt(unit):
            return unit.wait_time
        units=[player]

        # block = ClassCell([3,3],"terrain",health=1000,name="Jonesy")

        time=0
        state=0#0: selecting 1: moving 2: shooting first weapon 3: shooting second weapon
        okays=[]

        #initial render
        cg.grid[player.pos[1]][player.pos[0]][0]="o"
        cam.celclears.append(player.pos)

        cam.push()
        ctex.push()
        ptex.push()
        filePrint(tryPathFind(3,cangf,cg.grid,player.pos,(4,2)))

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
                elif key=="1" and not player.wps[0][3]>0:
                    state=2
                elif key=="2" and not player.wps[1][3]>0:
                    state=3

            ctex.addText("state: {} cursorPos: {}".format(state,wcp()))

            if key=="\n" and state!=0:
                cusp=wcp()
                if cusp in okays:
                    if state==1:
                        time=player.act_time
                        player.wait_time=time
                        player.pos=cusp
                    elif state==2:
                        time=player.wps[0][2]#the use time of the weapon is autocalculated already
                        player.wait_time=time
                        player.wps[0][3]=player.wps[0][1]["cooldown"]
                    elif state==3:
                        time=player.wps[1][2]#the use time of the weapon is autocalculated already
                        player.wait_time=time
                        player.wps[1][3]=player.wps[1][1]["cooldown"]
                    state=0
                    okays=[]

                    ctex.addText("did action, taking {} time".format(str(time)))
                    ptex.text[0]="last turn time: ."+str(time)+"s"

            if key =="q":
                if state==0:
                    break
                else:
                    state=0

            #time+ai
            if time!=0:
                # cg.rollText("time passed: {}".format(time))
                for un in units:
                    un.wait_time-=time
                    un.wps[0][3]-=time
                    un.wps[1][3]-=time
                    # if un.wait_time<=0 and un.kind!="player":
                    #     #do ai stuff
                time=0
                noneCanMove=True
                min=9999999999
                for un in units:
                    oir=un.wait_time>0
                    if un.wait_time<min:
                        min=un.wait_time
                if noneCanMove:
                    for un in units:
                        un.wait_time-=min


            #EFFECTS
            #colors
            if state==1:
                for p in pathGrid(player.move_max,cangf,cg.grid,player.pos):
                    okays.append(p)
                    cg.grid[p[1]][p[0]][1]=5
                    cam.colclears.append(p)
                pos = wcp()
                cg.grid[pos[1]][pos[0]][1]=4
                cam.colclears.append(pos)

            elif state in [2,3]:
                for p in rayCircle(player.pos,player.wps[state-2][1]["range"],cg.grid,canff):
                    okays.append(p)
                    cg.grid[p[1]][p[0]][1]=5
                    cam.colclears.append(p)
                pos = wcp()
                cg.grid[pos[1]][pos[0]][1]=3
                cam.colclears.append(pos)

            #objects
            cg.grid[player.pos[1]][player.pos[0]][0]="o"
            cam.celclears.append(player.pos)

            cam.push()
            ptex.push()
            ctex.push()

            stdscr.refresh()

    curses.wrapper(main)
