import cv2
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import sys
import time
from source import OCR

class Train(object):
    image: object
    binaryImage: object

    def __init__(self, filename, gui):
        self.gui = gui
        self.ocr = OCR
        self.image_path = filename
        self.image = cv2.imread(self.image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        print("Train nesnesi olustu")

    def preprocess(self):

        # gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # self.ocr.showDatasetfromImage(gray_image, "Gray Image", self.gui.DatasetFrame,gui=self.gui)
        #
        # blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        # self.ocr.showDatasetfromImage(blurred_image, "Blurred Image", self.gui.DatasetFrame,gui=self.gui)
        #
        # self.binaryImage = cv2.adaptiveThreshold(blurred_image,
        #                                          255,
        #                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #
        #                                          cv2.THRESH_BINARY_INV,
        #                                          # invert so foreground will be white, background will be black
        #                                          11,  # size of a pixel neighborhood used to calculate threshold value
        #                                          2)  # constant subtracted from the mean or weighted mean
        #
        # cv2.waitKey(0)
        # self.ocr.showDatasetfromImage(self.binaryImage, "Binary Image", self.gui.DatasetFrame,gui=self.gui)
        #
        # cv2.destroyAllWindows()
        self.binaryImage, self.gray_image = self.ocr.preprocess(self.image, self.gui, self.gui.DatasetFrame)

    def segmentation(self):

        self.gui.update()
        im2, contours, hierarchy = cv2.findContours(self.binaryImage, cv2.RETR_EXTERNAL,
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
            cv2.rectangle(self.image,   #dogru dimi bu
                          (intX, intY),  # upper left corner
                          (intX + intW, intY + intH),  # lower right corner
                          (0, 0, 255),  # red
                          2)  # thickness

            imgROI = self.binaryImage[intY:intY + intH, intX:intX + intW]
            imgROIResized = cv2.resize(imgROI, (20, 30))

            self.ocr.showDatasetfromImage(self.image, "Training Numbers Segmentation",
                                      self.gui.DatasetFrame,gui=self.gui)  ##burda cagırınca 0.3 saniye bekliyor ondan acılmıyor entry


            intChar = self.gui.entry.get()
            self.gui.update()
            print(intChar)
            time.sleep(0.5)
            if intChar == 27:  # esc
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
        self.gui.clearButtonTrain.configure(state=NORMAL)