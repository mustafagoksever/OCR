from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import os
import operator
from matplotlib import pyplot as plt
import numpy as np
import string

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


class Train_Test(Tk):

    filename : object
    text = ""
    image_path = ""
    allContoursWithData = []
    validContoursWithData = []
    kNearest : object
    npaROIResized :object
    strFinalString = ""
    def __init__(self):
        super(Train_Test,self).__init__()
        self.title("OCR")
        self.minsize(720,540)

        self.wm_iconbitmap('myicon.ico')
        self.configure(background = '#FFFFFF')
        self.labelFrame = ttk.LabelFrame(self, text = "Open New Picture")
        self.labelFrame.grid(column=0,row=1,padx=20,pady= 20)

        self.button()

        self.button2()
        self.button3()
        self.button4()

    def button(self):
        self.button=ttk.Button(self.labelFrame,text = "Browse",command = self.filedialog)
        self.button.grid(column=1,row=1)

    def button2(self):
        self.button2=ttk.Button(self.labelFrame,text = "Preprocess",command = self.preproces)
        self.button2.grid(column=1,row=2)
        self.button2.configure(state=DISABLED)
    def button3(self):
        self.button3=ttk.Button(self.labelFrame,text = "Segmentation",command = self.segmentation)
        self.button3.grid(column=1,row=3)
        self.button3.configure(state=DISABLED)
    def button4(self):
        self.button4 = ttk.Button(self.labelFrame, text="Test", command=self.test)
        self.button4.grid(column=1, row=4)
        self.button4.configure(state=DISABLED)
    def filedialog(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select a Picture",filetype = (('jpeg','*.jpg'),('png','*.png') ))

        if self.filename is not "":
            self.button2.configure(state=NORMAL)
            self.image_path = self.filename
        else :
            messagebox.showerror("Error", "You did not select any photo! Browse again!")


    def get_ImagePath(self):
        return self.image_path


    def preproces(self):

        self.image = cv2.imread(self.image_path)  # gray_image = cv2.imread(self.filename,0)

        cv2.imshow("Original Image", self.image)
        cv2.waitKey(0)
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Gray Image", self.gray_image)
        cv2.waitKey(0)
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
        cv2.waitKey(0)

        ret, self.binary = cv2.threshold(self.gray_image, 127, 256, cv2.THRESH_BINARY_INV)
        cv2.imshow("Binary Image", self.binary)
        cv2.waitKey(0)
        messagebox.showinfo("Steps", "Preprocessed done! You can push Segmentation Button")
        cv2.destroyAllWindows()
        self.button3.configure(state=NORMAL)
    def segmentation(self):


        im2, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for npaContour in contours:
            contourWithData = ContourWithData()
            contourWithData.npaContour = npaContour  #
            contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)
            contourWithData.calculateRectTopLeftPointAndWidthAndHeight()
            contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)
            self.allContoursWithData.append(
                contourWithData)

        self.allContoursWithData.sort(key=operator.attrgetter("intRectX"))
        for a,contourWithData in enumerate(self.allContoursWithData):  # for all contours
            if contourWithData.checkIfContourIsValid():
                self.validContoursWithData.append(contourWithData)
                (x, y, w, h) = cv2.boundingRect(contourWithData.npaContour)

                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                imgROI = self.binary[y:y + h, x:x + w]
                # thresholdan alabiliriz
                # imgROI = cv2.resize(imgROI, (50, 50))
                cv2.imshow("Original Image", self.image)
                cv2.imshow("ROI", imgROI)

                cv2.imwrite("roi/" + str(a) + '.png', imgROI)
                cv2.waitKey(0)


        # contours.sort(key=lambda c: np.min(c[:, :, 0]))
        # contours = sorted(contours,
        # key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * self.image.shape[1])




             # wait for user key press
        #         for a, contour in enumerate(contours):
        # (x, y, w, h) = cv2.boundingRect(contour)
        #
        #     cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     imgROI = self.binary[y:y + h, x:x + w]
        #
        #     # imgROI = cv2.resize(imgROI, (50, 50))
        #     cv2.imshow("Original Image", self.image)
        #     cv2.imshow("ROI", imgROI)
        #
        #     cv2.imwrite("roi/" + str(a) + '.png', imgROI)
        #     cv2.waitKey(0)

        cv2.destroyAllWindows()
        self.button4.configure(state=NORMAL)
    def test(self):
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
            # call KNN function find_nearest

            strCurrentChar = str(chr(int(npaResults[0][0])))

            self.strFinalString = self.strFinalString + strCurrentChar


        print("\n" + self.strFinalString + "\n")

        cv2.imshow("imgTestingNumbers",self.image)

        messagebox.showinfo("Result", "The text is " + self.strFinalString)
        cv2.waitKey(0)

if __name__ == "__main__":
    myGUI = Train_Test()
    myGUI.mainloop()



