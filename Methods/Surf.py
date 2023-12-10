# https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
import math
import random

import cv2
import os
trainPath = "C:\Users\rlvkl\training"
testPath = "C:\Users\rlvkl\testing"
threshold = 0.63
def detect(image, detector):
    finger = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    keyPoints, descriptors = detector.detectAndCompute(finger, None)
    return keyPoints, descriptors

def compare(image1, image2, detector):
    finger1 = cv2.imread(image1)
    finger2 = cv2.imread(image2)

    kp1, desc1 = detect(finger1, detector)
    kp2, desc2 = detect(finger2, detector)

    flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
    matches = flann.knnMatch(desc1, desc2, k=2)
    result = cv2.drawMatchesKnn(finger1, kp1, finger2, kp2, matches, None)

    #Ratio Test
    foundMatch = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            foundMatch.append([m])

    a = len(foundMatch)
    percent = (a * 100) / len(kp2)
    return percent


def fullTest():
    trainFiles = []
    testFiles = []

    for file in os.listdir(trainPath):
        if file.endswith(".png"):
            trainFiles.append(trainPath + '\\' + file)

    for file in os.listdir(testPath):
        if file.endswith(".png"):
            testFiles.append(testPath + '\\' + file)

    trueAccept = 0
    falseAccept = 0
    trueReject = 0
    falseReject = 0

    for findex, refFile in enumerate(trainFiles + testFiles):
        for sIndex, subFile in enumerate((trainFiles + testFiles)[findex:]):
            simPercent = compare(refFile, subFile, cv2.SURF_create())
            print(f'{refFile} compared to {subFile}: %{simPercent}')
            if simPercent >= threshold:
                if refFile[-11:] == subFile[-11:]:
                    trueAccept += 1
                else:
                    falseAccept += 1
            else:
                if refFile[-11:] == subFile[-11:]:
                    falseReject += 1
                else:
                    trueReject += 1
            print("True Accept Rate:", trueAccept)
            print("False Accept Rate:", falseAccept)
            print("True Reject Rate:", trueReject)
            print("False Reject Rate:", falseReject)

#Using a sample because a full test of the set would be n^2 and take too long
def sampleTest():
    trainFiles = []
    testFiles = []

    for file in os.listdir(trainPath):
        if file.endswith(".png") and file.startswith('f'):
            trainFiles.append(trainPath + '\\' + file)

    for file in os.listdir(testPath):
        if file.endswith(".png") and file.startswith('f'):
            testFiles.append(testPath + '\\' + file)

    results = dict()

    for threshold in range(20, 200, 5):
        threshold = threshold/100
        results[threshold] = {
            "trueAccept": 0,
            "falseAccept": 0,
            "trueReject": 0,
            "falseReject": 0
        }
        testRange = trainFiles + testFiles
        for i in range(0, math.floor(len(testRange)/10)):
            refFile = testRange.pop(random.randint(0, len(testRange)))
            score = compare(refFile, refFile[0:-12] + 's' + refFile[-11:], cv2.SURF_create())
            if score >= threshold:
                results[threshold]['trueAccept'] += 1
            else:
                results[threshold]['falseReject'] += 1
            randFile = testRange[random.randint(0, len(testRange))]
            score = compare(refFile,randFile[0:-12] + 's' + randFile[-11:], cv2.SURF_create())
            if score >= threshold:
                results[threshold]['falseAccept'] += 1
            else:
                results[threshold]['trueReject'] += 1
            print(results)

def frrTest():
    trainFiles = []
    testFiles = []
    for file in os.listdir(trainPath):
        if file.startswith('f') and file.endswith('.png'):
            trainFiles.append(file)

    for file in os.listdir(testPath):
        if file.startswith('f') and file.endswith('.png'):
            testFiles.append(file)
    trueAccept = 0
    falseReject = 0
    for file in trainFiles:
        simPercent = compare(trainPath + '\\' + file, trainPath + '\\' + file.replace('f', 's'), cv2.SURF_create())
        print(f'{file} compared to {file.replace("f", "s")}: {simPercent}')

        if simPercent > threshold:
            trueAccept += 1
        else:
            falseReject += 1
        print("True Accept:", trueAccept)
        print("False Reject:", falseReject)

def main():
    sampleTest()

if __name__ == '__main__':
    main()