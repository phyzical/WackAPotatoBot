from os import listdir
from os.path import basename
import cv2
import numpy as np
import pyautogui
import time
import mss
from datetime import datetime

imageDir = 'images'
debug = False
debugTime = False

enableAutoDeconstruction = True

baseX = 0
baseY = 40
extraWidth = 1600
extraHeight = 870

gameboardWidth = 590
gameboardHeight = 580
gameboardBaseX = 235
gameboardBaseY = 180

refImages = [imageDir+"/" + s for s in listdir(imageDir)]


def initiliseImages(imageFile):
    imageFileName = basename(imageFile).split(".", 1)[0]
    image = cv2.imread(imageFile)
    return {"image": image, "type": imageFileName}


imageTypes = list(map(initiliseImages, refImages))


def findImages(types, gameboard=False):
    # part of the screen
    totalTime = 0
    if debugTime:
        start = time.time()
    with mss.mss() as sct:
        bbox = (baseX, baseY,  baseX + extraWidth,  baseY + extraHeight)
        if gameboard:
            bbox = (gameboardBaseX, gameboardBaseY,  gameboardBaseX +
                    gameboardWidth,  gameboardBaseY + gameboardHeight)
        img_scr = sct.grab(bbox)
    if debugTime:
        end = time.time()
        print("time taken for imagegrab: " + str(end - start))
        totalTime += end - start

    if debugTime:
        start = time.time()
    img_rgb = cv2.cvtColor(np.array(img_scr), cv2.COLOR_BGRA2BGR)
    if debugTime:
        end = time.time()
        print("time taken for convert: " + str(end - start))
        totalTime += end - start

    if debug:
        mss.tools.to_png(img_scr.rgb, img_scr.size,
                         output="tests/screenshot.png")
    for tileType in findRefImageByTypes(types):
        typeImage = tileType["image"]
        type = tileType["type"]
        w, h = typeImage.shape[:-1]
        if debug:
            mss.tools.to_png(img_scr.rgb, img_scr.size,
                             output="tests/screenshot-"+type+".png")
        if debugTime:
            start = time.time()
        res = cv2.matchTemplate(img_rgb, typeImage, cv2.TM_CCOEFF_NORMED)
        if debugTime:
            end = time.time()
            print("time taken for match: " + str(end - start))
            totalTime += end - start

        threshold = .75
        if debugTime:
            start = time.time()
        loc = np.where(res >= threshold)
        if debugTime:
            end = time.time()
            print("time taken for np: " + str(end - start))
            totalTime += end - start
        matches = list(zip(*loc[::-1]))
        if len(matches) > 0:
            pt = matches[0]  # Switch collmns and rows
            # xy of center point for moving
            x = pt[0] + (w/2)
            y = pt[1] + (h/2)
            tile = {"x": x, "y": y}
            if debug:
                print("Found " + type)
                print(tile)
                cv2.rectangle(img_rgb, pt,
                              (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                cv2.putText(img_rgb, type,
                            (pt[0] + w, pt[1] + h),  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.imwrite('tests/result-' +
                            datetime.now().strftime('%H:%M:%S')+'.png', img_rgb)
            if debugTime:
                print("total time taken to match: " + str(totalTime))
            return tile
    if debugTime:
        print("total time taken to match: " + str(totalTime))


def findRefImageByTypes(types):
    return [image for image in imageTypes if image['type'] in types]


def findAndClick(types, gameboard=False, clickOffsetX=0, clickOffsetY=15):
    image = findImages(types, gameboard)
    if image:
        x = image['x'] + baseX + clickOffsetX
        y = image['y'] + baseY + clickOffsetY
        pyautogui.click(x, y)


def startGame():
    print("Starting game")
    findAndClick(["start"], False, 0, -baseY)
    i = 2
    running = True
    while running:
        findAndClick(["green", "yellow"], True, gameboardBaseX, gameboardBaseY)
        i = i + 1
        if i % 100 == 0:
            print("checking if the game finished")
            timer = findImages(["timer"])
            if timer:
                running = False


def destroyInventory():
    print("Destorying equipment")
    findAndClick(["exit-icon"], False, 0, -baseY)
    findAndClick(["inventory"])
    findAndClick(["destroy-inventory"])
    findAndClick(["tick"])
    findAndClick(["home-icon"])
    findAndClick(["open-icon", "open-icon-cooldown"])


def start():
    findAndClick(["open-icon", "open-icon-cooldown"])
    while True:
        startText = findImages(["start-text"])
        if startText:
            startGame()
        if enableAutoDeconstruction:
            destroyInventory()

        print("Sleeping for 5 minutes")
        time.sleep(60*5)


start()
