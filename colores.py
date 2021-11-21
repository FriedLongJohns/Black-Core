import curses
#1:black, 2:red, 3:green, 4:yellow, 5:blue, 6:magenta, 7:cyan, and 8:white
tcolors = []
ccolors = [curses.COLOR_BLACK]
def setPair(num,color1,color2):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)