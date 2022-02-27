from gridView import *
from gridClasses import *
from equipment import *
from gridGeo import *
from levelGen import *
from time import sleep
from classtypes import inf
import os

try:
    open(os.getcwd()+"/compiling_notes.txt","r").close()
    print("Running from file, will not clear log")
except:
    print("Running from exe, clearing log")
    with open(os.getcwd()+"/output.txt","w") as file:
        file.write("")

#versions so far:
#   Mink: Base
#   Sleuth: AI upgrade, animations
print("Current Version: Sleuth")

sleep(1)

if __name__ == "__main__":
    filePrint("______NEW______")
    def main(stdscr):
        curses.start_color()
        curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_GREEN)
        curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_RED)
        curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_CYAN)
        curses.init_pair(5,curses.COLOR_WHITE,curses.COLOR_BLUE)
        curses.init_pair(6,curses.COLOR_WHITE,curses.COLOR_MAGENTA)

        curses.noecho()#terminal doesn't get keypresses
        curses.cbreak()#take keypresses
        curses.curs_set(0)# Hide the cursor
        stdscr.keypad(True)#make arrow keys not be escape sequences

        stdscr.resize(60,90)
        uip=[4,4]#UI pos
        pGear=[0,0,2,0]

        def core(level,units,cg,objectiveFunc,tex,nameOverrides={}):
            camsize=(10,10)
            def cam_area():
                return [[cam.pos[0],cam.pos[1]],[cam.pos[0]+cam.viewSize[0],cam.pos[1]+cam.viewSize[1]]]

            cam=cursedcam(camsize,stdscr,cg,outOffset=uip)
            cursor_tex=cursedtext([[uip[0]*2,uip[1]+11],[200+uip[0]*2-1,11+uip[1]]],stdscr,rolling=False,text=[])
            list_tex=cursedtext([[uip[0]*2,uip[1]+13],[200+uip[0]*2-1,20+uip[1]]],stdscr,rolling=True,text=[])


            #unit and unit func setup
            player = Unit(
                [3,3],
                list(FRAMES.keys())[pGear[0]],
                [
                    list(WEAPONS.keys())[pGear[1]],
                    list(WEAPONS.keys())[pGear[2]],
                ],
                list(ARMORS.keys())[pGear[3]],
                kind="player",
                displayColor=2
            )
            for unit in units:
                if unit.kind=="enemy":
                    unit.displayColor=3
                elif unit.kind=="ally":
                    unit.displayColor=5
            units.append(player)

            #helper funcs
            def cangf(x,y):
                if cg.grid[y][x][0]=="." and (not vec2(x,y) in [unit.pos for unit in units]):
                    return True
                return False
            def canff(x,y):
                if cg.grid[y][x][0] == "#":
                    return False
                return True
            def getwt(unit):
                return unit.wait_time
            def wcp():
                return vec2(cam.pos[0]+cursorPos[0],cam.pos[1]+cursorPos[1])

            time=0
            state=0#0: selecting 1: moving 2: shooting first weapon 3: shooting second weapon
            okays=[]
            cursorPos = vec2(player.pos[0],player.pos[1])

            def render(clear=True,color=1,cell=1):#0: don't show 1: show if not overriding 2: force show
                for un in units:
                    if cell==2 or (cell==1 and not str(un.pos) in list(cam.cell_overrides.keys())):
                        cam.cell_overrides[str(un.pos)]=un.displayChar
                    if color==2 or (color==1 and not str(un.pos) in list(cam.color_overrides.keys())):
                        cam.color_overrides[str(un.pos)]=un.displayColor
                list_tex.push()
                cam.push()
                cursor_tex.push()
                stdscr.refresh()
                if clear:
                    cam.cell_overrides={}
                    cam.color_overrides={}

            list_tex.addText("GAME START")
            list_tex.addText(tex)
            cursor_tex.text[0]="cursoring: nothing"
            cam.color_overrides[str(wcp())]=1

            render()
            while True:
                if objectiveFunc(units)==True:
                    list_tex.addText("OBJECTIVE COMPLETED")
                    render()
                    sleep(1.2)
                    list_tex.addText("GAME SHUTDOWN")
                    render()
                    sleep(2.2)
                    return

                # Wait for a keystroke before doing anything
                key = stdscr.getkey()


                if key == "KEY_LEFT" and cam.pos[0]!=0:
                    cam.pos[0]-=1
                elif key == "KEY_RIGHT" and cam_area()[1][0]!=cg.gridSize[0]:
                    if wcp()[0]==cg.gridSize[0]-1:
                        cursorPos[0]-=1
                    cam.pos[0]+=1
                elif key == "KEY_UP" and cam.pos[1]!=0:
                    cam.pos[1]-=1
                elif key == "KEY_DOWN" and cam_area()[1][1]!=cg.gridSize[1]:
                    if wcp()[1]==cg.gridSize[1]-1:
                        cursorPos[1]-=1
                    cam.pos[1]+=1

                elif key=="w" and cursorPos[1]!=0:
                    cursorPos[1]-=1
                elif key=="s" and cursorPos[1]!=camsize[1]-1 and wcp()[1]!=cg.gridSize[1]:
                    cursorPos[1]+=1
                elif key=="a" and cursorPos[0]!=0:
                    cursorPos[0]-=1
                elif key=="d" and cursorPos[0]!=camsize[0]-1 and wcp()[0]!=cg.gridSize[0]:
                    cursorPos[0]+=1

                elif key in "mq12" and state==0:
                    if key=="m":
                        state=1
                    elif key=="q":
                        break
                    elif key=="1":
                        if not player.wps[0][3]>0:
                            state=2
                        else:
                            list_tex.addText("Weapon 1-{} is on cooldown!".format(player.wps[0][0]))
                            render()
                    elif key=="2":
                        if not player.wps[1][3]>0:
                            state=3
                        else:
                            list_tex.addText("Weapon 2-{} is on cooldown!".format(player.wps[1][0]))
                            render()
                    if state!=0:
                        cursorPos=[mapl(player.pos)[i]-mapl(cam.pos)[i] for i in range(2)]
                    render()

                elif key=="q":
                    state=0
                    cam.color_overrides={}

                elif key=="\n" and state!=0:
                    cusp=wcp()
                    if cusp in okays:
                        if state==1:
                            time=player.act_time
                            player.wait_time=time*1.5#player moves twice as fast as enemies, to make it fair
                            loine={}
                            for pos in tryPathFind(player.move_max,cangf,cg.grid,player.pos,cusp):
                                loine[str(pos)]=4
                                player.pos=pos
                                for key in loine.keys():
                                    cam.color_overrides[key]=loine[key]
                                render()
                                sleep(.1)
                            player.pos=cusp
                            render()
                        elif state in [2,3] and player.wps[state-2][3]<=0:
                            time=player.wps[state-2][2]#multiply acted wait time by 2 or they will be able to act again (wt=time,-time=0)
                            player.wait_time=time*1.5
                            player.wps[state-2][3]=player.wps[state-2][1]["cooldown"]/2
                            loine={}
                            for pos in lineGrid([player.pos,cusp]):
                                loine[str(pos)]=3
                                for key in loine.keys():
                                    cam.color_overrides[key]=loine[key]
                                render()
                                sleep(.05)
                            render()
                            for i in range(len(units)):
                                unit=units[i]
                                if cusp==unit.pos:
                                    list_tex.addText(unit.damage(player.wps[state-2][1]["damage"],player))
                                    if not unit.health>0:
                                        list_tex.addText(unit.name+" was destroyed!")
                                        del units[i]
                                        break
                            render()
                            sleep(.3)
                        state=0
                        okays=[]

                        #time+ai
                        for un in units:
                            un.wait_time-=time
                            un.wps[0][3]-=time
                            un.wps[1][3]-=time

                        while player.wait_time>0:
                            todo=mapl(units)
                            un=player
                            m=player.wait_time
                            for i in todo:
                                if i.wait_time<m:
                                    un=i
                                    if i.wait_time<=0:
                                        m=0
                                        break
                                    m=i.wait_time

                            for u in units:
                                u.wait_time-=m
                                u.wps[0][3]-=m
                                u.wps[1][3]-=m

                            if un==player:
                                break

                            else:
                                action=["wait"]
                                targets=[]
                                for other in units:
                                    if other!=un and (other.kind in ["ally","player"] and un.kind=="enemy") or (other.kind=="enemy" and un.kind=="ally"):
                                        targets.append(other)

                                if targets:#if no targets [], use else case and wait
                                    target=un.get_enemy(targets)
                                    action=un.think(target,canff,cangf,cg.grid)

                                if action[0]=="fire":
                                    time=un.wps[action[1]][2]
                                    un.wait_time=un.wps[action[1]][2]*2
                                    un.wps[action[1]][3]=un.wps[action[1]][1]["cooldown"]
                                    ca=cam_area()
                                    if between2d(target.pos,ca[0],ca[1]):
                                        for pos in rayCircle(un.pos,un.wps[action[1]][1]["range"],cg.grid,canff):
                                            cam.color_overrides[str(pos)]=1
                                        render()
                                        sleep(.1)
                                        loine={}
                                        for pos in lineGrid([un.pos,target.pos]):
                                            loine[str(pos)]=3
                                            for key in loine.keys():
                                                cam.color_overrides[key]=loine[key]
                                            render()
                                            sleep(.05)
                                        render()
                                        list_tex.addText(target.damage(un.wps[action[1]][1]["damage"],un))
                                    else:
                                        list_tex.addText(target.damage(un.wps[action[1]][1]["damage"],un))
                                    if target.health<=0:
                                        list_tex.addText("{} was destroyed".format(target.name))
                                        if target.kind=="player":
                                            list_tex.addText("PLAYER IS DEAD")
                                            render()
                                            sleep(1.2)
                                            list_tex.addText("GAME SHUTDOWN")
                                            render()
                                            sleep(2.2)
                                            return

                                        new=mapl(units)
                                        for i in range(len(units)):
                                            unit=units[i]
                                            if unit==target:
                                                del new[i]
                                                break
                                        units=mapl(new)

                                        new=mapl(todo)
                                        for i in range(len(todo)):
                                            unit=todo[i]
                                            if unit==target:
                                                del new[i]
                                                break
                                        todo=mapl(new)

                                        render()
                                    render()
                                    sleep(.5)
                                elif action[0]=="move":
                                    time=un.act_time
                                    un.wait_time=time*2
                                    ca=cam_area()
                                    if between2d(action[1],ca[0],ca[1]):
                                        for pos in tryPathFind(un.move_max,cangf,cg.grid,un.pos,action[1]):
                                            un.pos=pos
                                            loine[str(pos)]=4
                                            for key in loine.keys():
                                                cam.color_overrides[key]=loine[key]
                                            render()
                                            sleep(.1)
                                        un.pos=action[1]
                                        render()
                                    else:
                                        un.pos=action[1]
                                        render()
                                else:#wait
                                    time=.1
                                un.wait_time-=time
                                un.wps[0][3]-=time
                                un.wps[1][3]-=time
                                player.wait_time-=time
                                player.wps[0][3]-=time
                                player.wps[1][3]-=time
                                del todo[0]
                    else:
                        list_tex.addText("Cannot act there!")


                #colors
                if state==1:
                    for p in pathGrid(player.move_max,cangf,cg.grid,player.pos):
                        okays.append(p)
                        cam.color_overrides[str(p)]=1
                    pos = wcp()
                    if pos in okays:
                        cam.cell_overrides[str(pos)]="O"
                    else:
                        cam.cell_overrides[str(pos)]="X"

                    cursor_tex.text[0]="cursoring: nothing"
                    for unit in units:
                        if pos==unit.pos:
                            cursor_tex.text[0]="cursoring: {}".format(unit.name)
                    if cg.grid[pos[1]][pos[0]][0]=="#":
                            cursor_tex.text[0]="cursoring: wall"
                    elif str(pos) in nameOverrides.keys():
                        cursor_tex.text[0]="cursoring: "+nameOverrides[str(pos)]
                    render(cell=0,color=2)

                elif state in [2,3]:
                    for p in rayCircle(player.pos,player.wps[state-2][1]["range"],cg.grid,canff):
                        okays.append(p)
                        cam.color_overrides[str(p)]=1
                    pos = wcp()
                    if pos in okays:
                        cam.cell_overrides[str(pos)]="O"
                    else:
                        cam.cell_overrides[str(pos)]="X"

                    cursor_tex.text[0]="cursoring: nothing"
                    for unit in units:
                        if pos==unit.pos:
                            cursor_tex.text[0]="cursoring: {}".format(unit.name)
                    if cg.grid[pos[1]][pos[0]][0]=="#":
                            cursor_tex.text[0]="cursoring: wall"
                    elif str(pos) in nameOverrides.keys():
                        cursor_tex.text[0]="cursoring: "+nameOverrides[str(pos)]
                    render(cell=0,color=2)

                else:
                    cp=wcp()
                    cam.color_overrides[str(cp)]=1
                    cursor_tex.text[0]="cursoring: nothing"
                    for unit in units:
                        if cp==unit.pos:
                            cursor_tex.text[0]="cursoring: {}".format(unit.name)
                    if cg.grid[cp[1]][cp[0]][0]=="#":
                            cursor_tex.text[0]="cursoring: wall"
                    elif str(cp) in nameOverrides.keys():
                        cursor_tex.text[0]="cursoring: "+nameOverrides[str(cp)]
                    render()

        def gear():
            rtex=cursedtext([[22+uip[0]*2,uip[1]],[70+uip[0]*2-1,11+uip[1]]],stdscr,rolling=False)#right
            mtex=cursedtext([[uip[0],uip[1]],[19+uip[0]*2-1,11+uip[1]]],stdscr,rolling=False)#middle
            pos=[pGear[0],0]

            def geardex(index):
                assert -1<index<4
                if index==0:
                    return FRAMES
                elif index==3:
                    return ARMORS
                else:
                    return WEAPONS

            def keydex(dic,index):
                return list(dic.keys())[index]

            def render():
                rtex.text=["" for i in rtex.text]

                eq={}
                name=""
                names=[keydex(geardex(g),pGear[g]) for g in range(4)]
                if pos[1]==0:
                    eq = FRAMES[names[0]],
                elif pos[1]==3:
                    eq = ARMORS[names[3]],
                else:
                    eq = WEAPONS[names[pos[1]]],
                eq=eq[0]

                i=1
                for k in list(eq.keys()):
                    data=str(eq[k])
                    chunks=data.split(" ")
                    nc=[""]
                    for chunk in chunks:
                        if len(nc[-1])+len(chunk)<42:
                            nc[-1]+=" "+chunk
                        else:
                            nc.append(chunk)
                    nc[0]=nc[0][1:]

                    for l in range(len(nc)):
                        rtex.text[i]=int(l==0)*(k+": ")+nc[l]
                        i+=1

                for l in range(len(names)):
                    if l==pos[1]:

                        mtex.text[l+1]="-"+names[l]+"-"
                    else:
                        mtex.text[l+1]=names[l]
                rtex.push()
                mtex.push()

            # stdscr.clear()
            mtex.text[0]="EQUIPMENT"
            mtex.text[-2]="Arrow keys to swap gear"
            mtex.text[-1]="Press enter to confirm loadout"
            render()
            while True:
                key=stdscr.getkey()
                if key=="KEY_LEFT" and pos[0]>0:
                    pos[0]-=1
                elif key=="KEY_RIGHT" and pos[0]+1<len(geardex(pos[1]).keys()):
                    pos[0]+=1
                elif key=="KEY_UP" and pos[1]>0:
                    pos[1]-=1
                    pos[0]=pGear[pos[1]]
                elif key=="KEY_DOWN" and pos[1]<3:
                    pos[1]+=1
                    pos[0]=pGear[pos[1]]
                elif key=="\n":
                    break
                pGear[pos[1]]=pos[0]
                render()

        def play_menu(ctex):
            options=[
                "Duel",
                "Extraction",
                "Squad combat",
                "Warfare",
                "Hunted",
                "Exit",
            ]
            selected=0
            last=len(options)-1
            level=None
            cg=None
            units={}
            def func(unit_list):
                for unit in unit_list:
                    if unit.kind=="enemy":
                        return False
                return True
            while True:
                ctex.text=mapl(options)
                ctex.text[selected]="-"+ctex.text[selected]+"-"
                stdscr.clear()
                ctex.push()
                key=stdscr.getkey()
                if key in ["KEY_UP","w"] and selected>0:
                    selected-=1
                elif key in ["KEY_DOWN","s"] and selected<last:
                    selected+=1
                elif key=="\n":
                    enemies=0
                    minpd=4
                    maxpd=10
                    pp=[3,3]
                    allies=0
                    size=[0,0]
                    key="null"
                    tex="ELIMINATE ALL ENEMIES"
                    if selected==last:
                        return
                    if selected==0:#duel
                        enemies=1
                        minpd=1
                        size=(2,2)
                        tex="ELIMINATE THE ENEMY"
                    if selected==1:#extraction
                        allies=2
                        enemies=27
                        minpd=6
                        size=(7,2)
                        tex="GO TO THE EXTRACTION POINT"
                    elif selected==2:#squad combat
                        allies=4
                        enemies=5
                        minpd=10
                        maxpd=7
                        size=(4,4)
                    elif selected==3:#warfare
                        allies=29
                        enemies=30
                        minpd=5
                        maxpd=100
                        size=(7,7)
                    elif selected==4:#hunted
                        enemies=45
                        minpd=6
                        size=(6,6)
                        def func(unit_list):
                            return len(unit_list)==1 and unit_list[0].kind=="player"

                    level=genBoard(size[0],size[1],wallCell="#")

                    raw_size=(size[0]*7,size[1]*7)
                    cg = cursedgrid([[0,0],mapl(raw_size)],stdscr,defaultCell=".")
                    for y in range(len(level)):
                        for x in range(len(level[y])):
                            cg.grid[y][x][0]=level[y][x]
                    cg.repRange(([1,1],[4,4]))

                    def cangf(x,y):
                        if cg.grid[y][x][0]=="." and (not vec2(x,y) in [unit.pos for unit in units]):
                            return True
                        return False
                    units=spawnEnemies(([0,0],[raw_size[0]-1,raw_size[1]-1]),enemies,cangf,cg.grid,minPlayerDist=minpd,playerPos=pp)
                    units+=spawnAllies(([0,0],[raw_size[0]-1,raw_size[1]-1]),allies,cangf,cg.grid,maxPlayerDist=maxpd,playerPos=pp,bad=[unit.pos for unit in units])

                    nameOverride={}
                    if selected==1:#extraction
                        pos=get_free_loc(([0,0],[raw_size[0]-1,raw_size[1]-1]),cg.grid,cangf,playerPos=pp,dist_range=[40,inf()],bad=[unit.pos for unit in units])
                        def func(unit_list,saved=pos):
                            for unit in unit_list:
                                if unit.kind=="player":
                                    if unit.pos==saved:
                                        return True
                                    return False

                        cg.grid[pos[1]][pos[0]][1]=6
                        nameOverride[str(vec2(pos))]="extraction point"

                    elif selected==0:#duel
                        units[0].aimode="assault"

                    stdscr.clear()
                    core(level,units,cg,func,tex,nameOverrides=nameOverride)

                elif key=="q":
                    return

        def menu():
            ctex=cursedtext([[uip[0],uip[1]+3],[300+uip[0],50+uip[1]]],stdscr,rolling=False)
            options=[
                "BLACK CORE",
                "Play",
                "Equipment",
                "Tutorial",
                "Options",
                "Credits",
                "Exit",
            ]
            selected=0
            while True:
                ctex.text=mapl(options)
                ctex.text[selected]="-"+ctex.text[selected]+"-"
                stdscr.clear()
                ctex.push()
                key=stdscr.getkey()
                if key in ["KEY_UP","w"] and selected>0:
                    selected-=1
                elif key in ["KEY_DOWN","s"] and selected<6:
                    selected+=1
                elif key=="\n":
                    key="null"
                    if selected==0:
                        ctex.text=[]
                        for line in [
                            "ABOUT BLACK CORE",
                            "Black Core is a little turn-based text display game I made for fun, and because I wanted to make something cool.",
                            "On par with my normal game development criteria, it's meant for those who want a challenge.",
                            "Not those who get dopamine from slowly gaining power or wealth, the game gives you everything you need to finish it.",
                            "And the only reward for doing so is knowing you did it.",
                            "It's that YOU, through your work and time, beat a little game in a big world.",
                            "The entire game is played with only number, q, WASD, arrow, and enter keys. All of it.",
                            "The game itself is quite simple: Choose equipment, then venture out into a randomized map with enemies do destroy in it.",
                            "There might be many more enemies than players, but the player moves much quicker than the enemies.",
                            "Every action in the game takes time, so if you're quick you might be able to attack the enemy then run away before it can do anything, and vice versa for a slow unit.",
                            "On the more technical side of things, I very much had fun with pathfinding for the first time - although not so much with good AI, and I'll admit I've reworked the math functions many, many times to get them to work correctly.",
                            "I hope you enjoy it."]:
                            chunks=line.split(" ")
                            nc=[""]
                            for chunk in chunks:
                                if len(nc[-1])+len(chunk)<70:
                                    nc[-1]+=" "+chunk
                                else:
                                    nc.append(chunk)
                            # nc[0]=nc[0][1:]
                            for l in range(len(nc)):
                                ctex.text.append(nc[l])
                            ctex.text.append("")
                        stdscr.clear()
                        ctex.push()
                        while not key in ["\n","q"]:
                            key=stdscr.getkey()
                    elif selected==1:
                        stdscr.clear()
                        play_menu(ctex)
                    elif selected==2:
                        stdscr.clear()
                        gear()
                    elif selected==3:
                        ctex.text=["Keybinds:",
                            "   w,a,s,d : cursor up,left,down,right",
                            "   up,left,down,right arrow keys : camera up,left,down,right",
                            "   m : select movement",
                            "   1 : select first weapon for firing",
                            "   2 : select second weapon for firing",
                            "   q : exit selection modes (from keys m,1, and 2) or exit game",
                            "   enter : confirm selection to fire or move",
                            "Game basics:",
                            "  The player is green with an \"o\" icon.",
                            "  When you select an action to do, several grid squares will turn white.",
                            "  These are the acceptable areas to preform actions.",
                            "  The cursor will always start on the position of the player,",
                            "and will have an \"O\" or \"X\" displayed.",
                            "  Enemies are \"*\" icons. They will shoot at the player.",
                            "  Allies are \"+\" and will (try) to shoot enemies. You can still shoot at them though."
                            "  # are walls. Do not try to break a wall. They do not break.",
                        ]
                        stdscr.clear()
                        ctex.push()
                        while not key in ["\n","q"]:
                            key=stdscr.getkey()
                    elif selected==4:
                        ctex.text=["Options Menu","","...What options would I put in this kind of game?","","You can go back now."]
                        stdscr.clear()
                        ctex.push()
                        while not key in ["\n","q"]:
                            key=stdscr.getkey()
                    elif selected==5:
                        ctex.text=["Credits","","100% Coded by me.","Uses:","-Curses, a python ascii display library","-PyInstaller, a python-to-exe command line tool","-Sheer will, to finish the despicable AI system."]
                        stdscr.clear()
                        ctex.push()
                        while not key in ["\n","q"]:
                            key=stdscr.getkey()
                    elif selected==6:
                        exit()
                elif key=="q":
                    exit()

        menu()

    curses.wrapper(main)
    print("LOG")
    print(open(os.getcwd()+"/output.txt","r").read())
    print("END LOG")
