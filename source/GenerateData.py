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
        self.title("Generate Data for OCR")
        self.minsize(720,540)
        tab_control = ttk.Notebook(self)
        page1 = ttk.Frame(tab_control)
        tab_control.add(page1, text='Train')
        page2 = ttk.Frame(tab_control)
        tab_control.add(page2, text='tedasfa')
        page3 = ttk.Frame(tab_control)
        tab_control.add(page3, text='asfsasfa')

        tab_control.grid(column=0, row=0)


        self.wm_iconbitmap('myicon.ico')
        self.configure(background = '#FFFFFF')
        self.labelFrame = ttk.LabelFrame(page1, text = "OCR Steps")
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save as...",)
        filemenu.add_command(label="Close",)

        filemenu.add_separator() #-------------------------

        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo")

        editmenu.add_separator()

        editmenu.add_command(label="Cut")
        editmenu.add_command(label="Copy")
        editmenu.add_command(label="Paste")
        editmenu.add_command(label="Delete")
        editmenu.add_command(label="Select All")

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index")
        helpmenu.add_command(label="About...")
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.config(menu=menubar)

        self.labelFrame.grid(column=0,row=1,padx=20,pady= 20)
        self.DatasetFrame = ttk.LabelFrame(self, text="Dataset")

        self.DatasetFrame.grid(column=0, row=2, padx=0, pady=0)

        self.button()
        self.button2()
        self.button3()



    def donothing(self):
        print("sada")
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

            imgROI = self.binary[intY:intY+intH, intX:intX+intW]
            imgROIResized = cv2.resize(imgROI, (20, 30))
            # cv2.imshow("imgROI", imgROI)
            cv2.imshow("imgROIResized", imgROIResized)

            imagepanel = Image.fromarray(imgROIResized)
            self.DatasetFrame.image = imagepanel



            cv2.imshow("Training Numbers", self.image)


            intChar = cv2.waitKey(0)

            if intChar == 27:                   # esc
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


if __name__ == '__main__':
    myGUI = GenerateData()

    myGUI.mainloop()
def getGUI():
    return myGUI