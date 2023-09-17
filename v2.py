import mss.tools
from PIL import Image, ImageDraw, ImageFont
import pyautogui, math, os, shutil
import numpy as np
import keyboard

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT = ImageFont.truetype("hksn_en.ttf")
SCREENSHOT_OUTPUT = "screenshot.png"

bottomRow = [
    144930,#D
    159269,#C
    173608,#B
    187946,#A
    173725,#B
    159504,#C
    145282,#D
]

topRow = [
    59670,#1
    45448,#2
    31227,#3
    17006,#4
    31345,#5
    45683,#6
    60022 #7
]

solDict = {
    '173608 173725 ': [17006, 60022], #B 47
    '159269 159504 187946 ': [31345, 45683], #AC 56 
    '159269 159504 173608 173725 187946 ': [45448, 17006, 31345, 60022], #ABC 2457
    '144930 145282 187946 ': [17006, 45683], #AD 46
    '144930 145282 173608 173725 187946 ': [17006], #ABD 4 
    '144930 145282 159269 159504 ': [31345, 45683, 60022], #CD 567
    '144930 145282 159269 159504 173608 173725 ': [31227, 17006, 45683] #BCD 346
}

"""
if os.path.exists("images"):
    shutil.rmtree("images")
os.mkdir("images")
"""

def screenshot():
    with mss.mss() as sct:
        # 1230 1650 390 865
        monitor = {"top": 390, "left": 1230, "width": 420, "height": 475}
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=SCREENSHOT_OUTPUT)

def find2DCoord(coords, im):
    width = im.size[0]
    x = coords%width or width
    y = math.floor(coords/width)
    return x, y

def find1DCoordAndOffset(x, y, im, offsetY):
    width = im.size[0]
    return (y+offsetY)*width+x

def drawing(x, y, colour, text, im):
    ImageDraw.Draw(im).rectangle(((x, y), (x, y)), fill=colour)
    ImageDraw.Draw(im).text((x,y), text, WHITE, FONT)
    return im

def findInARow(listInput, times):
    for i in range(times):
        G = (listInput[i] for i,val in enumerate(np.diff(listInput)) if val == 1)
        listInput = list(G)
    return listInput

def findPoints():

    with Image.open(SCREENSHOT_OUTPUT) as im:
        imageList = list(im.getdata())
        enumList = enumerate(imageList)

        pixelGen = (i for i,val in enumList if val == WHITE)
        
        pointsToClick = findInARow(list(pixelGen), 6)
        notBottom = (i for i in pointsToClick if not i in bottomRow)
        notBottomList = list(notBottom)
        
        if len(pointsToClick) == 0:
            return 0, 0, [], pointsToClick
        if len(notBottomList) == 0:
            key = "".join(str(e)+" " for e in pointsToClick)
            print(key)
            if not key in solDict:
                raise Exception("solution not found")
            for i in solDict[key]:
                tempX, tempY = find2DCoord(i, im)
                pyautogui.click(tempX+1230, tempY+390)
            screenshot()
            return findPoints()
        
        x, y = find2DCoord(notBottomList[0], im)
        with open("image1.txt", "a") as fWrite:
            pointText = "point {},{}\n".format(x, y)
            print(pointText)
            fWrite.write(pointText)

        #newIm = drawing(x, y, GREEN, "point", im)
        #newIm.save("images/{}-{}.png".format(time.monotonic(),len(notBottomList)))

        return x, y, notBottomList, pointsToClick
    
def drawOnAllPoints():

    with Image.open(SCREENSHOT_OUTPUT) as im:
        imageList = list(im.getdata())
        enumList = enumerate(imageList)

        pixelGen = (i for i,val in enumList if val == WHITE)
        
        pointsToClick = findInARow(list(pixelGen), 6)
        notBottom = (i for i in pointsToClick if not i in bottomRow)
        notBottomList = list(notBottom)
        
        for i,val in enumerate(notBottomList):
            value = notBottomList[i]
            xCoord, yCoord = find2DCoord(value, im)
            newIm = drawing(xCoord, yCoord, GREEN, "{}".format(i), im)
            print("{}: {} ({},{})".format(i,val,xCoord,yCoord))
        newIm.save("images/all points.png")


xCoord = yCoord = 0
clickCount = 0
pointsLeft = []
debug = []


with open("image1.txt", "w") as fWrite:
    fWrite.write("")

while 1:

    if keyboard.is_pressed("d"):
        break

    screenshot()
    """
    drawOnAllPoints()
    break
    """
    xCoord, yCoord, pointsLeft, debug = findPoints()

    if len(pointsLeft) < 1:
        pyautogui.click(1419,945)
        
    pyautogui.click(xCoord+1230, yCoord+390+68)
    clickCount += 1
    #clickText = "click {}th {}, {}\n".format(clickCount, xCoord, yCoord+68)
    #print(clickText)
    #print(len(pointsLeft), pointsLeft[0])

for i,val in enumerate(pointsLeft):
    print("{}: {}".format(i,val))
for i,val in enumerate(debug):
    print("{}: {}".format(i,val))
print(debug)

