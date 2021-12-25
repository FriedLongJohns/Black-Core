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

sleep(1)

if __name__ == "__main__":
    filePrint("______NEW______")
    def main(stdscr):
        try:
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
            cg = cursedgrid([[0,0],[50,50]],stdscr,defaultCell=".")#to make things square
            camsize=(10,10)
            def cam_area():
                return [[cam.pos[0],cam.pos[1]],[cam.pos[0]+cam.viewSize[0],cam.pos[1]+cam.viewSize[1]]]

            uip=[4,4]#UI pos
            cam=cursedcam(camsize,stdscr,cg,outOffset=uip)
            ctex=cursedtext([[uip[0]*2,uip[1]+11],[200+uip[0]*2-1,14+uip[1]]],stdscr,rolling=True)#under
            ptex=cursedtext([[21+uip[0]*2,uip[1]],[50+uip[0]*2-1,11+uip[1]]],stdscr,rolling=False)#right


            #unit and unit func setup
            player = Unit([3,3],"Talus",["Hammer","Burst Rifle"],"None",kind="player",displayColor=2)
            cursorPos = mapl(player.pos)
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
            ctex.addText("GAME START")

            def render(clear=True,color=1,cell=1,):
                for k in list(units.keys()):
                    un=units[k]
                    if cell==2 or (cell==1 and not str(un.pos) in list(cam.cell_overrides.keys())):
                        cam.cell_overrides[str(un.pos)]=un.displayChar
                    if color==2 or (color==1 and not str(un.pos) in list(cam.color_overrides.keys())):
                        cam.color_overrides[str(un.pos)]=un.displayColor
                ptex.push()
                ctex.push()
                cam.push()
                stdscr.refresh()
                if clear:
                    cam.cell_overrides={}
                    cam.color_overrides={}

            render()

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
            filePrint("right texbox: "+str(vars(ptex)))
            filePrint("cursor info:")
            filePrint(["pos(loc,world):",cursorPos,wcp()])
            filePrint("state: "+str(state))
            filePrint("okays: "+str(okays))
            filePrint("Main fail: {}".format(e))

    curses.wrapper(main)
    print("LOG")
    print(open(os.getcwd()+"/output.txt","r").read())
    print("END LOG")
