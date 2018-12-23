from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image

from source import OCR
import cv2

class userInterface(Tk):

    filename : object
    text = ""
    image_path = ""
    
    page1 :object
    page2 :object
    page3 :object
    page4 :object
    binaryImage :object
    myOcr :object

    def __init__(self):
        super(userInterface,self).__init__()



        self.title("OCR")
        self.minsize(900,600)
        self.wm_iconbitmap('myicon.ico')
        self.configure(background='#FFFFFF')
        self.createMenu()
        self.createTabs()

        self.train()


    def createTabs(self):
        tab_control = ttk.Notebook(self,width= self.winfo_width(),height=self.winfo_height())
        # ttk.Style().configure("tab_control", background='#FFFFFF', foreground='green')

        self.page1 = ttk.Frame(tab_control)

        tab_control.add(self.page1, text='Train')
        self.page2 = ttk.Frame(tab_control)
        tab_control.add(self.page2, text='Match Template Test')
        self.page3 = ttk.Frame(tab_control)
        tab_control.add(self.page3, text='KNN Test')
        self.page4 = ttk.Frame(tab_control)
        tab_control.add(self.page4, text='SVM Test')
        tab_control.pack(expand=True, fill=BOTH)

        tab_control.grid(column=0, row=0)





    def createMenu(self):
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save as...", )
        filemenu.add_command(label="Close", )

        filemenu.add_separator()  # -------------------------

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
    def train(self):
        self.labelFrame = ttk.LabelFrame(self.page1, text="OCR Steps")

        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)
        # self.DatasetFrame = ttk.LabelFrame(self.page1, text="Dataset")
        self.browseButton = ttk.Button(self.labelFrame, text="Browse" ,command = self.filedialogTrain)
        self.browseButton.grid(column=1, row=1)

        self.preprocessButton = ttk.Button(self.labelFrame, text="Preprocess", command = lambda: self.myOcr.preprocess(self.image_path) and self.segmentationButton.configure(state=NORMAL))


        # cv2.imshow("command donus",self.binaryImage)
        self.preprocessButton.grid(column=1, row=2)
        self.preprocessButton.configure(state=DISABLED)
        self.segmentationButton = ttk.Button(self.labelFrame,
                                  text="Segmentation" )#,command = self.segmentation)
        self.segmentationButton.grid(column=1, row=3)
        self.segmentationButton.configure(state=DISABLED)

        # self.DatasetFrame.grid(column=0, row=2, padx=0, pady=0)
        # if self.filename is not "":
        #     self.Datasetpanel = ttk.Label(self.DatasetFrame, image=img)
        #     self.DatasetFrame.image = img
        #     self.Datasetpanel.grid(column=0, row=0)



    def filedialogTrain(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select a Picture",filetype = (('jpeg','*.jpg'),('png','*.png') ))

        if self.filename is not "":
            self.myOcr = OCR.Ocr()
            self.preprocessButton.configure(state=NORMAL)
            self.image_path = self.filename
            # img = ImageTk.PhotoImage(Image.open(self.image_path))
        else :
            messagebox.showerror("Error", "You did not select any photo! Browse again!")


    def get_ImagePath(self):
        return self.image_path






if __name__ == '__main__':
    myGUI = userInterface()

    myGUI.mainloop()
def getGUI():
    return myGUI