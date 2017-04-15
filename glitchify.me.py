# ..:glitchify.me v0.0 #
# Gustavo Santiago #
import cv2
import numpy as np

# DEFINES #
# ---------------------------------------------------------------------------- #
DEBUG = 1
SPLASH = " ..:glitchify.me v0.0 "

R = 0
G = 1
B = 2
NOISE_GRAY = 0
NOISE_RGB = 1
DEAD_BLACK = 0
DEAD_WHITE = 1
# ---------------------------------------------------------------------------- #

# FUNCTIONS #
# ---------------------------------------------------------------------------- #
def displacement(src, seed, axis, spread):
    if src is None:
        return None

    height, width = src.shape[:2]
    out = np.zeros((height, width, 3), np.uint8)

    out = np.copy(src)

    if axis == 0:
        for i in range(0, height, spread):
            tmp = np.random.randint(0, seed)
            for j in range(0, width):
                if j - tmp >= 0:
                    out[i][j] = src[i][j - tmp]
                else:
                    out[i][j] = src[i][0]
    elif axis == 1:
        for j in range(0, width, spread):
            tmp = np.random.randint(0, seed)
            for i in range(0, height):
                if i - tmp >= 0:
                    out[i][j] = src[i - tmp][j]
                else:
                    out[i][j] = src[0][j]

    return out

def deadPixels(src, seed, col):
    if src is None:
        return None

    height, width = src.shape[:2]
    if(seed > width - 1 or seed > height - 1):
        return src

    out = np.zeros((height, width, 3), np.uint8)

    out = np.copy(src)

    for i in range(0, height, np.random.randint(1, seed)):
        for j in range(0, width, np.random.randint(1, seed)):
            if(col == DEAD_BLACK):
                out[i][j] = src[i][j] * np.random.randint(0, 2)
            elif(col == DEAD_WHITE):
                out[i][j] = -src[i][j] * np.random.randint(0, 2)

    return out

def noiseLayer(src, seed, type):
    if src is None:
        return None

    height, width = src.shape[:2]
    out = np.zeros((height, width, 3), np.float32)

    for i in range(height):
        for j in range(width):
            if type == NOISE_GRAY:
                out[i][j] = src[i][j] + np.float32(np.random.randint(-seed, seed))
            elif type == NOISE_RGB:
                for k in range(3):
                    out[i][j][k] = src[i][j][k] + np.float32(np.random.randint(-seed, seed))

    out = np.clip(out, 0, 255).astype(np.uint8)
    return out

def shiftRGB(src, x, y, col):
    if src is None:
        return None

    height, width = src.shape[:2]
    if col < 0 or col > 2 or x < 0 or y < 0 or x >= width or y >= height:
        return src

    out = np.zeros((height, width, 3), np.uint8)

    for i in range(y, height):
        for j in range(x, width):
            out[i-y][j-x][col] = src[i][j][col]

    others = list(np.array([0, 1, 2]))
    others.remove(col)
    for i in range(height):
        for j in range(width):
            for k in others:
                out[i][j][k] = src[i][j][k]

    return out

def writeImage(src):
    oname = input(">Type in the output filename: ")
    cv2.imwrite(oname, src)
    print(">\"" + oname + "\" successfully written :3")

