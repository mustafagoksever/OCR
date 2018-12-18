from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import operator
from matplotlib import pyplot as plt
import numpy as np
import string
from PIL import ImageTk, Image

class GenerateData(Tk):

    filename : object
    text = ""
    image_path = ""
    Datasetpanel :object
    def __init__(self):
        super(GenerateData,self).__init__()
        self.title("OCR")
        self.minsize(720,540)

        self.wm_iconbitmap('myicon.ico')
        self.configure(background = '#FFFFFF')
        self.labelFrame = ttk.LabelFrame(self, text = "OCR Steps")

        self.labelFrame.grid(column=0,row=1,padx=20,pady= 20)
        self.DatasetFrame = ttk.LabelFrame(self, text="Dataset")

        self.DatasetFrame.grid(column=0, row=2, padx=20, pady=20)

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
        self.button3=ttk.Button(self.labelFrame,text = "Segmentation and Generate Data",command = self.segmentation)
        self.button3.grid(column=1,row=3)
        self.button3.configure(state=DISABLED)
    def filedialog(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select a Picture",filetype = (('jpeg','*.jpg'),('png','*.png') ))

        if self.filename is not "":
            self.button2.configure(state=NORMAL)
            self.image_path = self.filename
            img = ImageTk.PhotoImage(Image.open(self.image_path))

            self.Datasetpanel = ttk.Label(self.DatasetFrame, image=img)
            self.DatasetFrame.image = img
            self.Datasetpanel.grid(column=0, row=0)
            # panel.pack(side="bottom", fill="both", expand="yes")
            # panel.pack()
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

        cv2.waitKey(0)

        ret, self.binary = cv2.threshold(self.gray_image, 127, 256, cv2.THRESH_BINARY_INV)
        cv2.imshow("Binary Image", self.binary)
        cv2.waitKey(0)
        messagebox.showinfo("Steps", "Preprocessed done! You can push Segmentation Button")
        cv2.destroyAllWindows()
        self.button3.configure(state=NORMAL)
    def segmentation(self):


        im2, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_SIMPLE)

        npaFlattenedImages = np.empty((0, 20 * 30))

        intClassifications = []  # declare empty classifications list, this will be our list of how we are classifying our chars from user input, we will write to file at the end
        #
        # possible chars we are interested in are digits 0 through 9, put these in list intValidChars

        intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'), ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'), ord('I'), ord('J'),ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'), ord('R'), ord('S'),ord('T'),ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z')]

        for npaContour in contours:
            # for each contour
            if cv2.contourArea(npaContour) > 100:          # if contour is big enough to consider
                [intX, intY, intW, intH] = cv2.boundingRect(npaContour)         # get and break out bounding rect

                                                # draw rectangle around each contour as we ask user for input
            cv2.rectangle(self.image,           # draw rectangle on original training image
                          (intX, intY),                 # upper left corner
                          (intX+intW,intY+intH),        # lower right corner
                          (0, 0, 255),                  # red
                          2)                            # thickness

            imgROI = self.binary[intY:intY+intH, intX:intX+intW]                                  # crop char out of threshold image
            imgROIResized = cv2.resize(imgROI, (20, 30))     # resize image, this will be more consistent for recognition and storage

            cv2.imshow("imgROI", imgROI)                    # show cropped out char for reference
            cv2.imshow("imgROIResized", imgROIResized)      # show resized image for reference
            cv2.imshow("training_numbers.png", self.image)      # show training numbers image, this will now have red rectangles drawn on it


            intChar = cv2.waitKey(0)                     # get key press

            if intChar == 27:                   # if esc key was pressed
                sys.exit()                      # exit program
            elif intChar in intValidChars:      # else if the char is in the list of chars we are looking for . . .

                intClassifications.append(intChar)                                                # append classification char to integer list of chars (we will convert to float later before writing to file)

                npaFlattenedImage = imgROIResized.reshape((1, 20 * 30))  # flatten image to 1d numpy array so we can write to file later
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)                    # add current flattened impage numpy array to list of flattened image numpy arrays
            # end if
        # end if
    # end for

        fltClassifications = np.array(intClassifications,
                                  np.float32)  # convert classifications list of ints to numpy array of floats

        npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))  # flatten numpy array of floats to 1d so we can write to file later

        print("\n\ntraining complete !!\n")

        np.savetxt("classifications.txt", npaClassifications)  # write flattened images to file
        np.savetxt("flattened_images.txt", npaFlattenedImages)  #
        print("kaydetme bitti")
        cv2.destroyAllWindows()























































 #
 #        # cv2.drawContours(self.image, contours, -1, (0, 255, 0), 3)
 #        contours.sort(key=lambda c: np.min(c[:, :, 0]))
 #        contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * self.image.shape[1])
 #        # contours.sort(key=operator.attrgetter("0"))
 #        #         # sort kisminda gelistirmeler yapilacak....
 #        #         # line segmentation yaparak siralama
 #        #         # moment ortalamaasi olarak dusun sirala
 #        #         #
 #
 #
 #
 #        for a,contour in enumerate(contours):
 #
 #            (x, y, w, h) = cv2.boundingRect(contour)
 #
 #            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
 #            imgROI = self.gray_image[y:y + h, x:x + w]
 #            # thresholdan alabiliriz
 #            # imgROI = cv2.resize(imgROI, (50, 50))
 #            cv2.imshow("Original Image", self.image)
 #            cv2.imshow("ROI", imgROI)
 #
 #            cv2.imwrite("roi/" + str(a) + '.png', imgROI)
 #
 #
 #
 #            for x in list(string.ascii_uppercase):
 #                Adataset = cv2.imread("dataset/"+x+".png")
 #                Adataset_gray = cv2.cvtColor(Adataset, cv2.COLOR_BGR2GRAY)
 #                ret,binarydataset = cv2.threshold(Adataset_gray, 127, 256, cv2.THRESH_BINARY_INV)
 #                # binarydataset = cv2.resize(binarydataset, (50, 50))
 #                # imgROI = cv2.resize(imgROI, (80, 60))
 #                # cv2.imshow("binary dataset",binarydataset)
 #                we,he = imgROI.shape[::-1]
 #                res = cv2.matchTemplate(Adataset_gray,imgROI,cv2.TM_CCOEFF_NORMED)
 #                threshold = 0.85
 #
 #
 #                # min max ekle
 #                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
 #                top_left = max_loc
 #                bottom_right = (top_left[0] + we, top_left[1] + he)
 #                if(max_val >= threshold):
 #                    print(x+" bulundu....")
 #                    self.text = self.text + x
 #                    break
 #
 #            cv2.waitKey(0)
 #            cv2.destroyAllWindows()
 #            # loc = np.where(res >= threshold)
 #            # for n in zip(*loc[::-1]):
 #            #     cv2.rectangle(Adataset,n,(n[0]+we,n[1]+he),(0,255,0),2)
 #            #     print("a buldum")
 #            #     messagebox.showinfo("A", "A BULDUM")
 #            #     # cv2.imshow("dataset bulunan harf",Adataset)
 #            #     # cv2.imshow("im roi bulunan harf",imgROI)
 #            #     cv2.waitKey(0)
 #            #     cv2.destroyAllWindows()
 #
 #
 #        messagebox.showinfo("Steps", "Segmentation done!! Contours were saved!")
 #        messagebox.showinfo("Result", "The text is " + self.text)
 #        print("The text is " + self.text)
 #        self.button3.configure(state=DISABLED)
 #        self.button2.configure(state=DISABLED)
 #        self.text = ""
 #        cv2.destroyAllWindows()
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 # # pyplots

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

if __name__ == '__main__':
    myGUI = GenerateData()

    myGUI.mainloop()
