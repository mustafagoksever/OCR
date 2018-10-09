from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class GUI(Tk):


    def __init__(self):
        super(GUI,self).__init__()
        self.title("OCR")
        self.minsize(1080,540)
        self.wm_iconbitmap('myicon.ico')
        self.configure(background = '#4D4D4D')
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
        self.label.configure(text= self.filename)


if __name__ == '__main__':


    myGUI = GUI()
    myGUI.mainloop()

