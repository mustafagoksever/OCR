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


from source import OCR, SnapFromPhoneCamera

MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30


class MatchTemplate(object):
    image: object
    binaryImage: object
    text: object
    def __init__(self, filename, gui):
        self.ocr = OCR
        self.gui = gui
        self.image_path = filename
        self.image = cv2.imread(self.image_path)
        self.imageCopy = self.image.copy()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        print("Match Template nesnesi olustu")

    def TakePhotoFromPhoneCamera(self):
        img = SnapFromPhoneCamera.takeAPhotoFromPhoneCamere()

        cv2.imshow("kjbkj",self.img)

    def matchTemplate(self):
        text = ""
        self.gui.update()
        time.sleep(0.5)
        self.binary, self.gray_image, self.binaryCopy = self.ocr.preprocess(self.image,self.gui,self.gui.DatasetFrameMatch)

        im2, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_SIMPLE)

        # contours.sort(key=lambda c: np.min(c[:, :, 0]))
        # contours = sorted(contours,
        #                   key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * self.image.shape[1])


        # 2. method
        # contours = sorted(contours, key=lambda cont: cv2.boundingRect(cont)[0])

        # 3.Method
        (contours, boundingBoxes) = self.sort_contours(contours, method="left-to-right")
        for a, contour in enumerate(contours):

            (x, y, w, h) = cv2.boundingRect(contour)

            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            imgROI = self.binary[y:y + h, x:x + w]

            self.ocr.showDatasetfromImage(self.image, "Image Segmentation",
                                      self.gui.DatasetFrameMatch, gui=self.gui)


            cv2.imwrite("roi/" + str(a) + '.png', imgROI)

            for x in list(string.ascii_uppercase):
                Adataset = cv2.imread("dataset/" + x + ".png")
                Adataset_gray = cv2.cvtColor(Adataset, cv2.COLOR_BGR2GRAY)
                ret, binarydataset = cv2.threshold(Adataset_gray, 127, 256, cv2.THRESH_BINARY_INV)

                we, he = imgROI.shape[::-1]
                res = cv2.matchTemplate(binarydataset, imgROI, cv2.TM_CCOEFF_NORMED)
                threshold = 0.85

                # min max ekle
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                top_left = max_loc
                bottom_right = (top_left[0] + we, top_left[1] + he)
                if (max_val >= threshold):
                    print(x + " found....")
                    text = text + x
                    break


            time.sleep(0.3)
        messagebox.showinfo("Result", "The text is " + text)
        print("The text is " + text)

        text = ""
        self.gui.clearButtonMatch.configure(state=NORMAL)

    def sort_contours(self,cnts, method="left-to-right"):
            # initialize the reverse flag and sort index
            reverse = False
            i = 0

            # handle if we need to sort in reverse
            if method == "right-to-left" or method == "bottom-to-top":
                reverse = True

            # handle if we are sorting against the y-coordinate rather than
            # the x-coordinate of the bounding box
            if method == "top-to-bottom" or method == "bottom-to-top":
                i = 1

            # construct the list of bounding boxes and sort them from top to
            # bottom
            boundingBoxes = [cv2.boundingRect(c) for c in cnts]
            (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                                key=lambda b: b[1][i], reverse=reverse))

            # return the list of sorted contours and bounding boxes
            return (cnts, boundingBoxes)
