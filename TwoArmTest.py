from Tkinter import Tk, Text, TOP, BOTH, X, N, S, E, W, LEFT, RIGHT, Button, Canvas, IntVar, Toplevel, BOTTOM, Grid, CENTER, Menu, SE, StringVar
from ttk import Frame, Label, Entry, Combobox, Scrollbar, Checkbutton, LabelFrame, Treeview
import csv, math, os
import xlsxwriter
import tkFileDialog as filedialog
import tkMessageBox as MessageBox
import sqlite3
from functools import partial



class TwoArm(Frame):
    Areas = []
    Table1 = []
    Table2 = []
    Headers = []

    rowNumTop = 0
    SignalDesignationTop = []
    SignalDistanceTop = []
    SignalAreaTop = []
    ButtonsTop = []
    IsSignalCheckButtonTop = []
    IsSignalTop = []
    SignAreaTop = []
    KTop = 0
    AreaOfSignalTop = 0
    MaxDistanceTop = 0

    rowNumBottom = 0
    SignalDesignationBottom = []
    SignalDistanceBottom = []
    SignalAreaBottom = []
    ButtonsBottom = []
    IsSignalCheckButtonBottom = []
    IsSignalBottom = []
    SignAreaBottom = []
    KBottom = 0
    AreaOfSignalBottom = 0
    MaxDistanceBottom = 0
    TwoWayPoleTable = []

    Design = ""
    name = ""
    NameLabel = None
    DesignTop = []
    DesignBottom = []

    WorkingDirectory = os.path.dirname(os.path.realpath(__file__))
    DataDirectory = WorkingDirectory + "/Data/"
    
    with open(DataDirectory+'Areas For Signal Heads.csv', 'rb') as csvfile:
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

    with open(DataDirectory+'Two Way Pole Table.csv') as CsvFile:
        SpamReader = csv.reader(CsvFile)
        for Row in SpamReader:
            TwoWayPoleTable.append(Row)
        
    # print TwoWayPoleTable

    SignalHeadType = []
    # SignalHeadType = (
    #     "1 Section -- 8",
    #     "3 Sections -- 8",
    #     "4 Sections -- 8",
    #     "5 Sections - Vertical -- 8",
    #     "5 Sections - Cluster -- 8",
    #     "5 Sections - Mixed -- 8",
    #     "1 Section -- 12",
    #     "3 Sections -- 12",
    #     "4 Sections -- 12",
    #     "5 Sections - Vertical -- 12",
    #     "5 Sections - Cluster -- 12",
    #     "5 Sections - Mixed -- 12"
    # )

    for i in range(len(Areas)):
        for j in range(1, len(Headers[0])):
            # print "YO"
            SignalHeadType.append(Areas[i][0]+" -- "+str(Headers[0][j]))


    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # self.Areas = []
        # self.Table1 = []
        # self.Table2 = []
        # self.Headers = []

        self.rowNumTop = 0
        self.SignalDesignationTop = []
        self.SignalDistanceTop = []
        self.SignalAreaTop = []
        self.ButtonsTop = []
        self.IsSignalCheckButtonTop = []
        self.IsSignalTop = []
        self.SignAreaTop = []
        self.KTop = 0
        self.AreaOfSignalTop = 0
        self.MaxDistanceTop = 0

        self.rowNumBottom = 0
        self.SignalDesignationBottom = []
        self.SignalDistanceBottom = []
        self.SignalAreaBottom = []
        self.ButtonsBottom = []
        self.IsSignalCheckButtonBottom = []
        self.IsSignalBottom = []
        self.SignAreaBottom = []
        self.KBottom = 0
        self.AreaOfSignalBottom = 0
        self.MaxDistanceBottom = 0
        # self.TwoWayPoleTable = []

        self.Design = ""
        self.name = ""
        self.DesignTop = []
        self.DesignBottom = []


        self.initUI()
        # self.NameLabel = Label(self.frame)
        

    def onMouseWheelTop(self, event):
        self.TopCanvas.yview_scroll(-1*(event.delta/120), "units")

    def onMouseWheelBottom(self, event):
        self.BottomCanvas.yview_scroll(-1*(event.delta/120), "units")

    def Calculation(self, flag):
        self.MaxDistanceTop = 0
        self.MaxDistanceBottom = 0
        count = 0
        
        DistanceFromPoleToSignalTop = 0
        self.KTop = 0
        try:
            for i in range(len(self.SignalDesignationTop)):
                DistanceFromPoleToSignalTop = self.SignalDistanceTop[i].get()
                if self.SignalDistanceTop[i].get() == "":
                    DistanceFromPoleToSignalTop = '0'
                if self.MaxDistanceTop < float(DistanceFromPoleToSignalTop):
                    self.MaxDistanceTop = float(DistanceFromPoleToSignalTop)
                
                value = self.SignalAreaTop[i].get()

                if self.IsSignalTop[i] == 1:
                    ValueArray = value.split("--")
                    index = [(ind, self.Areas[ind].index(ValueArray[0].strip())) for ind in xrange(len(self.Areas)) if ValueArray[0].strip() in self.Areas[ind]]
                    if ValueArray[1].strip() == '8':
                        value = float(self.Areas[index[0][0]][1])
                    else:
                        value = float(self.Areas[index[0][0]][2])
                else:
                    if self.SignalAreaTop[i].get() == "":
                        value = '0'
                
                self.AreaOfSignalTop += float(value)
                AreaMomentDesign = float(DistanceFromPoleToSignalTop)*float(value)
                self.KTop += AreaMomentDesign
        
        except ValueError, e:
            MessageBox.showerror("Error", message=str(e))
            return
        

        DistanceFromPoleToSignalBottom = 0
        self.KBottom = 0
        try:
            for i in range(len(self.SignalDesignationBottom)):
                DistanceFromPoleToSignalBottom = self.SignalDistanceBottom[i].get()
                if self.SignalDistanceBottom[i].get() == "":
                    DistanceFromPoleToSignalBottom = '0'
                if self.MaxDistanceBottom < float(DistanceFromPoleToSignalBottom):
                    self.MaxDistanceBottom = float(DistanceFromPoleToSignalBottom)

                value = self.SignalAreaBottom[i].get()
                
                if self.IsSignalBottom[i] == 1:
                    ValueArray = value.split("--")
                    index = [(ind, self.Areas[ind].index(ValueArray[0].strip())) for ind in xrange(len(self.Areas)) if ValueArray[0].strip() in self.Areas[ind]]
                    if ValueArray[1].strip() == '8':
                        value = float(self.Areas[index[0][0]][1])
                    else:
                        value = float(self.Areas[index[0][0]][2])
                else:
                    if self.SignalAreaBottom[i].get() == "":
                        value = '0'
                
                self.AreaOfSignalBottom += float(value)
                
                AreaMomentDesign = float(DistanceFromPoleToSignalBottom)*float(value)
                self.KBottom += AreaMomentDesign

        except ValueError, e:
            MessageBox.showerror("Error", message=str(e))
            return 

        # print self.KTop
        # print self.KBottom

        if flag:
            self.Output()

    
    def setName(self):
        # pass
        # self.NameLabel.destroy()
        LabelText = StringVar()
        LabelText.set(str(self.name))
        # # print LabelText.get()
        self.parent.title(LabelText.get())
        # self.NameLabel = Label(self.frame, text=LabelText.get())
        # self.NameLabel.config(font=("Helvetica, 12"))
        # self.NameLabel.grid(row=3000, column=2, columnspan=3, padx=20, pady=15)

    def setKVal(self):
        pass
        # self.KVal.destroy()
        # self.KVal = None
        # LabelText = StringVar()
        # LabelText.set("K Value: "+str(self.KTop))
        # self.KVal = Label(self.frame, text=LabelText.get())
        # self.KVal.config(font=("Helvetica, 15"))
        # self.KVal.grid(row=3000, column=0, columnspan=3, padx=20, pady=15)

    def setMaxDistance(self):
        self.MaxDistanceTop = self.SignalDistanceTop[len(self.SignalDistanceTop)-1]
        self.MaxDistanceBottom = self.SignalDistanceBottom[len(self.SignalDistanceBottom)-1]



    def setDesign(self):
        # self.DesignLabel.destroy()
        # LabelText = StringVar()
        # LabelText.set("Use Design: "+str(self.Design))
        # self.DesignLabel = Label(self.frame, text=LabelText.get())
        # self.DesignLabel.config(font=("Helvetica, 15"))
        # self.DesignLabel.grid(row=3000, column=7, columnspan=2, padx=20, pady=15)
        self.DesignTop = self.DesignChoice(self.KTop, self.MaxDistanceTop)
        self.DesignBottom = self.DesignChoice(self.KBottom, self.MaxDistanceBottom)
        self.Design = self.FinalDesignChoice()


    def Output(self):
        dlg = Toplevel(master=self.parent)
        
        dlg.iconbitmap('favicon.ico')
        frame = Frame(dlg)
        frame.pack(fill='both', expand=True)
        frame2 = Frame(dlg, borderwidth=1, relief="ridge")
        frame2.pack(fill='both', side=BOTTOM)
        
        MsgTop = "K of Arm A : "+str(int(math.ceil(self.KTop)))
        MsgBottom = "K of Arm B : "+str(int(math.ceil(self.KBottom)))
        
        DesignMessageTop = "Use Design(Arm A) : "
        self.DesignTop = self.DesignChoice(self.KTop, self.MaxDistanceTop)
        # if DesignTop is None:
        #     DesignTop[0] = 0
        FinalDesignMessageTop = DesignMessageTop + str(self.DesignTop[0])
        
        DesignMessageBottom = "Use Design(Arm B) : "
        self.DesignBottom = self.DesignChoice(self.KBottom, self.MaxDistanceBottom)
        FinalDesignMessageBottom = DesignMessageBottom + str(self.DesignBottom[0])

        label = Label(frame, text=MsgTop)
        label.grid(row=1, column=3, columnspan=15, pady=15, padx=15)
        label.config(font=("Courier, 20"))

        label2 = Label(frame, text=MsgBottom)
        label2.grid(row=2, column=3, columnspan=15, pady=15, padx=15)
        label2.config(font=("Courier, 20"))

        label3 = Label(frame, text=FinalDesignMessageTop)
        label3.grid(row=3, column=3, columnspan=15, pady=15, padx=15)
        label3.config(font=("Courier, 20"))

        label4 = Label(frame, text=FinalDesignMessageBottom)
        label4.grid(row=4, column=3, columnspan=15, pady=15, padx=15)
        label4.config(font=("Courier, 20"))
        
        CalculatedResult = self.FinalDesignChoice()

        # for i in range(len(self.TwoWayPoleTable)):
        #     if self.TwoWayPoleTable[i][0] == '':
        #         self.TwoWayPoleTable[i][0] = 0
        #     if int(self.TwoWayPoleTable[i][0]) == int(DesignTop[0]):
        #         for j in range(len(self.TwoWayPoleTable[i])):
        #             if self.TwoWayPoleTable[0][j] == '':
        #                 self.TwoWayPoleTable[0][j] = 0
        #             if int(self.TwoWayPoleTable[0][j]) == int(DesignBottom[0]):
        #                 CalculatedResult = self.TwoWayPoleTable[i][j]
        #                 break

        # if CalculatedResult == '':
        #     CalculatedResult = "N/A"


        self.Design = str(CalculatedResult)
        FinalMessage = "Use Design : " + str(CalculatedResult)
        label5 = Label(frame, text=FinalMessage)
        label5.grid(row=5, column=3, columnspan=15, pady=15, padx=15)
        label5.config(font=("Courier, 20"))
    
        btn = Button(frame2, text="End Program", command=self.parent.quit)
        btn.pack(side=RIGHT, padx=15, pady=6)
        Button(frame2, text="Save to Database", command=self.SaveToDatabase).pack(side=RIGHT, padx=15, pady=6)
        Button(frame2, text="Write to Excel File", command=lambda: self.WriteToExcelFile(dlg)).pack(side=RIGHT, padx=15, pady=6)
        dlg.transient(self.parent)
        self.Center(dlg)
        dlg.grab_set()

    
    def FinalDesignChoice(self):
        CalculatedResult = None
        for i in range(len(self.TwoWayPoleTable)):
            if self.TwoWayPoleTable[i][0] == '':
                self.TwoWayPoleTable[i][0] = 0
            if int(self.TwoWayPoleTable[i][0]) == int(self.DesignTop[0]):
                for j in range(len(self.TwoWayPoleTable[i])):
                    if self.TwoWayPoleTable[0][j] == '':
                        self.TwoWayPoleTable[0][j] = 0
                    if int(self.TwoWayPoleTable[0][j]) == int(self.DesignBottom[0]):
                        CalculatedResult = self.TwoWayPoleTable[i][j]
                        break

        if CalculatedResult == '':
            CalculatedResult = "N/A"

        return CalculatedResult
    

    def Center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        # print size
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size[0], size[1], x, y))


    def DesignChoice(self, KValue, MaxDistance):
        ReturnValue = None
        for i in self.Table1:
            if MaxDistance+2 < float(i[2]):
                # MaxChoice.append(i)                      
                if KValue < float(i[1]):
                    ReturnValue = i
                    # return i
                    break
                else:
                    continue
        
        if ReturnValue is None:
            # print "Woah"
            ReturnValue = []
            ReturnValue.append("N/A")
        
        return ReturnValue

    def WriteToExcelFile(self, window):
        # xlFilePath = filedialog.asksaveasfilename(initialdir="/", title="Select File", filetypes=(("Excel Files", "*.xlsx"),))
        # # print xlFilePath
        # workbook = xlsxwriter.workbook(xlFilePath+self.name+".xlsx")

        window.destroy()

        try:
            xlFilePath = filedialog.asksaveasfilename(initialdir=self.DataDirectory, title="Select File", filetypes=(("Excel Files", "*.xlsx"),))
            if xlFilePath is '':
                return
            elif '.' in xlFilePath:
                workbook = xlsxwriter.Workbook(xlFilePath)
            
            else:
                workbook = xlsxwriter.Workbook(xlFilePath+".xlsx")

            worksheet = workbook.add_worksheet()

            MergeFormat = workbook.add_format({
                'bold' : 1,
                'border' : 1,
                'align' : 'center'
            })

            MergeUnderline =  workbook.add_format({
                'align' : 'center',
                'underline' : 1,
                'bold' : 1

            })

            BorderFormat = workbook.add_format({
                'border' : 1
            })

            WrapText = workbook.add_format()
            WrapText.set_text_wrap()
            WrapText.set_border()

            worksheet.merge_range("A1:D1", self.name, MergeFormat)

            Heading = []
            Heading.append("Signal Or Sign Designation")
            Heading.append("Distance from Pole to Signal Or Sign")
            Heading.append("Area of Signal Or Sign")
            Heading.append("Area Moment Design Factor")


            worksheet.merge_range(3, 0, 3, 3, "Arm A", MergeUnderline)
            
            import time
            import datetime

            TimeStamp = time.time()
            DateTime = datetime.datetime.fromtimestamp(TimeStamp).strftime('%m/%d/%Y %H:%M:%S')

            worksheet.set_column(5, 5, 25)
            worksheet.set_column(0, 0, 15)
            worksheet.set_column(1, 1, 23)
            worksheet.set_column(2, 2, 20)
            worksheet.set_column(3, 3, 20)
            # worksheet.set_column(7, 7, 27)

            
            
            worksheet.write_string(5, 0, Heading[0], WrapText)
            worksheet.write_string(5, 1, Heading[1], WrapText)
            worksheet.write_string(5, 2, Heading[2], WrapText)
            worksheet.write_string(5, 3, Heading[3], WrapText)

            CurrentRow = 6

            Items = []
            for item in range(len(self.SignalDesignationTop)):
                ItemRow = []
                ItemRow.append(self.SignalDesignationTop[item].get())
                ItemRow.append(self.SignalDistanceTop[item].get())
                ItemRow.append(self.SignalAreaTop[item].get())
                AreaMoment = float(self.SignalDistanceTop[item].get()) * float(self.SignalAreaTop[item].get())
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
            worksheet.write_number(CurrentRow, 1, float(self.KTop), BorderFormat)

            # from xlsxwriter.utility import xl_rowcol_to_cell
            # cell = xl_rowcol_to_cell(CurrentRow, 1)

            # worksheet.write(cell, '=SUM(D7:D13)', BorderFormat)


            CurrentRow += 3

            worksheet.merge_range(CurrentRow, 0, CurrentRow, 3, "Arm B", MergeUnderline)
            CurrentRow += 2

            worksheet.write_string(CurrentRow, 0, Heading[0], WrapText)
            worksheet.write_string(CurrentRow, 1, Heading[1], WrapText)
            worksheet.write_string(CurrentRow, 2, Heading[2], WrapText)
            worksheet.write_string(CurrentRow, 3, Heading[2], WrapText)

            CurrentRow += 1

            Items = []
            for item in range(len(self.SignalDesignationBottom)):
                ItemRow = []
                ItemRow.append(self.SignalDesignationBottom[item].get())
                ItemRow.append(self.SignalDistanceBottom[item].get())
                ItemRow.append(self.SignalAreaBottom[item].get())
                AreaMoment = float(self.SignalDistanceBottom[item].get()) * float(self.SignalAreaBottom[item].get())
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
            worksheet.write_number(CurrentRow, 1, float(self.KBottom), BorderFormat)

            CurrentRow += 3

            worksheet.write_string(CurrentRow, 0, "Use Design", MergeFormat)
            worksheet.write_string(CurrentRow, 1, self.Design, MergeFormat)

            # from xlsxwriter.utility import xl_rowcol_to_cell
            # cell = xl_rowcol_to_cell(CurrentRow, 1)

            # worksheet.write(cell, '=SUM(D7:D13)', BorderFormat)

            CurrentRow += 4

            worksheet.write_string(CurrentRow, 3, "Generated By Software", WrapText)
            worksheet.write_string(CurrentRow+1, 3, "Generated On : "+DateTime, WrapText)

            workbook.close()
            MessageBox.showinfo("Success", "The data has been successfully written to the File.")
            # CurrentRow += 1

        except IOError, e:
            MessageBox.showerror("Error", message=str(e))

        except Exception, e:
            MessageBox.showerror("Error", message=str(e))


    def ClickOnSignal(self, index, b, canvas):
        if canvas == "Top":
            value = b.get()
            if value == 0:
                AreaEntry = Entry(self.TopCanvasFrame)
                AreaEntry.grid(row = index, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
                self.IsSignalTop[index-1] = 0
                self.SignalAreaTop[index-1] = AreaEntry
            else:
                entry3 = Combobox(self.TopCanvasFrame, values = self.SignalHeadType, state ='readonly', width = 23)
                entry3.current(0)
                entry3.grid(row = index, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
                self.IsSignalTop[index-1] = 1
                self.SignalAreaTop[index-1] = entry3

        else:
            value = b.get()
            if value == 0:
                AreaEntry = Entry(self.BottomCanvasFrame)
                AreaEntry.grid(row = index, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
                self.IsSignalBottom[index-1] = 0
                self.SignalAreaBottom[index-1] = AreaEntry
            else:
                entry3 = Combobox(self.BottomCanvasFrame, values = self.SignalHeadType, state ='readonly', width = 23)
                entry3.current(0)
                entry3.grid(row = index, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
                self.IsSignalBottom[index-1] = 1
                self.SignalAreaBottom[index-1] = entry3


    def onResizeTop(self, event):
        canvas_width = event.width
        canvas_height = event.height
        self.TopCanvas.itemconfig(self.TopFrameWindow, width=canvas_width)

    def onResizeBottom(self, event):
        canvas_width = event.width
        canvas_height = event.height
        self.BottomCanvas.itemconfig(self.BottomFrameWindow, width=canvas_width)

    def onTopFrameConfigure(self, event):
        self.TopCanvas.configure(scrollregion=self.TopCanvas.bbox("all"))
        
   
    def onBottomFrameConfigure(self, event):
        self.BottomCanvas.configure(scrollregion=self.BottomCanvas.bbox("all"))


    def OnClosing(self, window):
        """ Some yes no inputs regarding exit or Previous step """
        # dialog = MessageBox.askyesno("How To Proceed", "Do you want to go back?", parent=self.parent)
        # if dialog:
        #     window.destroy()
        #     self.parent.deiconify()
        #     return
        # else:
        Sure = MessageBox.askokcancel("Quit", "The Application will be closed", icon='warning', parent=self.parent)
        if Sure:
            window.destroy()
            self.parent.quit()

    def ShowWindow(self, toShow):
        self.parent.withdraw()
        if toShow == "OneArm":
            Window = Toplevel()
            Window.protocol("WM_DELETE_WINDOW",lambda : self.OnClosing(Window))
            Window.title("GUI Application")
            Window.iconbitmap('favicon.ico')
            Window.geometry("1050x500+200+100")

            from OneArmTest import OneArm

            app = OneArm(Window)


        elif toShow == "TwoArm":
            Window = Toplevel()
            Window.protocol("WM_DELETE_WINDOW",lambda : self.OnClosing(Window))
            Window.title("GUI Application")
            Window.iconbitmap('favicon.ico')
            Window.geometry("1050x600+200+100")
            app = TwoArm(Window)
        else:
            Window = Toplevel()
            Window.geometry("400x100+500+300")
            Window.protocol("WM_DELETE_WINDOW",lambda : self.OnClosing(Window))
            Window.resizable(0,0)
            Window.tk_strictMotif()
            Window.iconbitmap('favicon.ico')

            from FinalSoftware import FinalSoftware

            FinalSoftware(Window)
        


    def Menu(self):
        self.menubar = Menu(self)
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="List", menu=menu)
        menu.add_command(label="Open A Configuration", command=self.Index)

        # menu = Menu(self.menubar, tearoff=0)
        # self.menubar.add_cascade(label="Edit", menu=menu)
        # menu.add_command(label="Cut")
        # menu.add_command(label="Copy")
        # menu.add_command(label="Paste")

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Window", menu=menu)
        menu.add_command(label="Select Mode", command= lambda: self.ShowWindow("Select"))
        menu.add_command(label="One Arm Calculation", command= lambda: self.ShowWindow("OneArm"))
        menu.add_command(label="Two Arm Calculation", command= lambda: self.ShowWindow("TwoArm"))

        try:
            self.parent.config(menu=self.menubar)
        except:
            print "Uvee"
        
    def Index(self):
        self.parent.withdraw()
        window = Toplevel()
        window.iconbitmap('favicon.ico')
        window.protocol("WM_DELETE_WINDOW",lambda : self.onClosingIndex(window))
        self.TreeView(window)

    def onClosingIndex(self, window):
        #  dialog = MessageBox.askyesno("How To Proceed", "Do you want to go back?", parent=self.parent)
        # if dialog:
        window.destroy()
        self.parent.deiconify()
            # return
        # else:
        # Sure = MessageBox.askokcancel("Quit", "The Application will be closed", icon='warning')
        # if Sure:
            # self.parent.quit()


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

        
        from FinalSoftware import FinalSoftware
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
    
    def onDoubleClick(self, event):
        
        item = self.tree.selection()[0]
        # print ("You Clicked On ", str(self.tree.item(item, "text")))
        Value = []
        Value.append(str(self.tree.item(item, "text")))

        Items = []
        Items.append(self.tree.item(item, "values"))
        # print Items
        # print Items[0][3]

        flag = Items[0][3]

        if flag == "No":

            from FinalSoftware import FinalSoftware
            Connection = FinalSoftware.CreateConnection()
            Cursor = Connection.cursor()

            Cursor.execute("SELECT * FROM OneArmValue WHERE OneArmIdFK = ?", Value)
            ResultSet = Cursor.fetchall()

            window = Toplevel()
            # self.parent.destroy()
            # window.protocol("WM_DELETE_WINDOW",lambda : self.OnClosing(window))
            window.title("GUI Application")
            window.iconbitmap('favicon.ico')
            window.geometry("1050x500+200+100")

            from OneArmTest import OneArm

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
            from FinalSoftware import FinalSoftware
            Connection = FinalSoftware.CreateConnection()
            Cursor = Connection.cursor()

            Cursor.execute("SELECT * FROM TwoArmValue WHERE TwoArmIdFK = ? AND Arm = 'A';", Value)
            ResultSet = Cursor.fetchall()

            window = Toplevel()
            # self.destroy()
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
            app.setKVal()
            app.setDesign()
            app.setMaxDistance()


    def SaveToDatabase(self):
        dlg = Toplevel(master=self.parent)
        dlg.geometry("350x150")
        self.Center(dlg)
        dlg.iconbitmap('favicon.ico')
        frame = Frame(dlg)
        frame.pack(fill='both', expand=True)

        label = Label(frame, text="Save To Database As...")
        label.place(relx=0.5, rely=0.3, anchor=CENTER)
        entry = Entry(frame, width=50)
        entry.place(relx=0.5, rely=0.5, anchor=CENTER)

        button = Button(frame, text="Save", command=partial(self.SaveToDatabaseContinued, entry, dlg))
        button.place(relx=0.95, rely=0.9, anchor=SE)
        dlg.transient()
        dlg.grab_set()

    def SaveToDatabaseContinued(self, entry, dlg):
        SaveAs = entry.get()
        self.name = SaveAs
        dlg.destroy()

        from FinalSoftware import FinalSoftware
        Conn = FinalSoftware.CreateConnection()
        # print Conn
        cursor = Conn.cursor()


        Id = []
        Id.append(str(SaveAs))
        # task = (str(SaveAs), )
        sql = "SELECT TwoArmId FROM TwoArm Where Name = ?;"
        cursor.execute(sql, (str(SaveAs), ))

        ResultSet = []
        ResultSet = cursor.fetchall()
        # print lines.rowcount
        if ResultSet:
            # print ResultSet[0][0]
            # print "Yo"
            for data in range(len(ResultSet)):
                sql = "DELETE FROM TwoArmValue Where TwoArmIdFK = ?;"
                cursor.execute(sql, ResultSet[data])

                sql = "DELETE FROM TwoArm WHERE TwoArmId = ?;"
                cursor.execute(sql, ResultSet[data])
        
        


        
        task = (str(SaveAs), 0)
        sql = "Insert into TwoArm(Name, KValueUp) Values (?,?);"
        InsertId = None
        try:
            cursor.execute(sql, task)
            Conn.commit()
            InsertId = cursor.lastrowid
            # print InsertId
        except Exception, e:
            print e
            Conn.rollback()

        sql = "Insert into TwoArmValue(SignalDesignation, SignalDistance, SignalArea, TwoArmIdFK, Arm) Values (?,?,?,?,?);"
        
        for i in range(len(self.SignalDesignationTop)):
            SignalDesign = self.SignalDesignationTop[i].get()
            SignalDistance = self.SignalDistanceTop[i].get()
            
            #TODO Calculate Area based on signal selected Done
            value = self.SignalAreaTop[i].get()
            if self.IsSignalTop[i] == 1:
                ValueArray = value.split("--")
                index = [(ind, self.Areas[ind].index(ValueArray[0].strip())) for ind in xrange(len(self.Areas)) if ValueArray[0].strip() in self.Areas[ind]]
                if ValueArray[1].strip() == '8':
                    # print self.Areas[index[0][0]][1]
                    value = float(self.Areas[index[0][0]][1])
                else:
                    value = float(self.Areas[index[0][0]][2])
            else:
                if self.SignalAreaTop[i].get() == "":
                    value = '0'
            
            SignalArea = value

            task = (SignalDesign, SignalDistance, SignalArea, InsertId, "A")

            try:
                cursor.execute(sql, task)
                Conn.commit()
            except:
                Conn.rollback() 


        for i in range(len(self.SignalDesignationBottom)):
            SignalDesign = self.SignalDesignationBottom[i].get()
            SignalDistance = self.SignalDistanceBottom[i].get()
            
            #TODO Calculate Area based on signal selected Done
            value = self.SignalAreaBottom[i].get()
            if self.IsSignalBottom[i] == 1:
                ValueArray = value.split("--")
                index = [(ind, self.Areas[ind].index(ValueArray[0].strip())) for ind in xrange(len(self.Areas)) if ValueArray[0].strip() in self.Areas[ind]]
                if ValueArray[1].strip() == '8':
                    # print self.Areas[index[0][0]][1]
                    value = float(self.Areas[index[0][0]][1])
                else:
                    value = float(self.Areas[index[0][0]][2])
            else:
                if self.SignalAreaBottom[i].get() == "":
                    value = '0'
            
            SignalArea = value

            task = (SignalDesign, SignalDistance, SignalArea, InsertId, "B")

            try:
                cursor.execute(sql, task)
                Conn.commit()
            except:
                Conn.rollback() 

        
        try:
            task = (self.KTop, self.KBottom, self.Design, InsertId)
            cursor.execute("UPDATE TwoArm SET KValueUp = ?, KValueDown = ?, Design = ? WHERE TwoArmId = ?", task)
            Conn.commit()
            MessageBox.showinfo("Success", "The data has been successfully entered into the database.")
        except:
            Conn.rollback()
                
        Conn.close()

    def WritingScript(self, data, Arm):
        rowNumber = 0
        count = 0

        if Arm == "Top":
            for row in data:
                if count!=0:
                    self.AddButtonClicked("Top")
                self.SignalDesignationTop[rowNumber].insert(0, row[1])
                self.SignalDistanceTop[rowNumber].insert(0, row[2])
                self.SignalAreaTop[rowNumber].insert(0, row[3])
                rowNumber += 1
                # SignalDesignation[rowNumber].insert(0, row[1])
                count += 1
        
        elif Arm == "Bottom":
            for row in data:
                if count!=0:
                    self.AddButtonClicked("Bottom")
                self.SignalDesignationBottom[rowNumber].insert(0, row[1])
                self.SignalDistanceBottom[rowNumber].insert(0, row[2])
                self.SignalAreaBottom[rowNumber].insert(0, row[3])
                rowNumber += 1
                # SignalDesignation[rowNumber].insert(0, row[1])
                count += 1
        
        self.Calculation(False)


    def initUI(self):
        self.parent.title("GUI Application")
        self.Menu()
        self.TopFrame = Frame(self.parent, relief="raised", borderwidth=1)
        self.BottomFrame = Frame(self.parent, relief="ridge", borderwidth=1)

        self.TopFrame.pack(side=TOP, expand=True, fill="both")
        self.BottomFrame.pack(side=BOTTOM, expand=True, fill="both")

        self.TopCanvas = Canvas(self.TopFrame, borderwidth=1)
        self.BottomCanvas = Canvas(self.BottomFrame, borderwidth=1)

        self.TopCanvasFrame = Frame(self.TopCanvas, width=1050, height=300)
        self.BottomCanvasFrame = Frame(self.BottomCanvas, width=1050, height=300)

        self.VsbTop = Scrollbar(self.TopFrame, orient='vertical', command=self.TopCanvas.yview)
        self.TopCanvas.configure(yscrollcommand=self.VsbTop.set)
        self.VsbTop.pack(side="right", fill="both")
        
        self.TopCanvas.pack(side="left", fill="both", expand=True)
        self.TopFrameWindow = self.TopCanvas.create_window((2,2), window=self.TopCanvasFrame, anchor="nw", tags="self.TopCanvasFrame")
        self.TopCanvasFrame.bind("<Configure>", self.onTopFrameConfigure)
        self.TopCanvas.bind("<Configure>", self.onResizeTop)


        self.VsbBottom = Scrollbar(self.BottomFrame, orient='vertical', command=self.BottomCanvas.yview)
        self.BottomCanvas.configure(yscrollcommand=self.VsbBottom.set)
        self.VsbBottom.pack(side="right", fill="both")
        
        self.BottomCanvas.pack(side="left", fill="both", expand=True)
        self.BottomFrameWindow = self.BottomCanvas.create_window((2,2), window=self.BottomCanvasFrame, anchor="nw", tags="self.BottomCanvasFrame")
        self.BottomCanvasFrame.bind("<Configure>", self.onBottomFrameConfigure)
        self.BottomCanvas.bind("<Configure>", self.onResizeBottom)

        self.initUITop()
        self.initUIBottom()

    def initUITop(self):
        # self.TopCanvas.bind_all("<MouseWheel>", self.onMouseWheelTop)
        # self.TopCanvasFrame.bind("<Button-1>", lambda _: self.TopCanvasFrame.foucs_set())
        # self.TopCanvas.bind("<MouseWheel>", self.onMouseWheelTop)
        headingLabel = Label(self.TopCanvasFrame, text="Arm A")
        headingLabel.config(font=("Courier, 25"))
        headingLabel.grid(row=self.rowNumTop, column=1, columnspan=6, pady=20)
        self.rowNumTop += 1

        CalculateButton = Button(self.TopCanvasFrame, text = "Calculate K", command=lambda: self.Calculation(True))
        CalculateButton.grid(row=0, column=8, pady=10, columnspan=3)

        lbl1 = Label(self.TopCanvasFrame, text= "Signal/Sign Designation")
        lbl1.grid(row = self.rowNumTop, column = 0, padx = 7, pady = 10)
        Grid.columnconfigure(self.TopCanvasFrame, 0, weight=1)


        entry1 = Entry(self.TopCanvasFrame)
        entry1.grid(row = self.rowNumTop, column = 1, columnspan = 2, sticky = E+W+N, pady = 10)
        Grid.columnconfigure(self.TopCanvasFrame, 1, weight=1)
        self.SignalDesignationTop.append(entry1)

        lbl2 = Label(self.TopCanvasFrame, text= "Distance b/w Pole & Signal")
        lbl2.grid(row = self.rowNumTop, column = 3, padx = 8, pady = 10)
        Grid.columnconfigure(self.TopCanvasFrame, 3, weight=1)

        entry2 = Entry(self.TopCanvasFrame)
        entry2.grid(row = self.rowNumTop, column = 4, columnspan = 1, sticky = E+W+N, pady = 10)
        Grid.columnconfigure(self.TopCanvasFrame, 4, weight=1)
        self.SignalDistanceTop.append(entry2)

        lbl3 = Label(self.TopCanvasFrame, text= "Area of Signal", width = 12)
        lbl3.grid(row = self.rowNumTop, column = 5, padx = 8, pady = 10)
        Grid.columnconfigure(self.TopCanvasFrame, 5, weight=1)

        AreaEntry = Entry(self.TopCanvasFrame, width=23)
        AreaEntry.grid(row = self.rowNumTop, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
        Grid.columnconfigure(self.TopCanvasFrame, 6, weight=1)
        self.SignalAreaTop.append(AreaEntry)

        addButton = Button(self.TopCanvasFrame, text="   +   ", command=lambda: self.AddButtonClicked("Top"))
        addButton.grid(row = self.rowNumTop, column = 8, pady = 10, padx = 10)
        Grid.columnconfigure(self.TopCanvasFrame, 8, weight=1)
        self.ButtonsTop.append(addButton)

        b = IntVar()
        b.set(0)
        index = self.rowNumTop
        checkButton = Checkbutton(self.TopCanvasFrame, text="Is A Signal", variable=b, command=lambda: self.ClickOnSignal(index, b, "Top"), onvalue=1, offvalue=0)
        checkButton.grid(row=self.rowNumTop, column = 9, pady = 10)
        Grid.columnconfigure(self.TopCanvasFrame, 9, weight=1)
        self.IsSignalCheckButtonTop.append(checkButton)
        self.IsSignalTop.append(0)

        pass
    
    def initUIBottom(self):
        # self.BottomCanvasFrame.bind("<Button-1>", lambda _: self.BottomCanvasFrame.focus_set())
        # self.BottomCanvas.bind("<MouseWheel>", self.onMouseWheelBottom)
        headingLabel = Label(self.BottomCanvasFrame, text="Arm B")
        headingLabel.config(font=("Courier, 25"))
        headingLabel.grid(row=self.rowNumBottom, column=1, columnspan=6, pady=20)
        self.rowNumBottom += 1

        lbl1 = Label(self.BottomCanvasFrame, text= "Signal/Sign Designation")
        lbl1.grid(row = self.rowNumBottom, column = 0, padx = 7, pady = 10)
        Grid.columnconfigure(self.BottomCanvasFrame, 0, weight=1)

        entry1 = Entry(self.BottomCanvasFrame)
        entry1.grid(row = self.rowNumBottom, column = 1, columnspan = 2, sticky = E+W+N, pady = 10)
        Grid.columnconfigure(self.BottomCanvasFrame, 1, weight=1)
        self.SignalDesignationBottom.append(entry1)

        lbl2 = Label(self.BottomCanvasFrame, text= "Distance b/w Pole & Signal")
        lbl2.grid(row = self.rowNumBottom, column = 3, padx = 8, pady = 10)
        Grid.columnconfigure(self.BottomCanvasFrame, 3, weight=1)

        entry2 = Entry(self.BottomCanvasFrame)
        entry2.grid(row = self.rowNumBottom, column = 4, columnspan = 1, sticky = E+W+N, pady = 10)
        Grid.columnconfigure(self.BottomCanvasFrame, 4, weight=1)
        self.SignalDistanceBottom.append(entry2)

        lbl3 = Label(self.BottomCanvasFrame, text= "Area of Signal", width = 12)
        lbl3.grid(row = self.rowNumBottom, column = 5, padx = 8, pady = 10)
        Grid.columnconfigure(self.BottomCanvasFrame, 5, weight=1)

        AreaEntry = Entry(self.BottomCanvasFrame, width=23)
        AreaEntry.grid(row = self.rowNumBottom, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
        Grid.columnconfigure(self.BottomCanvasFrame, 6, weight=1)
        self.SignalAreaBottom.append(AreaEntry)

        addButton = Button(self.BottomCanvasFrame, text="   +   ", command=lambda: self.AddButtonClicked("Bottom"))
        addButton.grid(row = self.rowNumBottom, column = 8, pady = 10, padx = 10)
        Grid.columnconfigure(self.BottomCanvasFrame, 8, weight=1)
        self.ButtonsBottom.append(addButton)

        b = IntVar()
        b.set(0)
        index = self.rowNumBottom
        checkButton = Checkbutton(self.BottomCanvasFrame, text="Is A Signal", variable=b, command=lambda: self.ClickOnSignal(index, b, "Bottom"), onvalue=1, offvalue=0)
        checkButton.grid(row=self.rowNumBottom, column = 9, pady = 10)
        Grid.columnconfigure(self.BottomCanvasFrame, 9, weight=1)
        self.IsSignalCheckButtonBottom.append(checkButton)
        self.IsSignalBottom.append(0)


    def AddButtonClicked(self, canvas):
        if canvas == 'Top':
            button = self.ButtonsTop[self.rowNumTop-1]
            button.grid_forget()
            self.rowNumTop += 1

            lbl1 = Label(self.TopCanvasFrame, text= "Signal/Sign Designation")
            lbl1.grid(row = self.rowNumTop, column = 0, padx = 7, pady = 10)

            entry1 = Entry(self.TopCanvasFrame)
            entry1.grid(row = self.rowNumTop, column = 1, columnspan = 2, sticky = E+W+N, pady = 10)
            self.SignalDesignationTop.append(entry1)

            lbl2 = Label(self.TopCanvasFrame, text= "Distance b/w Pole & Signal")
            lbl2.grid(row = self.rowNumTop, column = 3, padx = 8, pady = 10)

            entry2 = Entry(self.TopCanvasFrame)
            entry2.grid(row = self.rowNumTop, column = 4, columnspan = 1, sticky = E+W+N, pady = 10)
            self.SignalDistanceTop.append(entry2)

            lbl3 = Label(self.TopCanvasFrame, text= "Area of Signal", width = 12)
            lbl3.grid(row = self.rowNumTop, column = 5, padx = 8, pady = 10)

            AreaEntry = Entry(self.TopCanvasFrame, width=23)
            AreaEntry.grid(row = self.rowNumTop, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
            self.SignalAreaTop.append(AreaEntry)

            addButton = Button(self.TopCanvasFrame, text="   +   ", command=lambda: self.AddButtonClicked("Top"))
            addButton.grid(row = self.rowNumTop, column = 8, pady = 10, padx = 10)
            self.ButtonsTop.append(addButton)

            b = IntVar()
            b.set(0)
            index = self.rowNumTop
            checkButton = Checkbutton(self.TopCanvasFrame, text="Is A Signal", variable=b, command=lambda: self.ClickOnSignal(index, b, "Top"), onvalue=1, offvalue=0)
            checkButton.grid(row=self.rowNumTop, column = 9, pady = 10)
            self.IsSignalCheckButtonTop.append(checkButton)
            self.IsSignalTop.append(0)

        else:
            button = self.ButtonsBottom[self.rowNumBottom-1]
            button.grid_forget()
            self.rowNumBottom += 1
        

            lbl1 = Label(self.BottomCanvasFrame, text= "Signal/Sign Designation")
            lbl1.grid(row = self.rowNumBottom, column = 0, padx = 7, pady = 10)

            entry1 = Entry(self.BottomCanvasFrame)
            entry1.grid(row = self.rowNumBottom, column = 1, columnspan = 2, sticky = E+W+N, pady = 10)
            self.SignalDesignationBottom.append(entry1)

            lbl2 = Label(self.BottomCanvasFrame, text= "Distance b/w Pole & Signal")
            lbl2.grid(row = self.rowNumBottom, column = 3, padx = 8, pady = 10)

            entry2 = Entry(self.BottomCanvasFrame)
            entry2.grid(row = self.rowNumBottom, column = 4, columnspan = 1, sticky = E+W+N, pady = 10)
            self.SignalDistanceBottom.append(entry2)

            lbl3 = Label(self.BottomCanvasFrame, text= "Area of Signal", width = 12)
            lbl3.grid(row = self.rowNumBottom, column = 5, padx = 8, pady = 10)

            AreaEntry = Entry(self.BottomCanvasFrame, width=23)
            AreaEntry.grid(row = self.rowNumBottom, column = 6, columnspan = 2, sticky = E+W+N, pady = 10)
            self.SignalAreaBottom.append(AreaEntry)

            addButton = Button(self.BottomCanvasFrame, text="   +   ", command=lambda: self.AddButtonClicked("Bottom"))
            addButton.grid(row = self.rowNumBottom, column = 8, pady = 10, padx = 10)
            self.ButtonsBottom.append(addButton)

            b = IntVar()
            b.set(0)
            index = self.rowNumBottom
            checkButton = Checkbutton(self.BottomCanvasFrame, text="Is A Signal", variable=b, command=lambda: self.ClickOnSignal(index, b, "Bottom"), onvalue=1, offvalue=0)
            checkButton.grid(row=self.rowNumBottom, column = 9, pady = 10)
            self.IsSignalCheckButtonBottom.append(checkButton)
            self.IsSignalBottom.append(0)

def main():
    pass
    # root = Tk()
    # root.geometry("1050x600+200+100")
    # root.resizable(0,0)
    # root.tk_strictMotif()
    # root.iconbitmap('favicon.ico')
    # app = TwoArm(root)
    # root.mainloop()  

# if __name__ == '__main__':
#     main()  