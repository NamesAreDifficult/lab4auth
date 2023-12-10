import math
import os
import random

import cv2
from Methods import SIFT, Surf, orb

trainPath = "/home/clientbox/training"
testPath = "/home/clientbox/testing"
# threshold = 3

def getSimilarity(image1, image2):
    ORBScore = orb.compare(image1, image2, cv2.ORB_create())
    SIFTScore = SIFT.compare(image1, image2, cv2.xfeatures2d.SIFT_create())
    SURFScore = Surf.compare(image1, image2, cv2.xfeatures2d.SURF_create())

    return ORBScore + SIFTScore + SURFScore

def sampleTest():
    trainFiles = []
    testFiles = []

    for file in os.listdir(trainPath):
        if file.endswith(".png") and file.startswith('f'):
            trainFiles.append(trainPath + '/' + file)

    for file in os.listdir(testPath):
        if file.endswith(".png") and file.startswith('f'):
            testFiles.append(testPath + '/' + file)

    testResults = []
    for testNum in range(0,10):
        results = dict()
        # threshRange = range(20, 200, 5)
        threshRange = range(100, 600, 5)
        for threshold in threshRange:
            threshold = threshold / 100
            results[threshold] = {
                "trueAccept": 0,
                "falseAccept": 0,
                "trueReject": 0,
                "falseReject": 0
            }

        testRange = trainFiles + testFiles
        for i in range(0, math.floor(len(testRange)/10)):
            refFile = testRange.pop(random.randint(0, len(testRange)-1))
            accscore = getSimilarity(refFile, refFile[0:-12] + 's' + refFile[-11:])
            randFile = testRange[random.randint(0, len(testRange) - 1)]
            rejscore = getSimilarity(refFile, randFile[0:-12] + 's' + randFile[-11:])

            for threshold in threshRange:
                threshold = threshold / 100
                if accscore >= threshold:
                    results[threshold]['trueAccept'] += 1
                else:
                    results[threshold]['falseReject'] += 1
                if rejscore >= threshold:
                    results[threshold]['falseAccept'] += 1
                else:
                    results[threshold]['trueReject'] += 1
            print(testNum, results)
        testResults.append(results)
    print(testResults)
    for ind, res in enumerate(testResults):
        print(ind)
        for k,v in res.items():
            print('\t',k,':',v)

def main():
    sampleTest()

if __name__ == "__main__":
    main()
