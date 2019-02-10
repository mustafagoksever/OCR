import functools
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

MIN_CONTOUR_AREA = 50
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30
DIVISION_FACTOR = 500
H_SPAC = 50
V_SPAC = 20


allContoursWithData = []
validContoursWithData = []

class ContourWithData():

    def __init__(self):

        self.npaContour = None           # contour
        self.boundingRect = None         # bounding rect for contour
        self.intRectX = 0                # bounding rect top left corner x location
        self.intRectY = 0                # bounding rect top left corner y location
        self.intRectWidth = 0            # bounding rect width
        self.intRectHeight = 0           # bounding rect height
        self.fltArea = 0.0               # area of contour
        self.aspectRatio = 0.0
        self.XCentroid = 0.0
        self.YCentroid = 0.0

    def rectDetails(self):               # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight
        self.aspectRatio = float(intWidth) / intHeight
        self.XCentroid = intX + intWidth/2
        self.YCentroid = intY + intHeight/2

    def contourCheck(self):
        if self.fltArea > MIN_CONTOUR_AREA and (0.5 < self.aspectRatio < 2): return True    # much better validity checking would be necessary
        return False



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
        self.imageCopy = self.image.copy()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.ocr = OCR

        print("KNN nesnesi olustu")

    def knn(self):
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
        # reshape numpy array to 1d, necessary to pass to call to train#
        kNearest = cv2.ml.KNearest_create()
        kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)
        return kNearest

    def getContourDetails(self, npaContours):

        for npaContour in npaContours:
            # print cv2.contourArea(npaContour)
            contourWithData = ContourWithData()  # instantiate a contour with data object
            contourWithData.npaContour = npaContour  # assign contour to contour with data
            contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)  # get the bounding rect
            contourWithData.rectDetails()  # get bounding rect info
            contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)  # calculate the contour area
            allContoursWithData.append(contourWithData)

        return allContoursWithData

    def compare(self, contourWithData1, contourWithData2):
        if (contourWithData1.intRectY - contourWithData2.intRectY < V_SPAC):
            if (contourWithData1.intRectX < contourWithData2.intRectX):
                return -1
            elif (contourWithData1.intRectX > contourWithData2.intRectX):
                return 1
            else:
                return 0
        else:
            return 0

    def getValidContours(self, allContoursWithData):

        for contourWithData in allContoursWithData:
            if contourWithData.contourCheck():
                validContoursWithData.append(contourWithData)

                (x, y, w, h) = cv2.boundingRect(contourWithData.npaContour)

                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # imgROI = self.binary[y:y + h, x:x + w]  # imgRoi kullanılmıyor

                self.ocr.showDatasetfromImage(self.image, "Segmentation", self.gui.DatasetFrameKNN, gui=self.gui)

        validContoursWithData.sort(key=operator.attrgetter("intRectY"))
        cmp = functools.cmp_to_key(self.compare)
        validContoursWithData.sort(key=cmp)

        return validContoursWithData

    ##
    ##self.allContoursWithData.sort(key=operator.attrgetter("intRectX"))
    ##       for a, contourWithData in enumerate(self.allContoursWithData):  # for all contours
    ##           if contourWithData.contourCheck():
    ##               self.validContoursWithData.append(contourWithData)
    ##               (x, y, w, h) = cv2.boundingRect(contourWithData.npaContour)
    ##
    ##               cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    ##               # imgROI = self.binary[y:y + h, x:x + w]  # imgRoi kullanılmıyor

    def formatCheck(self, contourWithData, i, length):
        line_change = ""

        if (i != length):
            nextContour = validContoursWithData[i]
        else:
            nextContour = validContoursWithData[i - 1]
            # print strFinalString
        if (nextContour.YCentroid - contourWithData.YCentroid > V_SPAC):  # Much better Check required
            line_change = "\n"

        if (nextContour.XCentroid - contourWithData.XCentroid > H_SPAC):  # Much better Check required
            return line_change + "\t"
        return line_change

    def recogtion(self, img, imgThresh, validContoursWithData):

        kNearest = self.knn()
        strFinalString = ""
        i = 0
        a = 0.0
        length = len(validContoursWithData)
        # print length
        for contourWithData in validContoursWithData:
            i += 1
            # print 'Recognising {}th character...{} left'.format(i + 1, length - i)
            # print contourWithData.intRectX, contourWithData.intRectY
            # if(i > 9 ):
            cv2.rectangle(img, (contourWithData.intRectX, contourWithData.intRectY), (
            contourWithData.intRectX + contourWithData.intRectWidth,
            contourWithData.intRectY + contourWithData.intRectHeight), (0, 255, 0), 2)
            # if(i == 45):
            cv2.putText(img, str(i), (int(contourWithData.XCentroid), int(contourWithData.YCentroid)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            imgROI = imgThresh[contourWithData.intRectY: contourWithData.intRectY + contourWithData.intRectHeight,
                     contourWithData.intRectX: contourWithData.intRectX + contourWithData.intRectWidth]
            # imgROI = img[contourWithData.intRectY : contourWithData.intRectY + contourWithData.intRectHeight,contourWithData.intRectX : contourWithData.intRectX + contourWithData.intRectWidth]
            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
            cv2.imwrite("a.jpg", imgROI)
            # strCurrentChar = (label_image.recognize())
            npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
            # npaROIResized = deskew(npaROIResized)
            npaROIResized = np.float32(npaROIResized)


            retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k=1)
            # npaResults = svm.predict_all(npaROIResized)
            strCurrentChar = chr(int(npaResults[0][0]))

            line_change = self.formatCheck(contourWithData, i, length)
            self.strFinalString = self.strFinalString + strCurrentChar + line_change
            #npaContour = None##TO DO#BAK


            # cv2.namedWindow('Fuck '+str(i), cv2.WINDOW_NORMAL)
            # cv2.imshow('Fuck '+str(i), imgROI)
            # print strCurrentChar

            # if (cv2.waitKey(0) & 255) == 121:  ### For Windows Os remove 255 from this line ###
            #     a = a + 1
            # cv2.destroyAllWindows()
            # print contourWithData.intRectX, contourWithData.intRectY

        # print 'Accuracy:', a/ i
        print(self.strFinalString)


        messagebox.showinfo("Result", "The text is " + self.strFinalString)
        self.strFinalString = ""
        self.strCurrentChar = ""
        self.allContoursWithData.clear()
        self.validContoursWithData.clear()

        self.gui.clearButtonKNN.configure(state=NORMAL)
        # print strCurrentChar


    def kNearest(self):

        time.sleep(0.3)

        self.binary, self.gray_image, self.binaryCopy = self.ocr.preprocess(self.image, self.gui, self.gui.DatasetFrameKNN)

        im2, npaContours, npaHierarchy = cv2.findContours(self.binaryCopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        allContoursWithData = self.getContourDetails(npaContours)

        validContoursWithData = self.getValidContours(allContoursWithData)

        self.recogtion(self.imageCopy, self.binaryCopy, validContoursWithData)



        #npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))
        ## reshape numpy array to 1d, necessary to pass to call to train

      # for contourWithData in self.validContoursWithData:
      #     cv2.rectangle(self.image,
      #                   (contourWithData.intRectX, contourWithData.intRectY),  # upper left corner
      #                   (contourWithData.intRectX + contourWithData.intRectWidth,
      #                    contourWithData.intRectY + contourWithData.intRectHeight),  # lower right corner
      #                   (0, 255, 0),  # green
      #                   2)  # thickness

      #     imgROI = self.binary[contourWithData.intRectY: contourWithData.intRectY + contourWithData.intRectHeight,
      #              # crop char out of threshold image
      #              contourWithData.intRectX: contourWithData.intRectX + contourWithData.intRectWidth]

      #     imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
      #     # cv2.imshow("karakter",imgROIResized)
      #     # cv2.waitKey()
      #     # cv2.destroyAllWindows()
      #     self.npaROIResized = imgROIResized.reshape(
      #         (1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image into 1d numpy array

      #     self.npaROIResized = np.float32(
      #         self.npaROIResized)  # convert from 1d numpy array of ints to 1d numpy array of floats
      #     retval, npaResults, neigh_resp, dists = self.kNearest.findNearest(self.npaROIResized, k=1)

#
      #     print(self.strCurrentChar)
      #     self.strFinalString = self.strFinalString + self.strCurrentChar
      #     npaContour=None

      # print("\n" + self.strFinalString + "\n")

      # messagebox.showinfo("Result", "The text is " + self.strFinalString)
      # self.strFinalString = ""
      # self.strCurrentChar = ""
      # self.allContoursWithData.clear()
      # self.validContoursWithData.clear()


      # self.gui.clearButtonKNN.configure(state=NORMAL)

