import cv2
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from PIL import ImageTk, Image
import sys

from source.UserInterface import userInterface

class Ocr():
    image :object
    binaryImage :object


    def __init__(self,filename,gui):
        self.gui = gui
        self.image_path =filename
        self.image = cv2.imread(self.image_path)
        print("ocr nesnesi olustu")

    def showDatasetfromImage(self,image,string):

        self.gui.showDatasetfromImage(image)
        self.gui.DatasetFrame.configure(text=string)
        self.gui.update()

        # cv2.waitKey(0)
    #     next butonunu bekleme olayi
    def preprocess(self):

        self.gui.nextStepButton.configure(state=NORMAL)
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




            cv2.imshow("Training Numbers", self.image)
            self.showDatasetfromImage(self.image,"Training Numbers Segmentation")

            intChar = cv2.waitKey(0)

            if intChar == 27:                   # esc
               sys.exit()
            elif intChar in intValidChars:
                intClassifications.append(intChar)

                npaFlattenedImage = imgROIResized.reshape((1, 20 * 30))
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)

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
