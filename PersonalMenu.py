from Tkinter import Tk, Text, TOP, BOTH, X, N, S, E, W, LEFT, RIGHT, Button, Canvas, IntVar, Toplevel, BOTTOM, Grid, CENTER, Menu, SE, StringVar
from ttk import Frame, Label, Entry, Combobox, Scrollbar, Checkbutton, LabelFrame, Treeview

class PersonalMenu:
    def __init__(self, parent):
        self.parent = parent
        self.Menu()
        

    def Menu(self):
        self.menubar = Menu(self.parent)
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="List", menu=menu)
        menu.add_command(label="Open A Configuration", command=self.Index)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Cut")
        menu.add_command(label="Copy")
        menu.add_command(label="Paste")
        # return self.menubar

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

    