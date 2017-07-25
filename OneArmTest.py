from Tkinter import Tk, Text, TOP, BOTH, X, N, S, E, W, LEFT, RIGHT, Button, Canvas, IntVar, Toplevel, BOTTOM, Grid, CENTER, SE, Menu, StringVar
from ttk import Frame, Label, Entry, Combobox, Scrollbar, Checkbutton, LabelFrame, Treeview
import csv
import math
import xlsxwriter
import tkFileDialog as filedialog
import tkMessageBox as MessageBox
import sqlite3
import os
import datetime
from functools import partial

from FinalSoftware import FinalSoftware
from TwoArmTest import TwoArm
from PersonalMenu import PersonalMenu

class OneArm(Frame):
    rowNum = 0
    SignalDesignation = []
    SignalDistance = []
    SignalArea = []
    Buttons = []
    MinusButtons = []
    IsSignalCheckButton = []
    IsSignal = []
    Areas = []
    SignArea = []
    Table1 = []
    Table2 = []
    K = 0
    AreaOfSignal = 0
    MaxDistance = 0
    Headers = []
    KVal = None
    DesignLabel = None
    Design = 0
    name = ""
    NameLabel = None

    WorkingDirectory = os.path.dirname(os.path.realpath(__file__))
    DataDirectory = WorkingDirectory + "/Data/"

    with open(DataDirectory+'/Areas For Signal Heads.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, quotechar='|')
        for row in spamreader:
            if "Signal Head Type" in row:
                continue
            elif "Inches" in row:
                Headers.append(row)
                continue
            else:
                Areas.append(row)

    # print Areas

    with open(DataDirectory+'Table1.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if "Design No." in row:
                continue
            else:
                Table1.append(row)

    # print Areas
    with open(DataDirectory+'Table2.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if "Design No." in row:
                continue
            else:
                Table2.append(row)

    # print Areas

    SignalHeadType = []
    # SignalHeadType = (
        # "1 Section -- 8",
        # "3 Sections -- 8",
        # "4 Sections -- 8",
        # "5 Sections - Vertical -- 8",
        # "5 Sections - Cluster -- 8",
        # "5 Sections - Mixed -- 8",
        # "1 Section -- 12",
        # "3 Sections -- 12",
        # "4 Sections -- 12",
        # "5 Sections - Vertical -- 12",
        # "5 Sections - Cluster -- 12",
        # "5 Sections - Mixed -- 12"
    # )

    for i in range(len(Areas)):
        for j in range(1, len(Headers[0])):
            # print "YO"
            SignalHeadType.append(Areas[i][0]+" -- "+str(Headers[0][j]))


    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        rowNum = 0
        self.SignalDesignation = []
        self.SignalDistance = []
        self.SignalArea = []
        self.Buttons = []
        self.IsSignalCheckButton = []
        self.IsSignal = []
        self.SignArea = []
        self.MinusButtons = []
        self.K = 0
        self.AreaOfSignal = 0
        self.MaxDistance = 0
        self.initUI()
        self.KVal = Label(self.frame)
        self.Design = 0
        self.DesignLabel = Label(self.frame)
        self.NameLabel = Label(self.frame)
        self.name = ""

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta/120), "units")

    def Calculation(self, flag):
        
        self.MaxDistance = 0
        DistanceFromPoleToSignal = 0
        self.K = 0
        
        try:
            for i in range(len(self.SignalDesignation)):
                DistanceFromPoleToSignal = self.SignalDistance[i].get()
                if self.SignalDistance[i].get() == "":
                    DistanceFromPoleToSignal = '0'
                if self.MaxDistance < float(DistanceFromPoleToSignal):
                    self.MaxDistance = float(DistanceFromPoleToSignal)
                
                value = self.SignalArea[i].get()

                if self.IsSignal[i] == 1:
                    # print value
                    ValueArray = value.split("--")
                    index = [(ind, self.Areas[ind].index(ValueArray[0].strip())) for ind in xrange(len(self.Areas)) if ValueArray[0].strip() in self.Areas[ind]]
                    if ValueArray[1].strip() == '8':
                        # print self.Areas[index[0][0]][1]
                        value = float(self.Areas[index[0][0]][1])
                    else:
                        value = float(self.Areas[index[0][0]][2])
                else:
                    if self.SignalArea[i].get() == "":
                        value = '0'
                
                
                self.AreaOfSignal += float(value)
                AreaMomentDesign = float(DistanceFromPoleToSignal)*float(value)
                self.K += AreaMomentDesign

        except ValueError, e:
            MessageBox.showerror("Error", message=str(e))
            return

        v = self.DesignChoice()
        self.Design = str(v[0])

        if flag:
            self.Output()
        

    def Output(self):
        
        dlg = Toplevel(master=self.parent)
        
        dlg.iconbitmap('favicon.ico')
        frame = Frame(dlg)
        frame.pack(fill='both', expand=True)
        frame2 = Frame(dlg, borderwidth=1, relief="ridge")
        frame2.pack(fill='both', side=BOTTOM)
        # self.Center(self.parent)
        msg = "K is : "+str(int(math.ceil(self.K)))
        msg2 = "Use Design : "
        v = self.DesignChoice()
        if v is None:
            v[0] = 0
        self.Design = v[0]
        msg3 = msg2+str(v[0])
        label = Label(frame, text=msg)
        label.grid(row=1, column=3, columnspan=15, pady=15, padx=15)
        label.config(font=("Courier, 26"))
        label2 = Label(frame, text=msg3)
        label2.grid(row=2, column=3, columnspan=10, pady=15, padx=15)
        label2.config(font=("Courier, 23"))

        btn = Button(frame2, text="End Program", command=self.parent.quit)
        btn.pack(side=RIGHT, padx=15, pady=6)
        Button(frame2, text="Save To Database", command=self.SaveToDatabase).pack(side=RIGHT, padx=15, pady=6)
        Button(frame2, text="Write to Excel File", command= lambda: self.WriteToExcelFile(dlg)).pack(side=RIGHT, padx=15, pady=6)
        # dlg.transient(self.parent)
        self.setKVal()
        self.setDesign()
        self.setName()
        self.Center(dlg)
        dlg.grab_set()


    def SaveToDatabase(self):
        dlg = Toplevel(master=self.parent)
        dlg.geometry("350x150")
        dlg.iconbitmap('favicon.ico')
        frame = Frame(dlg)
        frame.pack(fill='both', expand=True)
        # frame.place(height=100, width=300)

        label = Label(frame, text="Save To Database As...")
        label.place(relx=0.5, rely=0.3, anchor=CENTER)
        entry = Entry(frame, width=50)
        entry.place(relx=0.5, rely=0.5, anchor=CENTER)

        button = Button(frame, text="Save", command=partial(self.SaveToDatabaseContinued, entry, dlg))
        button.place(relx=0.95, rely=0.9, anchor=SE)
        # dlg.transient(self.parent)
        dlg.grab_set()
        self.Center(dlg)

    def SaveToDatabaseContinued(self, entry, dlg):
        SaveAs = entry.get()
        dlg.destroy()
        Conn = FinalSoftware.CreateConnection()
        # print Conn
        cursor = Conn.cursor()
        
        task = (0, str(SaveAs), 0)
        sql = "Insert into OneArm(KValue, Name, Design) Values (?,?, ?);"
        InsertId = None
        try:
            cursor.execute(sql, task)
            Conn.commit()
            InsertId = cursor.lastrowid
            # print InsertId
        except:
            Conn.rollback()

        sql = "Insert into OneArmValue(SignalDesignation, SignalDistance, SignalArea, OneArmIdFK) Values (?,?,?,?);"
        
        for i in range(len(self.SignalDesignation)):
            SignalDesign = self.SignalDesignation[i].get()
            SignalDistance = self.SignalDistance[i].get()
            
            #TODO Calculate Area based on signal selected Done
            value = self.SignalArea[i].get()
            if self.IsSignal[i] == 1:
                ValueArray = value.split("--")
                index = [(ind, self.Areas[ind].index(ValueArray[0].strip())) for ind in xrange(len(self.Areas)) if ValueArray[0].strip() in self.Areas[ind]]
                if ValueArray[1].strip() == '8':
                    # print self.Areas[index[0][0]][1]
                    value = float(self.Areas[index[0][0]][1])
                else:
                    value = float(self.Areas[index[0][0]][2])
            else:
                if self.SignalArea[i].get() == "":
                    value = '0'
            
            SignalArea = value

            task = (SignalDesign, SignalDistance, SignalArea, InsertId)

            try:
                cursor.execute(sql, task)
                Conn.commit()
                # MessageBox.showinfo("Success", "The data has been successfully entered into the database.")
            except:
                # print "another yo"
                Conn.rollback() 
        
        try:
            task = (self.K, self.Design, InsertId)
            cursor.execute("UPDATE OneArm SET KValue = ?, Design = ? WHERE OneArmId = ?;", task)
            Conn.commit()
            MessageBox.showinfo("Success", "The data has been successfully entered into the database.")
        except Exception, e:
            # print e
            # print "yo"
            Conn.rollback()
                
        Conn.close()



    def Center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        # print size
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size[0], size[1], x, y))


    def DesignChoice(self):
        ReturnValue = None
        for i in self.Table1:
            if self.MaxDistance+2 < float(i[2]):
                # MaxChoice.append(i)                      
                if self.K < float(i[1]):
                    ReturnValue = i
                    break
                else:
                    continue
        
        if ReturnValue is None:
            ReturnValue = []
            ReturnValue.append("N/A")
            return ReturnValue

        return ReturnValue
        

    def WriteToExcelFile(self, window):
        window.destroy()
        try:
            xlFilePath = filedialog.asksaveasfilename(initialdir=self.DataDirectory, title="Select File", filetypes=(("Excel Files", "*.xlsx"),))
            # print xlFilePath
            if '.' in xlFilePath:
                workbook = xlsxwriter.Workbook(xlFilePath)
            elif xlFilePath is '':
                return
            else: 
                workbook = xlsxwriter.Workbook(xlFilePath+".xlsx")

            worksheet = workbook.add_worksheet()

            MergeFormat = workbook.add_format({
                'bold' : 1,
                'border' : 1,
                'align' : 'center'
            })

            BorderFormat = workbook.add_format({
                'border' : 1
            })

            worksheet.set_column(0, 0, 15)
            worksheet.set_column(0, 1, 23)
            worksheet.set_column(0, 2, 20)
            worksheet.set_column(0, 3, 20)

            WrapText = workbook.add_format()
            WrapText.set_text_wrap()
            WrapText.set_border()

            Heading = []
            Heading.append("Signal Or Sign Designation")
            Heading.append("Distance from Pole to Signal or Sign")
            Heading.append("Area of Signal or Sign")
            Heading.append("Area Moment Design Factor")
            

            worksheet.merge_range("A1:F1", self.name, MergeFormat)

            import time

            TimeStamp = time.time()
            DateTime = datetime.datetime.fromtimestamp(TimeStamp).strftime('%m/%d/%Y %H:%M:%S')
            # print DateTime

            worksheet.set_column(5, 5, 25)
            # worksheet.set_column(7, 7, 27)

            worksheet.write_string(2, 5, "Generated By Software", WrapText)
            worksheet.write_string(3, 5, "Generated On : "+DateTime, WrapText)
            
            worksheet.write_string(5, 0, Heading[0], WrapText)
            worksheet.write_string(5, 1, Heading[1], WrapText)
            worksheet.write_string(5, 2, Heading[2], WrapText)
            worksheet.write_string(5, 3, Heading[2], WrapText)

            CurrentRow = 6

            Items = []
            for item in range(len(self.SignalDesignation)):
                ItemRow = []
                ItemRow.append(self.SignalDesignation[item].get())
                ItemRow.append(self.SignalDistance[item].get())
                ItemRow.append(self.SignalArea[item].get())
                AreaMoment = float(self.SignalDistance[item].get()) * float(self.SignalArea[item].get())
                ItemRow.append(AreaMoment)
                Items.append(ItemRow)

            for designation, distance, area, areamoment in Items:
                worksheet.write_string(CurrentRow, 0, designation, BorderFormat)
                worksheet.write_number(CurrentRow, 1, float(distance), BorderFormat)
                worksheet.write_number(CurrentRow, 2, float(area), BorderFormat)
                worksheet.write_number(CurrentRow, 3, areamoment, BorderFormat)
                CurrentRow += 1    

            CurrentRow += 1
            
            worksheet.write_string(CurrentRow, 0, "K", MergeFormat)
            # worksheet.write_number(CurrentRow, 1, float(self.K), BorderFormat)

            from xlsxwriter.utility import xl_rowcol_to_cell
            cell = xl_rowcol_to_cell(CurrentRow, 1)

            worksheet.write(cell, '=SUM(D7:D13)', BorderFormat)


            CurrentRow += 1
            
            worksheet.write_string(CurrentRow, 0, "Use Design", MergeFormat)
            worksheet.write_number(CurrentRow, 1, float(self.Design), BorderFormat)

            workbook.close()
            MessageBox.showinfo("Success", "The data has been successfully written to the File.")

        except IOError, e:
            MessageBox.showerror("Error", message=str(e))
        
        except Exception, e:
            MessageBox.showerror("Error", message=str(e))


    def ClickOnSignal(self, index,b):
        value = b.get()
        if value == 0:
            AreaEntry = Entry(self.frame)
            AreaEntry.grid(row = index, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
            self.IsSignal[index-1] = 0
            self.SignalArea[index-1] = AreaEntry
        else:
            entry3 = Combobox(self.frame, values = self.SignalHeadType, state ='readonly', width = 23)
            entry3.current(0)
            entry3.grid(row = index, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
            self.IsSignal[index-1] = 1
            self.SignalArea[index-1] = entry3

    def onResize(self, event):
        canvas_width = event.width
        canvas_height = event.height
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def OnClosing(self, window):
        """ Some yes no inputs regarding exit or Previous step """
        dialog = MessageBox.askyesno("How To Proceed", "Do you want to go back to One Arm?", parent=self.parent)
        if dialog:
            window.destroy()
            self.parent.deiconify()
            return
        else:
            Sure = MessageBox.askokcancel("Quit", "The Application will be closed", icon='warning')
            if Sure:
                window.destroy()
                self.parent.quit()

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
        window.iconbitmap('favicon.ico')
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

        sql = "SELECT * FROM TwoArm"
        cursor.execute(sql)
        Rows = cursor.fetchall()

        for row in Rows:
            self.tree.insert("", 0, text=row[0], values=(row[2], str(row[1])+", "+str(row[3]), row[4], "Yes"))
        
        self.tree.pack()
    
    def onDoubleClick(self, event):
        
        item = self.tree.selection()[0]
        Value = []
        Value.append(str(self.tree.item(item, "text")))

        Items = []
        Items.append(self.tree.item(item, "values"))

        flag = Items[0][3]

        if flag == "No":
            Connection = FinalSoftware.CreateConnection()
            Cursor = Connection.cursor()

            Cursor.execute("SELECT * FROM OneArmValue WHERE OneArmIdFK = ?", Value)
            ResultSet = Cursor.fetchall()

            window = Toplevel()
            self.destroy()
            # window.protocol("WM_DELETE_WINDOW",lambda : self.OnClosing(window))
            window.title("GUI Application")
            window.iconbitmap('favicon.ico')
            window.geometry("1050x500+200+100")
            app = OneArm(window)
            app.WritingScript(ResultSet)

            Cursor.execute("SELECT name FROM OneArm WHERE OneArmId = ?", Value)
            ResultSet = Cursor.fetchall()

            for row in ResultSet:
                app.name = row[0]

            app.setKVal()
            app.setDesign()
            app.setName()
        
        else:
            Connection = FinalSoftware.CreateConnection()
            Cursor = Connection.cursor()

            Cursor.execute("SELECT * FROM TwoArmValue WHERE TwoArmIdFK = ? AND Arm = 'A';", Value)
            ResultSet = Cursor.fetchall()

            window = Toplevel()
            self.destroy()
            # window.protocol("WM_DELETE_WINDOW",lambda : self.OnClosing(window))
            window.title("GUI Application")
            window.iconbitmap('favicon.ico')
            window.geometry("1050x500+200+100")
            app = TwoArm(window)
            app.WritingScript(ResultSet, "Top")

            Cursor.execute("SELECT * FROM TwoArmValue WHERE TwoArmIdFK = ? AND Arm = 'B';", Value)
            ResultSet = Cursor.fetchall()
            app.WritingScript(ResultSet, "Bottom")
               

            Cursor.execute("SELECT name FROM TwoArm WHERE TwoArmId = ?", Value)
            ResultSet = Cursor.fetchall()

            for row in ResultSet:
                app.name = row[0]          
            

            app.setName()
            # app.setKVal()
            app.setDesign()

    def setKVal(self):
        self.KVal.destroy()
        # self.KVal = None
        LabelText = StringVar()
        LabelText.set("K Value: "+str(self.K))
        self.KVal = Label(self.frame, text=LabelText.get())
        self.KVal.config(font=("Helvetica, 15"))
        self.KVal.grid(row=3000, column=0, columnspan=3, padx=20, pady=15)

    def setDesign(self):
        self.DesignLabel.destroy()
        LabelText = StringVar()
        LabelText.set("Use Design: "+str(self.Design))
        self.DesignLabel = Label(self.frame, text=LabelText.get())
        self.DesignLabel.config(font=("Helvetica, 15"))
        self.DesignLabel.grid(row=3000, column=7, columnspan=2, padx=20, pady=15)

    def setName(self):
        
        self.NameLabel.destroy()
        LabelText = StringVar()
        LabelText.set(str(self.name))
        # print LabelText.get()
        self.parent.title(LabelText.get())
        self.NameLabel = Label(self.frame, text=LabelText.get())
        self.NameLabel.config(font=("Helvetica, 12"))
        self.NameLabel.grid(row=3000, column=2, columnspan=3, padx=20, pady=15)


    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    
    def WritingScript(self, data):
        rowNumber = 0
        count = 0
        for row in data:
            # print row
            if count != 0:
                self.AddButtonClicked()
            self.SignalDesignation[rowNumber].insert(0, row[1])
            self.SignalDistance[rowNumber].insert(0, row[2])
            self.SignalArea[rowNumber].insert(0, row[3])
            rowNumber += 1
            # SignalDesignation[rowNumber].insert(0, row[1])
            count += 1
            
        self.Calculation(False)



    def initUI(self):
        self.parent.title("GUI Application")
        self.Menu()
        # self.menu = PersonalMenu(self.parent)
        # x = menu.Menu()
        # self.menu = x
        self.canvas = Canvas(self.parent, relief="raised", borderwidth=1)
        self.frame = Frame(self.canvas, borderwidth=1, relief="sunken")
        
        self.vsb = Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="both", expand=0)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_frame = self.canvas.create_window((2,2), window=self.frame, anchor="nw", tags="self.frame", width=int(self.canvas.winfo_width()-1))
        # self.frame.pack(fill="both", side="top")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onResize)
        # self.frame.pack_propagate(0)
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

        headingLabel = Label(self.frame, text="Program to Calculate 'K'")
        headingLabel.config(font=("Courier, 26"))
        headingLabel.grid(row=self.rowNum, column=1, columnspan=6, pady=20, padx=15)
        self.rowNum += 1
        
        CalculateButton = Button(self.frame, text = "Calculate K", command=lambda:self.Calculation(True))
        CalculateButton.grid(row=0, column=8, pady=10, columnspan=3)

        lbl1 = Label(self.frame, text= "Signal/Sign Designation")
        lbl1.grid(row = self.rowNum, column = 0, padx = 7, pady = 10)
        Grid.columnconfigure(self.frame, 0, weight=1)

        entry1 = Entry(self.frame)
        
        entry1.grid(row = self.rowNum, column = 1, columnspan = 2, sticky=E+W+N, pady = 10)
        Grid.columnconfigure(self.frame, 1, weight=1)

        self.SignalDesignation.append(entry1)

        lbl2 = Label(self.frame, text= "Distance b/w Pole & Signal")
        lbl2.grid(row = self.rowNum, column = 3, padx = 8, pady = 10)
        Grid.columnconfigure(self.frame, 3, weight=1)

        entry2 = Entry(self.frame)
        
        entry2.grid(row = self.rowNum, column = 4, columnspan = 1, sticky = E+W+N, pady = 10)
        Grid.columnconfigure(self.frame, 4, weight=1)
        self.SignalDistance.append(entry2)

        lbl3 = Label(self.frame, text= "Area of Signal", width = 12)
        lbl3.grid(row = self.rowNum, column = 5, padx = 8, pady = 10)
        Grid.columnconfigure(self.frame, 5, weight=1)

        # entry3 = Entry(self.parent)
        # entry3.grid(row = self.rowNum, column = 6, columnspan = 1, sticky = E+W+N, pady = 10)

        # entry3 = Combobox(self.frame, values = self.SignalHeadType, state ='readonly', width = 23)
        # entry3.current(0)
        # entry3.grid(row = self.rowNum, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
        # self.SignalArea.append(entry3)

        AreaEntry = Entry(self.frame, width=23)
        AreaEntry.grid(row = self.rowNum, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
        Grid.columnconfigure(self.frame, 6, weight=1)
        self.SignalArea.append(AreaEntry)

        addButton = Button(self.frame, text="+", command=lambda: self.AddButtonClicked())
        addButton.grid(row = self.rowNum, column = 8, pady = 10, padx = 8, sticky="nw")

        # minusButton = Button(self.frame, text="-", command=self.MinusButtonClicked)
        # minusButton.grid(row = self.rowNum, column = 8, pady = 10, padx = 8, sticky="se")
        Grid.columnconfigure(self.frame, 8, weight=2)
        self.Buttons.append(addButton)
        # self.MinusButtons.append(minusButton)

        b = IntVar()
        b.set(0)
        index = self.rowNum
        checkButton = Checkbutton(self.frame, text="Is A Signal", variable=b, command=lambda: self.ClickOnSignal(index, b), onvalue=1, offvalue=0)
        checkButton.grid(row=self.rowNum, column = 9, pady = 10)
        Grid.columnconfigure(self.frame, 9, weight=1)
        Grid.columnconfigure(self.frame, 10, weight=1)
        Grid.columnconfigure(self.frame, 11, weight=1)
        Grid.columnconfigure(self.frame, 12, weight=1)
        Grid.columnconfigure(self.frame, 13, weight=1)

        self.IsSignalCheckButton.append(checkButton)
        self.IsSignal.append(0)


        # self.KVal = Label(self.frame, text="K Value "+str(self.K))
        # self.KVal.config(font=("Helvetica, 17"))
        # self.KVal.grid(row = self.rowNum + 2000, column=2, padx=15, pady=15)


    

    def AddButtonClicked(self):
        button = self.Buttons[self.rowNum-1]
        # print button
        button.grid_forget()
        # Grid.rowconfigure(self.frame, self.rowNum, weight=1)
        self.rowNum += 1
        # self.parent.grid_rowconfigure(self.rowNum, weight=1)
        
        
        lbl1 = Label(self.frame, text= "Signal/Sign Designation")
        lbl1.grid(row = self.rowNum, column = 0, padx = 7, pady = 10)
        
        entry1 = Entry(self.frame)
        
        entry1.grid(row = self.rowNum, column = 1, columnspan = 2, sticky = E+W+N, pady = 10)

        self.SignalDesignation.append(entry1)

        lbl2 = Label(self.frame, text= "Distance from Pole to Signal", width = 25)
        lbl2.grid(row = self.rowNum, column = 3, padx = 8, pady = 10)

        entry2 = Entry(self.frame)
        
        entry2.grid(row = self.rowNum, column = 4, columnspan = 1, sticky = E+W+N, pady = 10)
        self.SignalDistance.append(entry2)

        lbl3 = Label(self.frame, text="Area of Signal", width=12)
        lbl3.grid(row = self.rowNum, column=5, padx=8, pady=10)

        # entry3 = Entry(self.parent)
        # entry3 = Combobox(self.frame, values = self.SignalHeadType, state ='readonly', width = 23)
        # entry3.current(0)
        # entry3.grid(row = self.rowNum, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)


        # self.SignalArea.append(entry3)

        AreaEntry = Entry(self.frame, width=23)
        AreaEntry.grid(row = self.rowNum, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
        self.SignalArea.append(AreaEntry)

        addButton = Button(self.frame, text="+", command=lambda: self.AddButtonClicked())
        addButton.grid(row = self.rowNum, column = 8, pady = 10, padx = 10, sticky="nw")

        # minusButton = Button(self.frame, text="-", command=self.MinusButtonClicked)
        # minusButton.grid(row = self.rowNum, column = 8, pady = 10, padx = 10, sticky="se")

        # self.MinusButtons.append(minusButton)
        self.Buttons.append(addButton)


        b = IntVar()
        b.set(0)
        index = self.rowNum
        checkButton = Checkbutton(self.frame, text="Is A Signal", variable=b, command=lambda:self.ClickOnSignal(index, b))
        checkButton.grid(row=self.rowNum, column = 9, pady = 10)
        self.IsSignalCheckButton.append(checkButton)
        self.IsSignal.append(0)

       
        # print self.rowNum

    # def MinusButtonClicked(self, event):
    #     pass


   
def main():
    root = Tk()
    # root.geometry("1050x500+200+100")
    # root.resizable(0,0)
    # root.columnconfigure(0, weight=1s)
    # root.rowconfigure(1, weight=1)
    # root.rowconfigure(1, weight=1)
    # root.rowconfigure(2, weight=1)
    root.tk_strictMotif()
    root.iconbitmap('favicon.ico')
    app = OneArm(root)
    root.mainloop()  

# if __name__ == '__main__':
#     main()  