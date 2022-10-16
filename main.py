from os import listdir
from os.path import basename
import cv2
import numpy as np
from functools import reduce
import pyautogui
import time
import random
import mss

imageDir = 'images'
debug = True
baseX = 130
baseY = 40
extraWidth = 900
extraHeight = 850


def filterFiles(file):
    return file != imageDir+"/.DS_Store"


refImages = filter(
    filterFiles, [imageDir+"/" + s for s in listdir(imageDir)])


def initiliseImages(imageFile):
    imageFileName = basename(imageFile).split(".", 1)[0]
    image = cv2.imread(imageFile)
    # # convert the images to grayscale
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return {"image": image, "type": imageFileName}


imageTypes = list(map(initiliseImages, refImages))


def removeDuplicates(list, item):
    unique = 1
    errorVariancePixels = 10
    for listItem in list:
        unique = unique and (
            abs(listItem["x"] - item["x"]) > errorVariancePixels or abs(listItem["y"] - item["y"]) > errorVariancePixels)
    if unique == 1:
        list.append(item)
    return list


def findImages(i, types):
    # part of the screen
    totalTime = 0
    if debug:
        start = time.time()
    with mss.mss() as sct:
        img_rgb = sct.grab(
            (baseX, baseY, baseX+extraWidth, baseY + extraHeight))
    if debug:
        end = time.time()
        print("time taken for imagegrab: " + str(end - start))
        totalTime += end - start

    if debug:
        start = time.time()
        mss.tools.to_png(img_rgb.rgb, img_rgb.size,
                         output="tests/screenshot.png")
    if debug:
        end = time.time()
        print("time taken for save: " + str(end - start))
        totalTime += end - start
    img_rgb = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_BGRA2BGR)
    if debug:
        start = time.time()

    if debug:
        end = time.time()
        print("time taken for read: " + str(end - start))
        totalTime += end - start

    groupedImages = {}
    for tileType in findRefImageByTypes(types):
        typeImage = tileType["image"]
        type = tileType["type"]
        w, h = typeImage.shape[:-1]
        tiles = []
        if debug:
            start = time.time()
        res = cv2.matchTemplate(img_rgb, typeImage, cv2.TM_CCOEFF_NORMED)
        if debug:
            end = time.time()
            print("time taken for match: " + str(end - start))
            totalTime += end - start

        threshold = .75
        if debug:
            start = time.time()
        loc = np.where(res >= threshold)
        if debug:
            end = time.time()
            print("time taken for np:" + str(end - start))
            totalTime += end - start

        for pt in zip(*loc[::-1]):  # Switch collmns and rows
            # xy of center point for moving
            x = pt[0] + (w/2)
            y = pt[1] + (h/2)
            tiles.append({"x": x, "y": y, "pt": pt})

        groupedImagesByType = reduce(removeDuplicates, tiles, [])
        if len(groupedImagesByType) > 0:
            groupedImages[type] = groupedImagesByType
            if debug:
                for tile in groupedImages[type]:
                    pt = tile["pt"]
                    cv2.rectangle(img_rgb, pt,
                                  (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                    cv2.putText(img_rgb, type,
                                (pt[0] + w, pt[1] + h),  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    if debug:
        cv2.imwrite('tests/result-'+i+'.png', img_rgb)
        print("time taken: " + str(totalTime))
    # we do this as this game only needs 1 not groups
    group = list(groupedImages.values())
    if len(group) > 0:
        return group[0][0]
    # return list(groupedImages.values())


def findRefImageByTypes(types):
    return [image for image in imageTypes if image['type'] in types]


def click(image):
    x = image['x'] + baseX
    y = image['y']
    pyautogui.click(x, y)


def start():
    start = findImages("1", ["start"])
    if debug:
        print("Clicking start:")
        print(start)
    click(start)
    i = 2
    while i < 180:
        potato = findImages(str(i), ["green", "yellow"])
        if potato:
            if debug:
                print("Clicking Potato:")
                print(potato)
            click(potato)
        i = + 1


while True:
    startText = findImages("0",  ["start-text"])
    if debug:
        print(startText)
    if startText:
        start()
