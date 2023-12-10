# https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
import math
import random

import cv2
import os
trainPath = "C:\\Users\\trueh\\Documents\\fingerprints\\Train"
testPath = "C:\\Users\\trueh\\Documents\\fingerprints\\Test"
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

    brute = cv2.BFMatcher()
    matches = brute.knnMatch(desc1, desc2, k=2)

    #Ratio Test
    foundMatch = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            foundMatch.append([m])

    a = len(foundMatch)
    percent = (a * 100) / len(kp2)
    return percent

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

    testResults = []
    for testNum in range(0,10):
        results = dict()
        threshRange = range(20, 200, 5)
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
            accscore = compare(refFile, refFile[0:-12] + 's' + refFile[-11:], cv2.ORB_create())
            randFile = testRange[random.randint(0, len(testRange) - 1)]
            rejscore = compare(refFile, randFile[0:-12] + 's' + randFile[-11:], cv2.ORB_create())
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

if __name__ == '__main__':
    main()
