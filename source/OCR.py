import os

import cv2
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from PIL import ImageTk, Image
import sys
import time
import string
import operator
MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30


from source.UserInterface import userInterface

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


class Ocr():
    image :object
    binaryImage :object
    allContoursWithData = []
    validContoursWithData = []
    kNearest: object
    npaROIResized: object
    strFinalString = ""

    def __init__(self,filename,gui):
        self.gui = gui
        self.image_path =filename
        self.image = cv2.imread(self.image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        print("ocr nesnesi olustu")

    def showDatasetfromImage(self,image,string):


        self.gui.showDatasetfromImage(image)
        self.gui.DatasetFrame.configure(text=string)
        self.gui.update()
        time.sleep(0.3)
        # cv2.waitKey(0)
    #     next butonunu bekleme olayi
    def preprocess(self):

       # self.gui.nextStepButton.configure(state=NORMAL)
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Gray Image", gray_image)

        self.showDatasetfromImage(gray_image,"Gray Image")

        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
       # cv2.imshow("Blurred Image", blurred_image)
        self.showDatasetfromImage(blurred_image, "Blurred Image")
        self.binaryImage = cv2.adaptiveThreshold(blurred_image,
                                          255,
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

                                          cv2.THRESH_BINARY_INV,
                                          # invert so foreground will be white, background will be black
                                          11,  # size of a pixel neighborhood used to calculate threshold value
                                          2)  # constant subtracted from the mean or weighted mean

        cv2.waitKey(0)

        # ret, binary = cv2.threshold(gray_image, 127, 256, cv2.THRESH_BINARY_INV)
       # cv2.imshow("Binary Image", self.binaryImage)
       # cv2.waitKey(0)#
        self.showDatasetfromImage(self.binaryImage, "Binary Image")

        #messagebox.showinfo("Steps", "Preprocessed done! You can push Segmentation Button")
        cv2.destroyAllWindows()


    def getImage(self):
        return self.image

    def segmentation(self):

        im2, contours, hierarchy = cv2.findContours(self.binaryImage, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_SIMPLE)

        npaFlattenedImages = np.empty((0, 20 * 30))

        intClassifications = []
        intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'), ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'), ord('I'), ord('J'),ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'), ord('R'), ord('S'),ord('T'),ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z'),ord('a'),ord('b'),ord('c'),ord('d')]

        for npaContour in contours:

            if cv2.contourArea(npaContour) > 100:
                [intX, intY, intW, intH] = cv2.boundingRect(npaContour)
            cv2.rectangle(self.image,
                          (intX, intY),                 # upper left corner
                          (intX+intW,intY+intH),        # lower right corner
                          (0, 0, 255),                  # red
                          2)                            # thickness

            imgROI = self.binaryImage[intY:intY+intH, intX:intX+intW]
            imgROIResized = cv2.resize(imgROI, (20, 30))
            # cv2.imshow("imgROI", imgROI)
            # cv2.imshow("imgROIResized", imgROIResized)




            #cv2.imshow("Training Numbers", self.image)
            self.showDatasetfromImage(self.image,"Training Numbers Segmentation")
            #intChar = cv2.waitKey(0)

            intChar = self.gui.entry.get()
            #self.gui.entry.delete(0, END)
            self.gui.update()
            print(intChar)
            time.sleep(2)
            if intChar == 27:                   # esc
               sys.exit()
            elif intChar in intValidChars:
                intClassifications.append(intChar)

                npaFlattenedImage = imgROIResized.reshape((1, 20 * 30))
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)
            self.gui.entry.bind('<Return>', self.gui.newmethod)


        floatClassifications = np.array(intClassifications, np.float32)

        npaClassifications = floatClassifications.reshape((floatClassifications.size, 1))

        print("\ntraining complete !!\n")

        np.savetxt("Classifications.txt", npaClassifications)
        np.savetxt("Flattened_images.txt", npaFlattenedImages)
        messagebox.showinfo("Generate Data", "Training complete !!")
        cv2.destroyAllWindows()
    def genDate(self):
        im2, contours, hierarchy = cv2.findContours(self.binaryimage, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_SIMPLE)

        npaFlattenedImages = np.empty((0, 20 * 30))

        intClassifications = []
        intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'),
                         ord('9'), ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'),
                         ord('I'), ord('J'), ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'),
                         ord('R'), ord('S'), ord('T'), ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z'),
                         ord('a'), ord('b'), ord('c'), ord('d')]

        for npaContour in contours:

            if cv2.contourArea(npaContour) > 100:
                [intX, intY, intW, intH] = cv2.boundingRect(npaContour)
            cv2.rectangle(self.image,
                          (intX, intY),  # upper left corner
                          (intX + intW, intY + intH),  # lower right corner
                          (0, 0, 255),  # red
                          2)  # thickness

            imgROI = self.binary[intY:intY + intH, intX:intX + intW]
            imgROIResized = cv2.resize(imgROI, (20, 30))
            # cv2.imshow("imgROI", imgROI)
            # cv2.imshow("imgROIResized", imgROIResized)

            imagepanel = Image.fromarray(imgROIResized)

            # cv2.imshow("Training Numbers", self.image)

            intChar = cv2.waitKey(0)

            if intChar == 27:  # esc
                sys.exit()
            elif intChar in intValidChars:
                intClassifications.append(intChar)

                npaFlattenedImage = imgROIResized.reshape((1, 20 * 30))
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)

        foloatClassifications = np.array(intClassifications, np.float32)

        npaClassifications = foloatClassifications.reshape((foloatClassifications.size, 1))

        print("\n\ntraining complete !!\n")

        np.savetxt("Classifications.txt", npaClassifications)
        np.savetxt("Flattened_images.txt", npaFlattenedImages)
        messagebox.showinfo("Generate Data", "Training complete !!")
        cv2.destroyAllWindows()

    def matchTemplate(self):
        text:object
        text=""
        self.gui.update()
        time.sleep(0.5)

        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.gui.showDatasetfromImageMatch(self.gray_image)
        self.gui.DatasetFrameMatch.configure(text="Gray Image")
        self.gui.update()
        time.sleep(0.5)

        self.blurred_image = cv2.GaussianBlur(self.gray_image, (5, 5), 0)
        # thresh_image = cv2.adaptiveThreshold(blurred_image,  # input image
        #                                   255,  # make pixels that pass the threshold full white
        #                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                                   # use gaussian rather than mean, seems to give better results
        #                                   cv2.THRESH_BINARY_INV,
        #                                   # invert so foreground will be white, background will be black
        #                                   11,  # size of a pixel neighborhood used to calculate threshold value
        #                                   2)  # constant subtracted from the mean or weighted mean
        # # adaptive de biraz gurultu var duzelt
        # cv2.imshow("Gaussian Blur Image", self.blurred_image)
        # cv2.imshow("Gaussian Blur was converted to threshold", thresh_image)
        self.gui.showDatasetfromImageMatch(self.blurred_image)
        self.gui.DatasetFrameMatch.configure(text="Blurred Image")
        self.gui.update()
        time.sleep(0.5)

        ret, self.binary = cv2.threshold(self.gray_image, 127, 256, cv2.THRESH_BINARY_INV)
        self.gui.showDatasetfromImageMatch(self.binary)
        self.gui.DatasetFrameMatch.configure(text="Binary Image")
        self.gui.update()

        time.sleep(0.5)
        im2, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_EXTERNAL,
                                                    # retrieve the outermost contours only
                                                    cv2.CHAIN_APPROX_SIMPLE)  # compress horizontal, vertical, and diagonal           segments and leave only their                                                                               end points
        # hierarchy inner outer nesne takibi icin kullaniliyor

        # cv2.drawContours(self.image, contours, -1, (0, 255, 0), 3)
        contours.sort(key=lambda c: np.min(c[:, :, 0]))
        contours = sorted(contours,
                          key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * self.image.shape[1])
        # contours.sort(key=operator.attrgetter("0"))
        #         # sort kisminda gelistirmeler yapilacak....
        #         # line segmentation yaparak siralama
        #         # moment ortalamaasi olarak dusun sirala
        #         #

        for a, contour in enumerate(contours):

            (x, y, w, h) = cv2.boundingRect(contour)

            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            imgROI = self.gray_image[y:y + h, x:x + w]
            # thresholdan alabiliriz
            # imgROI = cv2.resize(imgROI, (50, 50))

            self.gui.showDatasetfromImageMatch(self.image)
            self.gui.DatasetFrameMatch.configure(text="Image Segmentation")
            self.gui.update()

            cv2.imwrite("roi/" + str(a) + '.png', imgROI)

            for x in list(string.ascii_uppercase):
                Adataset = cv2.imread("dataset/" + x + ".png")
                Adataset_gray = cv2.cvtColor(Adataset, cv2.COLOR_BGR2GRAY)
                ret, binarydataset = cv2.threshold(Adataset_gray, 127, 256, cv2.THRESH_BINARY_INV)
                # binarydataset = cv2.resize(binarydataset, (50, 50))
                # imgROI = cv2.resize(imgROI, (80, 60))
                # cv2.imshow("binary dataset",binarydataset)
                we, he = imgROI.shape[::-1]
                res = cv2.matchTemplate(Adataset_gray, imgROI, cv2.TM_CCOEFF_NORMED)
                threshold = 0.85

                # min max ekle
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                top_left = max_loc
                bottom_right = (top_left[0] + we, top_left[1] + he)
                if (max_val >= threshold):
                    print(x + " bulundu....")
                    text = text + x
                    break



            # loc = np.where(res >= threshold)
            # for n in zip(*loc[::-1]):
            #     cv2.rectangle(Adataset,n,(n[0]+we,n[1]+he),(0,255,0),2)
            #     print("a buldum")
            #     messagebox.showinfo("A", "A BULDUM")
            #     # cv2.imshow("dataset bulunan harf",Adataset)
            #     # cv2.imshow("im roi bulunan harf",imgROI)
            #     cv2.waitKey(0)
            #     cv2.destroyAllWindows()

            time.sleep(0.3)
        messagebox.showinfo("Result", "The text is " + text)
        print("The text is " + text)

        text = ""

    def kNearest(self):

        time.sleep(0.5)
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        self.gui.showDatasetfromImageKNN(self.gray_image)
        self.gui.DatasetFrameKNN.configure(text="Gray Image")
        self.gui.update()
        time.sleep(0.5)


        self.blurred_image = cv2.GaussianBlur(self.gray_image, (5, 5), 0)
        self.gui.showDatasetfromImageKNN(self.blurred_image)
        self.gui.DatasetFrameKNN.configure(text="Blurred Image")
        self.gui.update()
        time.sleep(0.5)


        ret, self.binary = cv2.threshold(self.gray_image, 127, 256, cv2.THRESH_BINARY_INV)
        self.gui.showDatasetfromImageKNN(self.binary)
        self.gui.DatasetFrameKNN.configure(text="Binary Image")
        self.gui.update()
        time.sleep(0.5)

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
                imgROI = self.binary[y:y + h, x:x + w]
                self.gui.showDatasetfromImageKNN(self.image)
                self.gui.DatasetFrameKNN.configure(text="Segmentation")
                self.gui.update()
                time.sleep(0.3)
                # thresholdan alabiliriz
            # #   # imgROI = cv2.resize(imgROI, (50, 50))
             #   cv2.imshow("Original Image", self.image)
             #   cv2.imshow("ROI", imgROI)
#
             #   cv2.imwrite("roi/" + str(a) + '.png', imgROI)


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

            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH,RESIZED_IMAGE_HEIGHT))

            self.npaROIResized = imgROIResized.reshape(
                (1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image into 1d numpy array

            self.npaROIResized = np.float32(self.npaROIResized)  # convert from 1d numpy array of ints to 1d numpy array of floats
            retval, npaResults, neigh_resp, dists = self.kNearest.findNearest(self.npaROIResized,k=1)

            strCurrentChar = str(chr(int(npaResults[0][0])))
            print(strCurrentChar)
            self.strFinalString = self.strFinalString + strCurrentChar



        print("\n" + self.strFinalString + "\n")



        messagebox.showinfo("Result", "The text is " + self.strFinalString)
        self.strFinalString=""
        cv2.waitKey(0)

