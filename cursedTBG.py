try:
    from gridView import *
    from gridClasses import *
    from equipment import *
    from gridGeo import *
    from levelGen import *
    from time import sleep
    import os
except Exception as e:
    filePrint("Import fail: {}".format(e))

try:
    open(os.getcwd()+"/compiling_notes.txt","r").close()
    print("Running from file, will not clear log")
except:
    print("Running from exe, clearing log")
    with open(os.getcwd()+"/output.txt","w") as file:
        file.write("")

sleep(.5)

if __name__ == "__main__":
    filePrint("______NEW______")
    def main(stdscr):
        curses.start_color()
        curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_GREEN)
        curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_RED)
        curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_CYAN)

        curses.noecho()#terminal doesn't get keypresses
        curses.cbreak()#take keypresses
        curses.curs_set(0)# Hide the cursor
        stdscr.keypad(True)#make arrow keys not be escape sequences

        stdscr.resize(150,150)
        uip=[4,4]#UI pos
        pGear=[0,0,1,0]

        def core():
            cg = cursedgrid([[0,0],[50,50]],stdscr,defaultCell=".")
            camsize=(10,10)
            def cam_area():
                return [[cam.pos[0],cam.pos[1]],[cam.pos[0]+cam.viewSize[0],cam.pos[1]+cam.viewSize[1]]]

            cam=cursedcam(camsize,stdscr,cg,outOffset=uip)
            ctex=cursedtext([[uip[0]*2,uip[1]+11],[200+uip[0]*2-1,14+uip[1]]],stdscr,rolling=True)#under


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
            cursorPos = vec2(player.pos[0],player.pos[1])
            units={}

            #helper funcs
            def cangf(x,y):
                if cg.grid[y][x][0]=="." or str(vec2(x,y)) in list(units.keys()):
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

            #level generation!
            level=genBoard(50,50,wallCell="#")
            for y in range(len(level)):
                for x in range(len(level[y])):
                    cg.grid[y][x][0]=level[y][x]
            units={str(u.pos):u for u in spawnUnits(([0,0],[49,49]),50,cangf,cg.grid,minPlayerDist=4,playerPos=[3,3])}
            for k in list(units.keys()):
                units[k].displayColor=3
            cg.repRange([[1,1],[6,6]])
            units[str(player.pos)]=player

            time=0
            state=0#0: selecting 1: moving 2: shooting first weapon 3: shooting second weapon
            okays=[]

            def render(clear=True,color=1,cell=1,):
                for k in list(units.keys()):
                    un=units[k]
                    if cell==2 or (cell==1 and not str(un.pos) in list(cam.cell_overrides.keys())):
                        cam.cell_overrides[str(un.pos)]=un.displayChar
                    if color==2 or (color==1 and not str(un.pos) in list(cam.color_overrides.keys())):
                        cam.color_overrides[str(un.pos)]=un.displayColor
                ctex.push()
                cam.push()
                stdscr.refresh()
                if clear:
                    cam.cell_overrides={}
                    cam.color_overrides={}

            render()

            instructions=[
                "PLAYER INITIALIZED",
                "Keybinds:",
                "   w,a,s,d : cursor up,left,down,right",
                "   up,left,down,right arrow keys : camera up,left,down,right",
                "   m : select movement",
                "   1 : select first weapon for firing",
                "   2 : select second weapon for firing",
                "   q : exit selection modes (from keys m,1, and 2) or exit game",
                "   enter : confirm selection to fire or move",
                "Game basics:",
                "The player is green with an \"o\" icon.",
                "When you select an action to do, several grid squares will turn white.",
                "These are the acceptable areas to preform actions.",
                "The cursor will always start on the position of the player, and will have an \"O\" or \"X\" displayed.",
                "Enemies are \"*\" icons. They will shoot at the player.",
                "# are walls. Do not try to break a wall. They do not break.",
                "ELIMINATE ALL ENEMIES",
            ]
            for i in instructions:
                ctex.addText(i)
                render()
                sleep(.7+len(i)/80)#bigger ones give longer time to read

            ctex.addText("GAME START")

            render()
            try:
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
                        if state!=0:
                            cursorPos=[mapl(player.pos)[i]-mapl(cam.pos)[i] for i in range(2)]

                    if key=="\n" and state!=0:
                        cusp=wcp()
                        # filePrint(okays)
                        # filePrint(cusp)
                        if cusp in okays:
                            if state==1:
                                time=player.act_time/2
                                player.wait_time=time*2#player moves twice as fast as enemies, to make it fair
                                for pos in tryPathFind(player.move_max,cangf,cg.grid,player.pos,cusp):
                                    cam.color_overrides[str(pos)]=4
                                player.pos=cusp
                                render()
                                sleep(.3)
                            elif state in [2,3]:
                                time=player.wps[state-2][2]/2#multiply acted wait time by 2 or they will be able toa ct again (wt=time,-time=0)
                                player.wait_time=time*2
                                player.wps[state-2][3]=player.wps[state-2][1]["cooldown"]/2
                                for pos in lineGrid([cusp,player.pos]):
                                    cam.color_overrides[str(pos)]=3
                                if str(cusp) in list(units.keys()):
                                    ctex.addText(units[str(cusp)].damage(player.wps[state-2][1]["damage"],player))
                                    if not units[str(cusp)].health>0:
                                        ctex.addText(units[str(cusp)].name+" was destroyed!")
                                        del units[str(cusp)]
                                        if len(units.keys())==1:#only player is left
                                            ctex.addText("OBJECTIVE COMPLETED")
                                            render()
                                            sleep(1.2)
                                            ctex.addText("GAME SHUTDOWN")
                                            render()
                                            sleep(1.5)
                                            exit()
                                render()
                                sleep(.3)
                            state=0
                            okays=[]
                        else:
                            ctex.addText("Weapon cannot shoot there")

                    if key =="q":
                        if state==0:
                            break
                        else:
                            state=0
                            cam.color_overrides={}

                    #time+ai
                    if time!=0:
                        while player.wait_time>0:
                            new={}
                            for k in list(units.keys()):
                                un=units[k]
                                cam.cell_overrides[str(un.pos)]=un.displayChar
                                cam.color_overrides[str(un.pos)]=un.displayColor
                                un.wait_time-=time
                                un.wps[0][3]-=time
                                un.wps[1][3]-=time
                                if un.wait_time<=0 and un.kind!="player":
                                    action = un.think(player,canff,cangf,cg.grid)
                                    if action[0]=="wait":
                                        time=.1
                                    elif action[0]=="fire":
                                        time=un.wps[action[1]][2]
                                        un.wait_time=un.wps[action[1]][2]*2
                                        un.wps[action[1]][3]=un.wps[action[1]][1]["cooldown"]

                                        for pos in rayCircle(un.pos,un.wps[action[1]][1]["range"],cg.grid,canff):
                                            cam.color_overrides[str(pos)]=1
                                        render()
                                        sleep(.3)
                                        for pos in lineGrid([un.pos,player.pos]):
                                            cam.color_overrides[str(pos)]=3
                                        render()
                                        ctex.addText(player.damage(un.wps[action[1]][1]["damage"],un))
                                        sleep(.3)
                                        if player.health<0:
                                            ctex.addText("PLAYER IS DEAD")
                                            render()
                                            sleep(1.2)
                                            ctex.addText("GAME SHUTDOWN")
                                            render()
                                            sleep(1.5)
                                            exit()
                                        render()
                                    elif action[0]=="move":
                                        time=un.act_time
                                        un.wait_time=time*2
                                        if between2d(un.pos,cam_area()[0],cam_area()[1]):
                                            for pos in tryPathFind(un.move_max,cangf,cg.grid,un.pos,action[1]):
                                                cam.color_overrides[str(pos)]=4
                                            un.pos=action[1]
                                            render()
                                            sleep(.3)
                                        else:
                                            un.pos=action[1]
                                            render()
                                new[str(un.pos)]=un
                            units = new

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
                        render(cell=0,color=2)

                    else:
                        render()
            except Exception as e:
                filePrint("units:")
                filePrint(units)
                filePrint("\n".join([str(vars(units[k])) for k in list(units.keys())]))
                filePrint("cam: "+str(vars(cam)))
                filePrint("grid: "+str(vars(cam)))
                filePrint("bottom texbox: "+str(vars(ctex)))
                filePrint("cursor info:")
                filePrint(["pos(loc,world):",cursorPos,wcp()])
                filePrint("state: "+str(state))
                filePrint("okays: "+str(okays))
                filePrint("Core fail: {}".format(e))

        def gear():
            try:
            # if True:
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
            except Exception as e:
                filePrint("rtex: "+str(vars(rtex)))
                filePrint("mtex: "+str(vars(mtex)))
                filePrint("pos: "+str(pos))
                filePrint("pGear: "+str(pGear))
                filePrint("Gear fail: {}".format(e))

        def menu():
            ctex=cursedtext([[uip[0],uip[1]+3],[200+uip[0],20+uip[1]]],stdscr,rolling=False)
            options=[
                "BLACK CORE",
                "Play",
                "Equipment",
                "Options",
                "Credits",
                "Exit",
            ]
            selected=0
            try:
                while True:
                    ctex.text=mapl(options)
                    ctex.text[selected]="-"+ctex.text[selected]+"-"
                    stdscr.clear()
                    ctex.push()
                    key=stdscr.getkey()
                    if key in ["KEY_UP","w"] and selected>0:
                        selected-=1
                    elif key in ["KEY_DOWN","s"] and selected<5:
                        selected+=1
                    elif key=="\n":
                        key="null"
                        if selected==0:
                            ctex.text=["ABOUT BLACK CORE","","  This is a game I made.","I like text-based visuals,","and turn-based games,","and I had fun making this.","So I hope you have fun playing."]
                            stdscr.clear()
                            ctex.push()
                            while not key in ["\n","q"]:
                                key=stdscr.getkey()
                        elif selected==1:
                            stdscr.clear()
                            core()
                        elif selected==2:
                            stdscr.clear()
                            gear()
                        elif selected==3:
                            ctex.text=["Options Menu","","...What options would I put in this kind of game?","","You can go back now."]
                            stdscr.clear()
                            ctex.push()
                            while not key in ["\n","q"]:
                                key=stdscr.getkey()
                        elif selected==4:
                            ctex.text=["Credits","","100% Coded by me.","Uses:","-Curses, a python ascii display library","-PyInstaller, a python-to-exe command line tool","-Sheer will, to finish the despicable AI system."]
                            stdscr.clear()
                            ctex.push()
                            while not key in ["\n","q"]:
                                key=stdscr.getkey()
                        elif selected==5:
                            exit()
                    elif key=="q":
                        exit()
            except Exception as e:
                filePrint("options: {}".format(options))
                filePrint("selected: {}".format(selected))
                filePrint("ctex: "+str(vars(ctx)))
                filePrint("Menu fail: {}".format(e))

        menu()

    curses.wrapper(main)
    print("LOG")
    print(open(os.getcwd()+"/output.txt","r").read())
    print("END LOG")
