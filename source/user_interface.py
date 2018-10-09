from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import cv2

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
        image = cv2.imread(self.filename)
        cv2.imshow("Selected Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_ImagePath(self):
        return self.image_path


