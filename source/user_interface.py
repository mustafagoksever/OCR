from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import cv2
from matplotlib import pyplot as plt
import numpy as np

MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

class userinterface(Tk):

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


        ret,binary = cv2.threshold(gray_image,127,256,cv2.THRESH_BINARY)
        # normal show
        cv2.imshow("Original Image", image)
        cv2.imshow("Selected Image was converted to gray", gray_image)
        cv2.imshow("Gray Image was converted to Gaussian Blur", blurred_image)
        cv2.imshow("Gaussian Blur was converted to threshold", thresh_image)
        cv2.imshow("Gray Image was converted to binary", binary)
        # pyplots

        # plt.subplot(131),plt.imshow(image,cmap='gray')
        # plt.title('Original Image'),plt.xticks([]),plt.yticks([])
        # plt.subplot(132), plt.imshow(gray_image, cmap='gray')
        # plt.title('Selected Image was converted to gray'), plt.xticks([]), plt.yticks([])
        # plt.subplot(133), plt.imshow(binary, cmap='gray')
        # plt.title('Gray Image was converted to binary'), plt.xticks([]), plt.yticks([])
        # plt.show()

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def get_ImagePath(self):
        return self.image_path


