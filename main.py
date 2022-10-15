import pyscreenshot as ImageGrab
from os import listdir
from os.path import basename
import cv2
import numpy as np
from functools import reduce
import pyautogui
import time
import random

imageDir = 'images'

def filterFiles(file):
    return file != "{imageDir}/.DS_Store"


images = filter(
    filterFiles, ["{imageDir}/" + s for s in listdir("{imageDir}")])


def initiliseImages(imageFile):
    imageFileName = basename(imageFile).split(".", 1)[0]
    image = cv2.imread(imageFile)
    # # convert the images to grayscale
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return {"image": image, "type": imageFileName}


imageTypes = list(map(initiliseImages, imageDir))
baseWindowX = 100

baseX = 300
baseY = 200


def doClick(groupedPotatoes):
    for tile in groupedPotatoes:
        x = (tile['x'] + baseX)/2
        y = (tile['y'] + baseY)/2
        print(
            f"clicking tile at x{x} y{y}")
        pyautogui.click(x, y)
        pyautogui.click(x, y)


# def removeDuplicates(list, item):
#     unique = 1
#     errorVariancePixels = 10
#     for listItem in list:
#         unique = unique and (
#             abs(listItem["x"] - item["x"]) > errorVariancePixels or abs(listItem["y"] - item["y"]) > errorVariancePixels)
#     if unique == 1:
#         list.append(item)
#     return list


def findPotatoes():
    # part of the screen
    screenshot = ImageGrab.grab(
        bbox=(baseX, baseY, baseX+1920, baseY + 1000))  # X1,Y1,X2,Y2
    screenshot.save("screenshot.png")
    img_rgb = cv2.imread('screenshot.png')
    # img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    groupedPotatoes = {}
    for tileType in imageTypes:
        typeImage = tileType["image"]
        type = tileType["type"]
        w, h = typeImage.shape[:-1]
        tiles = []
        res = cv2.matchTemplate(img_rgb, typeImage, cv2.TM_CCOEFF_NORMED)
        threshold = .65
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):  # Switch collmns and rows
            # xy of center point for moving
            x = pt[0] + (w/2)
            y = pt[1] + (h/2)
            tiles.append({"x": x, "y": y, "pt": pt})

        # groupedPotatoes[type] = reduce(removeDuplicates, tiles, [])
        for tile in groupedPotatoes[type]:
            pt = tile["pt"]
            cv2.rectangle(img_rgb, pt,
                          (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            cv2.putText(img_rgb, type,
                        (pt[0] + w, pt[1] + h),  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imwrite('result.png', img_rgb)

    return groupedPotatoes


def clickPotatoes(potatoes):
    if len(potatoes):
        for type in potatoes:
            # x = (tile['x'] + baseX)/2
            # y = (tile['y'] + baseY)/2
            potato = potatoes[type][0]
            pyautogui.click(potato['x'], potato['y'])

def start():
    potatoes = findPotatoes()
    print(potatoes)
    potatoes = {k: v for k, v in potatoes.items() if k == "green" or k == "yellow"}
    # clickPotatoes(potatoes)


start()
