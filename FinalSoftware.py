""" Imported Tkinter as it is the Base of the application """
from Tkinter import Tk, CENTER, SE, Toplevel, Menu
from ttk import Frame, Combobox, Label, Button, Treeview
import tkMessageBox as MessageBox
import os, sqlite3
from sqlite3 import Error

import OneArmTest
import TwoArmTest

class FinalSoftware(Frame):
    """ Main Class """
    # 
    combobox = None
    count = 0
    Choices = (
        "One Arm Calculation",
        "Two Arm Calculation"
    )

    Connection = None
    

    def __init__(self, parent):
        """ Frame and all widgets are initialized """
        Frame.__init__(self, parent)
        self.parent = parent
        # Connection = FinalSoftware.CreateConnection()
        self.initUI()
        

    @staticmethod
    def CreateConnection():
        WorkingDirectory = os.path.dirname(os.path.realpath(__file__))
        DataDirectory = WorkingDirectory + "/Data/"
        FilePath = None
        if not os.path.isdir(DataDirectory):
            # print WorkingDirectory
            os.makedirs(DataDirectory)
        
        FilePath = DataDirectory + "database.sqlite"

        try:
            if not os.path.isfile(FilePath):
                conn = sqlite3.connect(FilePath)
                
                FinalSoftware.CreateSchema(conn)
            else:
                conn = sqlite3.connect(FilePath)
                # print sqlite3.version
        except Error, e:
            print e
        
        return conn

    @staticmethod
    def CreateSchema(connection):
        """ Will be used to create the Schema of the Database upon first run. """
        SQLStringTableOneArm = " CREATE TABLE IF NOT EXISTS OneArm(OneArmId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, KValue INT, Name TEXT);"
        SQLStringTableTwoArm = "CREATE TABLE IF NOT EXISTS TwoArm(TwoArmId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, KValue INT, Name TEXT);"
        SQLStringTableOneArmValue = "CREATE TABLE IF NOT EXISTS OneArmValue(ArmId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, SignalDesignation TEXT, SignalDistance FLOAT, SignalArea FLOAT, OneArmIdFK INTEGER, FOREIGN KEY(OneArmIdFK) references OneArm(OneArmId) );"
        SQLStringTableTwoArmValue = "CREATE TABLE IF NOT EXISTS TwoArmValue(ArmId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, SignalDesignation TEXT, SignalDistance FLOAT, SignalArea FLOAT, Arm TEXT, TwoArmIdFK INTEGER, FOREIGN KEY(TwoArmIdFK) references TwoArm(TwoArmId) );"
    

        cursor = connection.cursor()
        cursor.execute(SQLStringTableOneArm)
        cursor.execute(SQLStringTableTwoArm)
        cursor.execute(SQLStringTableOneArmValue)
        cursor.execute(SQLStringTableTwoArmValue)


    def Menu(self):
        self.menubar = Menu(self)
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="List", menu=menu)
        menu.add_command(label="Open A Configuration", command=self.Index)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Cut")
        menu.add_command(label="Copy")
        menu.add_command(label="Paste")

        try:
            self.parent.config(menu=self.menubar)
        except:
            print "Uvee"
        

    def Index(self):
        self.parent.withdraw()
        window = Toplevel()
        window.protocol("WM_DELETE_WINDOW",lambda : self.OnClosing(window))
        self.TreeView(window)

    def TreeView(self, window):
        self.tree = Treeview(window)
        self.tree["columns"] = ("name", "K", "Design", "Arms")
        self.tree["show"] = "headings"

        self.tree.bind("<Double-1>", self.onDoubleClick)
        
        self.tree.column("name", width=250, anchor=CENTER)
        self.tree.column("K", anchor=CENTER)
        self.tree.column("Design", anchor=CENTER)
        self.tree.column("Arms", anchor=CENTER)

        self.tree.heading("name", text="Name")
        self.tree.heading("K", text="K value")
        self.tree.heading("Design", text="Design")
        self.tree.heading("Arms", text="Multiple Arms")

        connection = FinalSoftware.CreateConnection()
        cursor = connection.cursor()

        sql = "SELECT * FROM OneArm"
        cursor.execute(sql)
        Rows = cursor.fetchall()

        for row in Rows:
            self.tree.insert("", 0, text=row[0], values=(row[2], row[1], row[3], "No"))

            
        # tree.insert("", 0, text="Hello", values=("1A", "1B"))

        sql = "SELECT * FROM TwoArm"
        cursor.execute(sql)
        Rows = cursor.fetchall()

        for row in Rows:
            self.tree.insert("", 0, text=row[0], values=(row[2], str(row[1])+", "+str(row[3]), row[4], "Yes"))
        
        self.tree.pack()



    def initUI(self):
        """
        This method initializes all widgets big or
        small and gives the look to the entire application
        """
        self.parent.title("GUI Application")
        # FinalSoftware.Connection = self.CreateConnection()
        # print FinalSoftware.Connection
        # self.Menu()

        label = Label(self.parent, text="Select Program Calculation Method")
        label.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.combobox = Combobox(self.parent, values=self.Choices, state='readonly', width=23)
        self.combobox.place(relx=0.5, rely=0.5, anchor=CENTER)
        button = Button(self.parent, text="Next", command=self.Decision)
        button.place(relx=0.95, rely=0.9, anchor=SE)

    def Decision(self):
        value = self.combobox.get() 
        if value == "One Arm Calculation":
            self.parent.withdraw()
            window = Toplevel()
            window.protocol("WM_DELETE_WINDOW",lambda : self.OnClosing(window))
            window.title("GUI Application")
            window.iconbitmap('favicon.ico')
            window.geometry("1050x500+200+100")
            # window.geometry('{}x{}'.format(1000, 300))
            window.tk_strictMotif()
            app = OneArmTest.OneArm(window)
            app.Center(app.parent)

        elif value == "Two Arm Calculation":
            self.parent.withdraw()
            window = Toplevel()
            window.protocol("WM_DELETE_WINDOW", lambda : self.OnClosing(window))
            window.geometry("1050x600+200+100")
            # window.resizable(0,0)
            window.tk_strictMotif()
            window.iconbitmap('favicon.ico')
            app = TwoArmTest.TwoArm(window)
            app.Center(app.parent)
        
        else:
            # self.parent.withdraw()
            # window = Toplevel()
            # self.TreeView(window)
            pass

    
    
    def OnClosing(self, window):
        """ Some yes no inputs regarding exit or Previous step """
        # if self.count == 0:
        #     self.count = 1
        # dialog = MessageBox.askyesno("How To Proceed", "Do you want to go back?", parent=window)
        # if dialog:
        #     window.destroy()
        #     self.parent.deiconify()
        #     return
        # else:
        Sure = MessageBox.askokcancel("Quit", "The Application will be closed", icon='warning')
        if Sure:
            self.parent.destroy()
            self.parent.quit()
        # self.count = 0

    def onDoubleClick(self, event):
        item = self.tree.selection()[0]
        # print ("You Clicked On ", str(self.tree.item(item, "text")))
        Value = []
        Value.append(str(self.tree.item(item, "text")))
        
        Connection = FinalSoftware.CreateConnection()
        Cursor = Connection.cursor()

        Cursor.execute("SELECT * FROM OneArmValue WHERE OneArmIdFK = ?", Value)
        ResultSet = Cursor.fetchall()

        window = Toplevel()
        # window.protocol("WM_DELETE_WINDOW",lambda : self.OnClosing(window))
        window.title("GUI Application")
        window.iconbitmap('favicon.ico')
        window.geometry("1050x500+200+100")
        app = OneArmTest.OneArm(window)
        app.WritingScript(ResultSet)
        app.setKVal()
        app.setDesign()


def main():
    root = Tk()
    root.geometry("400x100+500+300")
    root.resizable(0,0)
    root.tk_strictMotif()
    root.iconbitmap('favicon.ico')
    FinalSoftware(root)
    root.mainloop()

if __name__ == '__main__':
    main()  