def showImage(src):
    cv2.imshow("glitchify.me", src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# TODO
def pixelSort(src, axis):
    # vaporsomething

# ---------------------------------------------------------------------------- #

# HANDLERS #
# ---------------------------------------------------------------------------- #
def makeDisplacement(src):
    print("\n>DISPLACEMENT")
    seed = input(">Type in the seed value: ")
    seed = int(seed)

    axis = input(">Type the axis [X/Y]: ")
    if(axis.upper() == "X" or axis == "0"): axis = 0
    elif(axis.upper() == "Y" or axis == "1"): axis = 1
    else: axis = 0

    spread = input(">Type the spread value: ")
    spread = int(spread)

    return displacement(src, seed, axis, spread)

def makeDeadPixels(src):
    print("\n>DEAD PIXELS")
    seed = input(">Type in the seed value: ")
    seed = int(seed)

    dtype = input(">Type the dead pixel type [Black/White]: ")
    if(dtype.upper() == "B" or dtype == "0"): dtype = DEAD_BLACK
    elif(dtype.upper() == "W" or dtype == "1"): dtype = DEAD_WHITE
    else: dtype = DEAD_BLACK

    return deadPixels(src, seed, dtype)

def makeNoiseLayer(src):
    print("\n>NOISE LAYER")
    seed = input(">Type in the seed value: ")
    seed = int(seed)

    ntype = input(">Type the noise type [Grayscale/RGB]: ")
    if(ntype.upper() == "G" or ntype == "0"): ntype = NOISE_GRAY
    elif(ntype.upper() == "R" or ntype == "1"): ntype = NOISE_RGB
    else: ntype = NOISE_GRAY

    return noiseLayer(src, seed, ntype)

def makeShiftRGB(src):
    print("\n>SHIFT RGB")
    col = input(">Type in the color to be shifted [R/G/B]: ")
    if(col.upper() == "R" or col == "0"): col = R
    elif(col.upper() == "G" or col == "1"): col = G
    elif(col.upper() == "B" or col == "2"): col = B
    else: col = R

    x = input(">Type in the X shift: ")
    x = int(x)
    y = input(">Type in the Y shift: ")
    y = int(y)
    return shiftRGB(src, x, y, col)

def makeRandom(src):
    out = np.copy(src)

    its = np.random.randint(0, 10)
    for i in range(its):
        nextg = np.random.randint(1, 5)
        if(nextg == 1):
            x = np.random.randint(0, 7)
            y = np.random.randint(0, 7)
            col = np.random.randint(0, 3)
            out = shiftRGB(out, x, y, col)
        elif(nextg == 2):
            seed = np.random.randint(2, 50)
            ntype = np.random.randint(0, 2)
            out = noiseLayer(out, seed, ntype)
        elif(nextg == 3):
            seed = np.random.randint(2, 100)
            col = np.random.randint(0, 2)
            out = deadPixels(out, seed, col)
        elif(nextg == 4):
            seed = np.random.randint(2, 70)
            axis = np.random.randint(0, 2)
            spread = np.random.randint(0, 100)
            out = displacement(out, seed, axis, spread)

    return out
# ---------------------------------------------------------------------------- #

# MENUS #
# ---------------------------------------------------------------------------- #
def glitchMenu(src):
    print("\n>GLITCHES")
    print("[1] Shift RGB")
    print("[2] Noise Layer")
    print("[3] Dead Pixels")
    print("[4] Displacement")
    print("[5] Random glitches")

    op = 0
    while(op != "1" and op != "2" and op != "3" and op != "4" and op != "5"):
        op = input()
    op = int(op)
    if(op == 1):
        return makeShiftRGB(src)
    elif(op == 2):
        return makeNoiseLayer(src)
    elif(op == 3):
        return makeDeadPixels(src)
    elif(op == 4):
        return makeDisplacement(src)
    elif(op == 5):
        return makeRandom(src)

def mainMenu(src, fname):
    modified = 0
    out = np.copy(src)

    op = 0
    while(op != 4):
        print("\n")
        print(SPLASH)
        if(modified == 0):
            print(">Current file: \"" + fname + "\"")
        else:
            print(">Current file: \"" + fname + "\"[modified]")

        print("[1] Apply glitch")
        print("[2] Show image")
        print("[3] Save image")
        print("[4] Quit")

        while(op != "1" and op != "2" and op != "3" and op != "4"):
            op = input()
        op = int(op)
        if(op == 1):
            if(modified == 0):
                out = glitchMenu(src)
            else:
                out = glitchMenu(out)
            modified = 1
        elif(op == 2):
            showImage(out)
        elif(op == 3):
            writeImage(out)
        op == 0

def openMenu():
    fname = input(">Type in the file name: ")

    if(DEBUG): print(">Opening file \"" + fname + "\"...")
    src = cv2.imread(fname, cv2.IMREAD_UNCHANGED)

    if(src is not None):
        print("\"" + fname + "\" successfully opened :3")
        mainMenu(src, fname)
    else:
        print("\"" + fname + "\" could not be opened :(")

def startMenu():
    print("[1] Open file")
    print("[2] Quit")

    op = 0
    while(op != "1" and op != "2"):
        op = input()
    op = int(op)
    if(op == 1):
        openMenu()
# ---------------------------------------------------------------------------- #

# MAIN #
# ---------------------------------------------------------------------------- #
print(SPLASH)
startMenu()
print(">Closing program...")
# ---------------------------------------------------------------------------- #
