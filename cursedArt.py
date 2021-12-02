from gridView import *

if __name__ == "__main__":
    filePrint("______NEW______")
    #0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
    def main(stdscr):
        curses.start_color()
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_GREEN)
        curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_RED)
        curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_CYAN)
        curses.init_pair(5,curses.COLOR_GREEN,curses.COLOR_WHITE)

        curses.noecho()#terminal doesn't get keypresses
        curses.cbreak()#take keypresses
        curses.curs_set(0)# Hide the cursor
        stdscr.keypad(True)#make arrow keys not be escape sequences

        cg = cursedgrid([30,30],stdscr,defaultCell=".")
        camsize=(10,10)
        cam = cursedcam(camsize,stdscr,cg.grid)

        cg.rollText("started")
        filePrint(cg)

        askis = {}
        def ak(key):
            askis[key] = ord(key)
        [ak(c) for c in "qcv1234567890fsdw"]

        copied = []#[x,y,contents]
        copying=False

        cursorPos = [0,0]

        cam.push_view()
        cg.push_text()

        while True:
            # Wait for a keystroke before doing anything
            key = stdscr.getkey()

            moved=False
            if key == "KEY_LEFT" and cam.pos[0]!=0:
                cam.pos[0]-=1
                moved=True
            elif key == "KEY_RIGHT" and cam.pos[0]!=cg.gridSize[0]:
                cam.pos[0]+=1
                moved=True
            elif key == "KEY_UP" and cam.pos[1]!=0:
                cam.pos[1]-=1
                moved=True
            elif key == "KEY_DOWN" and cam.pos[1]!=cg.gridSize[1]:
                cam.pos[1]+=1
                moved=True

            elif key=="w" and cursorPos[1]!=0:
                cursorPos[1]-=1
                moved=True
            elif key=="s" and cursorPos[1]!=camsize[1]-1:
                cursorPos[1]+=1
                moved=True
            elif key=="a" and cursorPos[0]!=0:
                cursorPos[0]-=1
                moved=True
            elif key=="d" and cursorPos[0]!=camsize[0]-1:
                cursorPos[0]+=1
                moved=True


            elif key=="x":
                cg.grid[cam.pos[1]+cursorPos[1]][cam.pos[0]+cursorPos[0]][0] = "x"


            elif key=="C":
                if copying:
                    copying=False
                else:
                    copying=True

            elif key=="X":
                copied=[]

            elif key=="V" and copied!=[]:
                cello = copied[0]
                for cell in copied:
                    cg.grid[cam.pos[1]+cursorPos[1]+cell[1]-cello[1]][cam.pos[0]+cursorPos[0]+cell[0]-cello[0]][0] = cell[2]


            elif key =="q":
                break

            if moved and copying:
                to = [
                    cam.pos[0]+cursorPos[0],
                    cam.pos[1]+cursorPos[1],
                    mapl(cg.grid[cam.pos[1]+cursorPos[1]][cam.pos[0]+cursorPos[0]][0])
                ]
                if not to in copied:
                    copied.append(to)

            if copied!=[]:
                for c in copied:
                    cg.grid[c[1]][c[0]][1] = 3
                    cam.colclears.append([c[0],c[1]])

            #temporary colors
            pos =[cam.pos[0]+cursorPos[0],cam.pos[1]+cursorPos[1]]
            cg.grid[pos[1]][pos[0]][1]=5
            cam.colclears.append(pos)

            if not copying and copied!=[]:
                cello = copied[0]
                for cell in copied:
                    pos = [cam.pos[0]+cursorPos[0]+cell[0]-cello[0],cam.pos[1]+cursorPos[1]+cell[1]-cello[1]]
                    cg.grid[pos[1]][pos[0]][1] = 4
                    cam.colclears.append(pos)

            cam.push_view()
            cg.push_text()

    curses.wrapper(main)
