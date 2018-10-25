from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import cv2
from matplotlib import pyplot as plt
import numpy as np


class userinterface(Tk):
#isdafghdfsa
#dsa
    filename: object
    image_path = ""
    def __init__(self):
        super(userinterface,self).__init__()
        self.title("OCR")
        self.minsize(720,540)

        self.wm_iconbitmap('myicon.ico')
        self.configure(background = '#FFFFFF')
        self.labelFrame = ttk.LabelFrame(self, text = "Open New Picture")
        self.labelFrame.grid(column=0,row=1,padx=20,pady= 20)

        self.button()


    def button(self):
        self.button=ttk.Button(self.labelFrame,text = "Browse",command = self.filedialog)
        self.button.grid(column=1,row=1)


    def filedialog(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select a Picture",filetype = (('jpeg','*.jpg'),('png','*.png') ))
        self.label = ttk.Label(self.labelFrame,text="")
        self.label.grid(column =1 ,row = 2)
        self.label.configure(text = self.filename)
        self.image_path = self.filename
        image = cv2.imread(self.filename) # gray_image = cv2.imread(self.filename,0)

        gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        thresh_image = cv2.adaptiveThreshold(blurred_image,  # input image
                                          255,  # make pixels that pass the threshold full white
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          # use gaussian rather than mean, seems to give better results
                                          cv2.THRESH_BINARY_INV,
                                          # invert so foreground will be white, background will be black
                                          11,  # size of a pixel neighborhood used to calculate threshold value
                                          2)  # constant subtracted from the mean or weighted mean
        # adaptive de biraz gurultu var duzelt

        ret,binary = cv2.threshold(blurred_image,127,256,cv2.THRESH_BINARY_INV)

        im2, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            imgROI = binary[y:y + h, x:x + w]
            cv2.imshow("imroi" , imgROI)
        # Adataset = cv2.imread("A.png", 0)
        # ret, binarydataset = cv2.threshold(Adataset, 127, 256, cv2.THRESH_BINARY_INV)
        #
        # we,he = imgROI.shape[::-1]
        # res = cv2.matchTemplate(binarydataset,imgROI,cv2.TM_CCOEFF_NORMED)
        # threshold = 0.8
        # loc = np.where(res>threshold)
        # for n in zip(*loc[::-1]):
        #     cv2.rectangle(Adataset,n,(n[0]+we,n[1]+he),(0,255,255),2)
        #     print("A")
        # cv2.imshow("A dataset",Adataset)
        # normal show
        cv2.imshow("Original Image", image)
        cv2.imshow("Selected Image was converted to gray", gray_image)
        cv2.imshow("Gray Image was converted to Gaussian Blur", blurred_image)
        cv2.imshow("Gaussian Blur was converted to threshold", thresh_image)
        cv2.imshow("Gray Image was converted to binary", binary)
        # pyplots

        #
        # plt.subplot(151),plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        #
        # plt.title('Original Image'),plt.xticks([]),plt.yticks([])
        # plt.subplot(152), plt.imshow(gray_image, cmap='gray')
        # plt.title('Gray'), plt.xticks([]), plt.yticks([])
        # plt.subplot(153), plt.imshow(blurred_image, cmap='gray')
        # plt.title('Gaussian Blur'), plt.xticks([]), plt.yticks([])
        # plt.subplot(154), plt.imshow(thresh_image, cmap='gray')
        # plt.title('Threshold '), plt.xticks([]), plt.yticks([])
        # plt.subplot(155), plt.imshow(binary, cmap='gray')
        # plt.title('Binary '), plt.xticks([]), plt.yticks([])
        # plt.show()


        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def get_ImagePath(self):
        return self.image_path


