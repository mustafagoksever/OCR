from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import operator
from matplotlib import pyplot as plt
import numpy as np


class UserInterface(Tk):

    filename : object

    image_path = ""
    def __init__(self):
        super(UserInterface,self).__init__()
        self.title("OCR")
        self.minsize(720,540)

        self.wm_iconbitmap('myicon.ico')
        self.configure(background = '#FFFFFF')
        self.labelFrame = ttk.LabelFrame(self, text = "Open New Picture")
        self.labelFrame.grid(column=0,row=1,padx=20,pady= 20)

        self.button()

        self.button2()
        self.button3()

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
        cv2.imshow("Gaussian Blur Image", self.blurred_image)
        # cv2.imshow("Gaussian Blur was converted to threshold", thresh_image)
        cv2.waitKey(0)

        ret, self.binary = cv2.threshold(self.blurred_image, 127, 256, cv2.THRESH_BINARY_INV)
        cv2.imshow("Binary Image", self.binary)
        cv2.waitKey(0)
        messagebox.showinfo("Steps", "Preprocessed done! You can push Segmentation Button")
        cv2.destroyAllWindows()
        self.button3.configure(state=NORMAL)
    def segmentation(self):


        im2, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_EXTERNAL,  # retrieve the outermost contours only
                                                    cv2.CHAIN_APPROX_SIMPLE)  # compress horizontal, vertical, and diagonal           segments and leave only their                                                                               end points
        # hierarchy inner outer nesne takibi icin kullaniliyor


        # cv2.drawContours(self.image, contours, -1, (0, 255, 0), 3)
        contours.sort(key=lambda c: np.min(c[:, :, 0]))
        contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * self.image.shape[1])
        # contours.sort(key=operator.attrgetter("0"))
        #         # sort kisminda gelistirmeler yapilacak....
        #         # line segmentation yaparak siralama
        #         # moment ortalamaasi olarak dusun sirala
        #         # knn


        for a,contour in enumerate(contours):

            (x, y, w, h) = cv2.boundingRect(contour)

            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            imgROI = self.gray_image[y:y + h, x:x + w]
            # imgROI = cv2.resize(imgROI, (50, 50))
            cv2.imshow("Original Image", self.image)
            cv2.imshow("ROI", imgROI)

            cv2.imwrite("roi/" + str(a) + '.png', imgROI)

            cv2.waitKey(0)

            cv2.destroyAllWindows()

            # Adataset = cv2.imread("dataset/AUpper.png")
            # Adataset_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            # ret, binarydataset = cv2.threshold(Adataset_gray, 127, 256, cv2.THRESH_BINARY_INV)
            # # binarydataset = cv2.resize(binarydataset, (50, 50))
            # # imgROI = cv2.resize(imgROI, (50, 50))
            # # cv2.imshow("binary dataset",binarydataset)
            #
            # we,he = imgROI.shape[::-1]
            # res = cv2.matchTemplate(Adataset_gray,imgROI,cv2.TM_CCOEFF_NORMED)
            # threshold             = 0.5
            # min max ekle
            # loc = np.where(res >= threshold)
            # for n in zip(*loc[::-1]):
            #     cv2.rectangle(Adataset,n,(n[0]+we,n[1]+he),(0,255,0),2)
            #     print("a buldum")
            #     messagebox.showinfo("A", "A BULDUM")
            #     cv2.imshow("dataset bulunan harf",Adataset)
            #     cv2.imshow("im roi bulunan harf",imgROI)
            #     cv2.waitKey(0)
            #     cv2.destroyAllWindows()
            # cv2.waitKey(0)

        messagebox.showinfo("Steps", "Segmentation done!! Contours were saved!")
        self.button3.configure(state=DISABLED)
        self.button2.configure(state=DISABLED)
        cv2.destroyAllWindows()



























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

        # // / Calculate
        # the
        # area
        # with the moments 00 and compare with the result of the OpenCV function
        # printf("\t Info: Area and Contour Length \n");
        # for (int i = 0; i < contours.size(); i++ )
        # {
        #     printf(" * Contour[%d] - Area (M_00) = %.2f - Area OpenCV: %.2f - Length: %.2f \n", i, mu[i].m00,
        #            contourArea(contours[i]), arcLength(contours[i], true));
        # Scalar
        # color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
        # drawContours(drawing, contours, i, color, 2, 8, hierarchy, 0, Point());
        # circle(drawing, mc[i], 4, color, -1, 8, 0);
        # }
        # }