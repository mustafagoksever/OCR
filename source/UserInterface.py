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
    counter =0
    page1 :object
    page2 :object
    page3 :object
    page4 :object
    binaryImage :object
    myOcr :object
    DatasetFrame :object
    def __init__(self):
        super(userInterface,self).__init__()



        self.title("OCR")
        self.minsize(900,600)
        self.maxsize(900,600)

        self.wm_iconbitmap('myicon.ico')
        self.configure(background='#FFFFFF',)
        self.createMenu()
        self.createTabs()

        self.train()
        self.matchTemplate()

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

        self.browseButton = ttk.Button(self.page1, text="Browse" ,command = self.filedialogTrain)
        # self.browseButton.pack()
        self.browseButton.place(x=20,y=20)
        self.DatasetFrame = ttk.LabelFrame(self.page1, text="Dataset")


        self.preprocessButton = ttk.Button(self.page1, text="Preprocess", command = lambda: [self.myOcr.preprocess() , self.segmentationButton.configure(state=NORMAL)] )
        self.preprocessButton.configure(state=DISABLED)
        self.preprocessButton.place(x=20,y=60)



        # enter binding yap
        self.segmentationButton = ttk.Button(self.page1,
                                  text="Segmentation" ,command =lambda: self.myOcr.segmentation() )
        self.segmentationButton.bind('<Button-1>',self.entryEnable)
        self.segmentationButton.configure(state=DISABLED)
        self.segmentationButton.place(x=20,y=100)


        self.entry = ttk.Entry(self.page1, text="character")
        self.entry.configure(state=DISABLED)
        self.entry.place(x=20,y=140)
        self.exitButton = ttk.Button(self.page1,
                                     text="Exit", command=sys.exit)
        self.exitButton.place(x=800,y=500)
        self.state = ttk.Label(self.page1,text="Mustafa")
        self.state.place(x=200,y=20)






    def entryEnable(self,event):
        self.entry.configure(state=NORMAL)

    def matchTemplate(self):
        self.browseButtonMatch = ttk.Button(self.page2, text="Browse", command=self.filedialogMatch)
        self.browseButtonMatch.grid(column=1, row=1)


    def filedialogMatch(self):

        self.filename = filedialog.askopenfilename(initialdir="/", title="Select a Picture",
                                                   filetype=(('jpeg', '*.jpg'), ('png', '*.png')))
        if self.filename is not None:
            messagebox.showerror("Error", "You did not select any photo! Browse again!")
        else:
            self.myOcr = OCR.Ocr(filename=self.filename)
            self.showDataset(self.filename)
            self.image_path = self.filename
            # img = ImageTk.PhotoImage(Image.open(self.image_path))


    def showDataset(self,filename):
        # img = ImageTk.PhotoImage(Image.open(filename))
        # if self.counter == 0:
        #     self.Datasetpanel = ttk.Label(self.DatasetFrame, image=img)
        #     self.Datasetpanel.grid(column=0, row=0)
        #     self.DatasetFrame.place(x=20, y=200)
        #     print("ilk resim olustu")
        # self.DatasetFrame.image = (img)
        # print(filename)
        # print(self.counter)
        # self.counter=self.counter+1
        # ikinci browse yaptiginda eski nesneyi silcek yeniden eklicek
        image = Image.open(filename)
        image = image.resize((300, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        self.Datasetpanel = ttk.Label(self.DatasetFrame, image=img)
        self.Datasetpanel.grid(column=0, row=0)
        self.DatasetFrame.place(x=20, y=200)
        self.DatasetFrame.image = (img)



    def filedialogTrain(self):

        self.filename=""
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select a Picture",filetype = (('jpeg','*.jpg'),('png','*.png') ))

        if self.filename is "":
            messagebox.showerror("Error", "You did not select any photo! Browse again!")

        else:
            self.myOcr = OCR.Ocr(filename=self.filename)



            self.state.config(text="ocr objesi olustu")
            self.showDataset(self.filename)
            self.preprocessButton.configure(state=NORMAL)


    def get_ImagePath(self):
        return self.image_path






if __name__ == '__main__':
    myGUI = userInterface()

    myGUI.mainloop()
def getGUI():
    return myGUI