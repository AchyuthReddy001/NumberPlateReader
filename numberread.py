# Main.py

import cv2
from termcolor import colored
import numpy as np
import BankTrans
import os
import sys
import argparse
import vehicle
from datetime import datetime
import csv

import DetectChars
import DetectPlates
import PossiblePlate

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

###################################################################################################
def num_read(var):
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()
    if blnKNNTrainingSuccessful == False:
        print("\nerror: KNN traning was not successful\n")
        return
    # end if
    '''
    path= argparse.ArgumentParser()
    path.add_argument("-i", "--input", required=True,
                    help="path to input image")
    args = vars(path.parse_args())
    imgOriginalScene  = cv2.imread(args["input"])
    vech=vehicle.test_single_image(args["input"])
    '''
    path = var
    imgOriginalScene = cv2.imread(path)  # open image
    #vech = vehicle.test_single_image(path)

    if imgOriginalScene is None:
        print("\nerror: image not read from file \n\n")  #
        os.system("pause")
        return
    # end if
    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)
    #cv2.imshow("imgOriginalScene", imgOriginalScene)
    if len(listOfPossiblePlates) == 0:
         print("\nno license plates were detected\n")
    else:
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
        licPlate = listOfPossiblePlates[0]
        #cv2.imshow("imgPlate", licPlate.imgPlate)
        #cv2.imshow("imgThresh", licPlate.imgThresh)
        if len(licPlate.strChars) == 0:
            #print("\nno characters were detected\n\n")
            return
        # end if
        #print("\nlicense plate read from image = " + licPlate.strChars + "\n")
        #print("----------------------------------------")
        #cv2.imshow("imgOriginalScene", imgOriginalScene)
        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)

    # end if else
    return licPlate.strChars
# end main



















