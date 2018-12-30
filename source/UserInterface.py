from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import numpy as np
from source import OCR
import cv2


class userInterface(Tk):
    filename: object
    text = ""
    image_path = ""
    counter = 0
    page1: object
    page2: object
    page3: object
    page4: object
    binaryImage: object
    myOcr: object
    DatasetFrame: object
    DatasetFrameMatch: object
    DatasetFrameKNN: object

    a: object

    def __init__(self):
        super(userInterface, self).__init__()
        self.a = 0

        self.title("OCR")
        self.minsize(900, 600)
        self.maxsize(900, 600)

        self.wm_iconbitmap('myicon.ico')
        self.configure(background='#FFFFFF', )
        self.createMenu()
        self.createTabs()

        self.train()
        self.matchTemplate()
        self.KNN()

    def createTabs(self):
        tab_control = ttk.Notebook(self, width=self.winfo_width(), height=self.winfo_height())
        # ttk.Style().configure("tab_control", background='#FFFFFF', foreground='green')

        self.page2 = ttk.Frame(tab_control)
        tab_control.add(self.page2, text='Match Template Test')
        self.page1 = ttk.Frame(tab_control)
        tab_control.add(self.page1, text='Train')
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
        filemenu.add_command(label="Close", )

        filemenu.add_separator()  # -------------------------

        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)

        editmenu.add_separator()

        editmenu.add_command(label="Cut")
        editmenu.add_command(label="Copy")
        editmenu.add_command(label="Paste")
        editmenu.add_command(label="Delete")

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index")
        helpmenu.add_command(label="About...")
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.config(menu=menubar)

    def Clear(self, method, frameName):
        method()
        frameName.destroy()

    def train(self):
        self.browseButtonTrain = ttk.Button(self.page1, text="Browse",
                                            command=lambda: self.filedialog(frame=self.DatasetFrame,
                                                                            btn=self.preprocessButton))
        #self.browseButton = ttk.Button(self.page1, text="Browse", command=self.filedialogTrain)
        # self.browseButton.pack()
        self.browseButtonTrain.place(x=20, y=20)
        self.DatasetFrame = ttk.LabelFrame(self.page1, text="Dataset")

        self.preprocessButton = ttk.Button(self.page1, text="Preprocess", command=lambda: [self.myOcr.preprocess(),
                                                                                           self.segmentationButton.configure(
                                                                                               state=NORMAL)])
        self.preprocessButton.configure(state=DISABLED)
        self.preprocessButton.place(x=20, y=60)

        # enter binding yap
        self.segmentationButton = ttk.Button(self.page1,
                                             text="Segmentation", command=lambda: self.myOcr.segmentation())
        self.segmentationButton.bind('<Button-1>', self.entryEnable)
        self.segmentationButton.configure(state=DISABLED)
        self.segmentationButton.place(x=20, y=100)

        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
        self.entry = ttk.Entry(self.page1, textvariable=sv)
        self.entry.configure(state=DISABLED)

        # self.entry.set(self.entry.get()[:1])
        self.entry.place(x=20, y=140)
        self.exitButton = ttk.Button(self.page1,
                                     text="Exit", command=sys.exit)
        self.exitButton.place(x=800, y=500)

        # self.clipboard_clear()
        self.clearButton = ttk.Button(self.page1, text="Clear",
                                      command=lambda: self.Clear(method=self.train, frameName=self.DatasetFrame))
        self.clearButton.place(x=700, y=400)

    def newmethod(self, event):
        self.a = 1
        self.entry.delete(0, END)
        print("enter")
        self.update()

    def callback(self, sv):
        c = sv.get()[0:1]
        sv.set(c)

    def entryEnable(self, event):
        self.entry.configure(state=NORMAL)

    def matchTemplate(self):
        self.browseButtonMatch = ttk.Button(self.page2, text="Browse", command=lambda: self.filedialog(frame=self.DatasetFrameMatch,
                                                                                                       btn=self.testButton1))
       # self.browseButtonMatch = ttk.Button(self.page2, text="Browse", command=self.filedialogMatch)
        self.browseButtonMatch.place(x=20, y=20)
        self.DatasetFrameMatch = ttk.LabelFrame(self.page2, text="Dataset")
        self.exitButton = ttk.Button(self.page2,
                                     text="Exit", command=sys.exit)
        self.exitButton.place(x=800, y=500)
        self.testButton1 = ttk.Button(self.page2,
                                      text="Test", command=lambda: self.myOcr.matchTemplate())
        self.testButton1.configure(state=DISABLED)
        self.testButton1.place(x=20, y=60)

        # self.clipboard_clear()
        self.clearButton = ttk.Button(self.page2, text="Clear",
                                      command=lambda: self.Clear(method=self.matchTemplate,
                                                                 frameName=self.DatasetFrameMatch))
        self.clearButton.place(x=700, y=400)

    def KNN(self):
        self.browseButtonKNN = ttk.Button(self.page3, text="Browse",
                                            command=lambda: self.filedialog(frame=self.DatasetFrameKNN,
                                                                            btn=self.testButton2))
        #self.browseButtonKNN = ttk.Button(self.page3, text="Browse", command=self.filedialogKNN)
        self.browseButtonKNN.place(x=20, y=20)

        self.exitButton = ttk.Button(self.page3,
                                     text="Exit", command=sys.exit)
        self.exitButton.place(x=800, y=500)
        self.DatasetFrameKNN = ttk.LabelFrame(self.page3, text="Dataset")
        self.testButton2 = ttk.Button(self.page3,
                                      text="Test", command=lambda: self.myOcr.kNearest())
        self.testButton2.place(x=20, y=60)
        self.testButton2.configure(state=DISABLED)

        self.clearButton = ttk.Button(self.page3, text="Clear",
                                      command=lambda: self.Clear(method=self.KNN, frameName=self.DatasetFrameKNN))
        self.clearButton.place(x=700, y=400)

        self.exitButton = ttk.Button(self.page3,
                                     text="Exit", command=sys.exit)
        self.exitButton.place(x=800, y=500)



    def filedialog(self, frame , btn):

        self.filename = filedialog.askopenfilename(initialdir="/", title="Select a Picture",
                                                   filetype=(('jpeg', '*.jpg'), ('png', '*.png')))
        if self.filename is "":
            messagebox.showerror("Error", "You did not select any photo! Browse again!")
        else:
            self.myOcr = OCR.Ocr(filename=self.filename, gui=myGUI)
            selectedImage = self.imageOpen(self.filename)
            self.showDatasetfromImage(selectedImage, frame)
            self.image_path = self.filename
            btn.configure(state=NORMAL)

    def showDatasetfromImage(self, image, frame):

        self.Datasetpanel = ttk.Label(frame, image=image)
        self.Datasetpanel.grid(column=0, row=0)
        frame.place(x=20, y=200)
        frame.image = (image)

    def get_ImagePath(self):
        return self.image_path

    def imageOpen(self,filename):
        image = Image.open(filename)
        image = image.resize((600, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        return img



  ## def filedialogMatch(self):

  #     self.filename = filedialog.askopenfilename(initialdir="/", title="Select a Picture",
  #                                                filetype=(('jpeg', '*.jpg'), ('png', '*.png')))
  #     if self.filename is "":
  #         messagebox.showerror("Error", "You did not select any photo! Browse again!")
  #     else:
  #         self.myOcr = OCR.Ocr(filename=self.filename, gui=myGUI)
  #         selectedImage = self.imageOpen(self.filename)
  #         self.showDatasetfromImage(selectedImage , self.DatasetFrameMatch)
  #         #self.showDatasetFromFileNameMatch(self.filename)
  #         self.image_path = self.filename
  #         self.testButton1.configure(state=NORMAL)
  #         # img = ImageTk.PhotoImage(Image.open(self.image_path))

  # def filedialogKNN(self):

  #     self.filename = filedialog.askopenfilename(initialdir="/", title="Select a Picture",
  #                                                filetype=(('jpeg', '*.jpg'), ('png', '*.png')))
  #     if self.filename is "":
  #         messagebox.showerror("Error", "You did not select any photo! Browse again!")
  #     else:
  #         self.myOcr = OCR.Ocr(filename=self.filename, gui=myGUI)
  #         openedImage = self.imageOpen(self.filename)
  #         self.showDatasetfromImage(openedImage , self.DatasetFrameKNN)
  #         #self.showDatasetFromFileNameKNN(self.filename)
  #         self.image_path = self.filename
  #         self.testButton2.configure(state=NORMAL)
  #         # img = ImageTk.PhotoImage(Image.open(self.image_path))

  # def filedialogTrain(self):

  #     self.filename = ""
  #     self.filename = filedialog.askopenfilename(initialdir="/", title="Select a Picture",
  #                                                filetype=(('jpeg', '*.jpg'), ('png', '*.png')))

  #     if self.filename is "":
  #         messagebox.showerror("Error", "You did not select any photo! Browse again!")

  #     else:
  #         self.myOcr = OCR.Ocr(filename=self.filename, gui=myGUI)
  #         selectedImage = self.imageOpen(self.filename)
  #         self.showDatasetfromImage(selectedImage, self.DatasetFrame)
  #         self.image_path = self.filename
  #         self.preprocessButton.configure(state=NORMAL)

 #   def showDatasetFromFileName(self, filename, frame):
#
 #       img = self.imageOpen(filename)
 #       self.Datasetpanel = ttk.Label(frame, image=img)
 #       self.Datasetpanel.grid(column=0, row=0)
 #       frame.place(x=20, y=200)
 #       frame.image = (img)



  # #def showDatasetFromFileNameMatch(self, filename):

   #    image = Image.open(filename)
   #    image = image.resize((600, 200))
   #    image = ImageTk.PhotoImage(image)
   #    self.Datasetpanel = ttk.Label(self.DatasetFrameMatch, image=image)
   #    self.Datasetpanel.grid(column=0, row=0)
   #    self.DatasetFrameMatch.place(x=20, y=200)
   #    self.DatasetFrameMatch.image = (image)

   ##def showDatasetfromImageMatch(self, imageParam):

   #    imageParam = cv2.resize(imageParam, (600, 200))

   #    image = Image.fromarray(imageParam)

   #    image = ImageTk.PhotoImage(image)

   #    self.Datasetpanel = ttk.Label(self.DatasetFrameMatch, image=image)
   #    self.Datasetpanel.grid(column=0, row=0)
   #    self.DatasetFrameMatch.place(x=20, y=200)
   #    self.DatasetFrameMatch.image = (image)



    #   def showDatasetfromImageKNN(self, imageParam):
    #
    #       imageParam = cv2.resize(imageParam, (600, 200))
    # #      image = Image.fromarray(imageParam)
    #
    #       image = ImageTk.PhotoImage(image)
    #
    #       self.Datasetpanel = ttk.Label(self.DatasetFrameKNN, image=image)
    #       self.Datasetpanel.grid(column=0, row=0)
    #       self.DatasetFrameKNN.place(x=20, y=200)
    #       self.DatasetFrameKNN.image = (image)


  #  def showDatasetFromFileNameKNN(self, filename):
  #      image = Image.open(filename)
  #      image = image.resize((600, 200), Image.ANTIALIAS)
  #      img = ImageTk.PhotoImage(image)
  #      self.Datasetpanel = ttk.Label(self.DatasetFrameKNN, image=img)
  #      self.Datasetpanel.grid(column=0, row=0)
  #      self.DatasetFrameKNN.place(x=20, y=200)
  #      self.DatasetFrameKNN.image = (img)


if __name__ == '__main__':
    myGUI = userInterface()

    myGUI.mainloop()


def getGUI():
    return myGUI
