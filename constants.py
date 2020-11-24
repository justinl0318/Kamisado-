"""constants"""

# color (tower & cell)
BROWN = 1
GREEN = 2
RED = 3
YELLOW = 4
PINK = 5
PURPLE = 6
BLUE = 7
ORANGE = 8
EMPTY = 0

# player
pwhite = 1
pblack = 2
NONE = 0

PLAYER_NAMES = ["?", "WHITE", "BLACK"]
COLOR_NAMES = ["Any", "Brown", "Green", "Red", "Yellow", "Pink", "Purple", "Blue", "Orange"]

# rgb color
COLOR_RGB = {
    BROWN: (90, 46, 17),
    GREEN: (0, 144, 87),
    RED: (209, 50, 55),
    YELLOW: (227, 194, 1),
    PINK: (209, 112, 157),
    PURPLE: (108, 53, 137),
    BLUE: (1, 106, 172),
    ORANGE: (215, 116, 33)
}

# inisialisasi colormap
COLORMAP = [[0 for i in range(8)] for j in range(8)]
for j in range(7, -1, -1):
    COLORMAP[0][j] = 8 - j
for i in range(1, 4):
    COLORMAP[i][i] = ORANGE
for i in range(7, 3, -1):
    COLORMAP[7-i][i] = BROWN
COLORMAP[2][0] = COLORMAP[1][3] = COLORMAP[3][5] = GREEN
COLORMAP[1][0] = COLORMAP[2][3] = COLORMAP[3][6] = RED
COLORMAP[1][5] = COLORMAP[2][6] = COLORMAP[3][7] = YELLOW
COLORMAP[3][0] = COLORMAP[1][2] = COLORMAP[2][1] = PINK
COLORMAP[3][1] = COLORMAP[2][4] = COLORMAP[1][7] = PURPLE
COLORMAP[3][2] = COLORMAP[1][4] = COLORMAP[2][7] = BLUE
# reverse
for i in range(4):
    for j in range(8):
        COLORMAP[7-i][7-j] = COLORMAP[i][j]


if __name__ == '__main__':
    # cek colormap
    # COLORTXT = "BGRYIULO"
    COLORTXT = ["Br", "Gn", "Rd", "Yl", "Pi", "Pu", "Bl", "Or"]
    def printcol(color, text):
        endcode = u"\u001b[0m"
        startcode = {
            BROWN: u"\u001b[48;5;130m",
            GREEN: u"\u001b[48;5;82m",
            RED: u"\u001b[48;5;196m",
            YELLOW: u"\u001b[48;5;11m",
            PINK: u"\u001b[48;5;13m",
            PURPLE: u"\u001b[48;5;55m",
            BLUE: u"\u001b[48;5;21m",
            ORANGE: u"\u001b[48;5;208m"
        }
        return "{}{}{}".format(startcode.get(color, u"\u001b[38;5;255m"), text, endcode)

    for i in range(8):
        for j in range(8):
            print(printcol(COLORMAP[i][j], COLORTXT[COLORMAP[i][j]-1]), end="")
        print()
