import os
import cv2
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import time
import operator
from source import OCR

MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

class ContourWithData():
    npaContour = None
    boundingRect = None
    intRectX = 0
    intRectY = 0
    intRectWidth = 0
    intRectHeight = 0
    fltArea = 0.0

    def calculateRectTopLeftPointAndWidthAndHeight(self):
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):
        if self.fltArea < MIN_CONTOUR_AREA: return False
        return True



class KNearest():
    image: object
    binaryImage: object
    allContoursWithData = []
    validContoursWithData = []
    kNearest: object
    strCurrentChar =""

    strFinalString = ""

    def __init__(self, filename, gui):
        self.gui = gui
        self.image_path = filename
        self.image = cv2.imread(self.image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.ocr = OCR

        print("KNN nesnesi olustu")

    def kNearest(self):

        time.sleep(0.3)

        self.binary, self.gray_image = self.ocr.preprocess(self.image, self.gui, self.gui.DatasetFrameKNN)

        im2, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for npaContour in contours:
            contourWithData = ContourWithData()
            contourWithData.npaContour = npaContour
            contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)
            contourWithData.calculateRectTopLeftPointAndWidthAndHeight()
            contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)
            self.allContoursWithData.append(
                contourWithData)

        self.allContoursWithData.sort(key=operator.attrgetter("intRectX"))
        for a, contourWithData in enumerate(self.allContoursWithData):  # for all contours
            if contourWithData.checkIfContourIsValid():
                self.validContoursWithData.append(contourWithData)
                (x, y, w, h) = cv2.boundingRect(contourWithData.npaContour)

                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # imgROI = self.binary[y:y + h, x:x + w]  # imgRoi kullanılmıyor

                self.ocr.showDatasetfromImage(self.image, "Segmentation", self.gui.DatasetFrameKNN, gui=self.gui)


        try:
            npaClassifications = np.loadtxt("Classifications.txt", np.float32)
        except:
            print("error, unable to open classifications.txt, exiting program\n")
            os.system("pause")
            return

        try:
            npaFlattenedImages = np.loadtxt("Flattened_images.txt", np.float32)
        except:
            print("error, unable to open flattened_images.txt, exiting program\n")
            os.system("pause")
            return

        npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))
        # reshape numpy array to 1d, necessary to pass to call to train

        self.kNearest = cv2.ml.KNearest_create()  # instantiate KNN object

        self.kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)


        for contourWithData in self.validContoursWithData:
            cv2.rectangle(self.image,
                          (contourWithData.intRectX, contourWithData.intRectY),  # upper left corner
                          (contourWithData.intRectX + contourWithData.intRectWidth,
                           contourWithData.intRectY + contourWithData.intRectHeight),  # lower right corner
                          (0, 255, 0),  # green
                          2)  # thickness

            imgROI = self.binary[contourWithData.intRectY: contourWithData.intRectY + contourWithData.intRectHeight,
                     # crop char out of threshold image
                     contourWithData.intRectX: contourWithData.intRectX + contourWithData.intRectWidth]

            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
            # cv2.imshow("karakter",imgROIResized)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            self.npaROIResized = imgROIResized.reshape(
                (1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image into 1d numpy array

            self.npaROIResized = np.float32(
                self.npaROIResized)  # convert from 1d numpy array of ints to 1d numpy array of floats
            retval, npaResults, neigh_resp, dists = self.kNearest.findNearest(self.npaROIResized, k=1)

            self.strCurrentChar = str(chr(int(npaResults[0][0])))

            print(self.strCurrentChar)
            self.strFinalString = self.strFinalString + self.strCurrentChar
            npaContour=None

        print("\n" + self.strFinalString + "\n")

        messagebox.showinfo("Result", "The text is " + self.strFinalString)
        self.strFinalString = ""
        self.strCurrentChar = ""
        self.allContoursWithData.clear()
        self.validContoursWithData.clear()
        

        self.gui.clearButtonKNN.configure(state=NORMAL)

