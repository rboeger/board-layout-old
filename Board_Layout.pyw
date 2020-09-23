from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from fractions import Fraction
from math import gcd
import os
import Functions
#import tempfile
#mport win32api
#import win32print

#................................................Class for GUI.......................................
class Board_Layout:

	def __init__(self, master):
		self.master = master
		self.master.title("Board Layout Program")

		#.......................................Define Variables..........................................
		self.IsWood = BooleanVar()
		self.WidthPosition = 0
		self.WoodDepth1 = StringVar()
		self.WoodDepth2 = StringVar()
		self.HasBass = BooleanVar()
		self.BassNum = IntVar()
		self.PipeRows = IntVar()
		self.middle = 0
		self.distance = 0
		self.bassdistance = 0
		self.entry_pipenum = []
		self.entry_pipenum.append(0)
		self.firstrun = True
		self.XDistance = 0
		self.DistAdded = 0
		self.pipediameter = []
		self.piperadius = []
		self.pipeY = []
		self.lblResult = []
		for n in range(0, 74):
			self.pipediameter.append(0)
			self.piperadius.append(0)
			self.pipeY.append(0)
			self.lblResult.append(0)

		#........................................Set style for widgets........................................
		self.style = ttk.Style()
		self.style.configure('TButton', font=10)
		self.style.configure('TCheckbutton', font=10)
		self.style.configure('TLabel', font=12)
		self.style.configure('Big_Font.TLabel', font=('default',18))
		self.style.configure('Big_White.TLabel', font=('default', 18))
		#self.style.configure('Big_White.TLabel', font=('default', 18), background='white')
		#self.style.configure('TSeparator', background="black")
		self.style.configure('Bold.TLabel', font=("default", 12, 'bold'))
		self.style.configure('White.TLabel', font=('default', 12))
		#self.style.configure('White.TLabel', font=('default', 12),background='white')
		self.style.configure('White.TFrame')
		#self.style.configure('White.TFrame', background='white')

		#.......................................Create widgets for first window..............................
		self.master.option_add('*tearOff', False)
		self.master.title("Board Layout Helper")
		self.frmHeader = ttk.Frame(self.master)
		self.frmHeader.grid(row=0, column=0)
		self.frmHeader2 = ttk.Frame(self.master)
		self.frmHeader2.grid(row=1, column=0)
		self.frmHeader3 = ttk.Frame(self.master)
		self.frame = ttk.Frame(self.master)
		self.frame.grid(row=3, column=0)

		self.menubar = Menu(self.master)
		self.master.configure(menu = self.menubar)
		self.file = Menu(self.menubar)
		self.layout = Menu(self.menubar)
		self.help_ = Menu(self.menubar)
		self.rows = Menu(self.menubar)
		self.menubar.add_cascade(menu=self.file, label="File")
		self.menubar.add_cascade(menu=self.layout, label="Layout")
		self.menubar.add_cascade(menu=self.help_, label="Help")

		self.file.add_command(label="New")
		self.file.add_command(label="Save", command=self.save_data)
		self.file.add_command(label="Save As...")
		self.file.add_command(label="Load", command=self.load_click)

		self.layout.add_checkbutton(label="Wooden Pipes", command=self.add_Wood,
									variable=self.IsWood, onvalue=True, offvalue=False)
		self.layout.add_cascade(menu=self.rows, label="Rows")
		self.rows.add_radiobutton(label="One Row of Pipes", variable=self.PipeRows, value=1, command=self.selectonerow)
		self.rows.add_radiobutton(label="2 Rows of Pipes", variable=self.PipeRows, value=2)
		self.rows.add_checkbutton(label="Single Row of Bass Pipes", command=self.add_Bass,
									variable=self.HasBass, onvalue=True, offvalue=False)
		self.PipeRows.set(1)

		ttk.Label(self.frmHeader, text="Toe Board Information", style='Big_Font.TLabel').grid(row=0, column=0,
																							  columnspan=2, padx=5,
																							  pady=5)
		ttk.Label(self.frmHeader, text="Job Name:").grid(row=1, column=0, padx=5, pady=5)
		self.entJobName = ttk.Entry(self.frmHeader, width=30, font=10)
		self.entJobName.grid(row=1, column=1, padx=5, pady=5)

		ttk.Label(self.frmHeader, text="Rank Name:").grid(row=2, column=0, padx=5, pady=5)
		self.entRankName = ttk.Entry(self.frmHeader, width=30, font=10)
		self.entRankName.grid(row=2, column=1, padx=5, pady=5)

		ttk.Label(self.frmHeader2, text="Room on Sides:").grid(row=0, column=0, padx=5, pady=5)
		ttk.Label(self.frmHeader2, text="Room on Ends:").grid(row=0, column=2, padx=5, pady=5)
		self.entSideRoom = ttk.Entry(self.frmHeader2, width=8, font=10)
		self.entEndRoom = ttk.Entry(self.frmHeader2, width=8, font=10)
		self.entSideRoom.grid(row=0, column=1, padx=5, pady=5)
		self.entEndRoom.grid(row=0, column=3, padx=5, pady=5)

		self.lblWood1 = ttk.Label(self.frmHeader2, text="Wood Depth 1:")
		self.lblWood2 = ttk.Label(self.frmHeader2, text="Wood Depth 2:")
		self.entWood1 = ttk.Entry(self.frmHeader2, width=8, font=10, textvariable=self.WoodDepth1)
		self.entWood2 = ttk.Entry(self.frmHeader2, width=8, font=10, textvariable=self.WoodDepth2)

		self.lblBass = ttk.Label(self.frmHeader3, text="Number of Single Row Bass Pipes:")
		self.entBass = ttk.Entry(self.frmHeader3, width=8, font=10, textvariable=self.BassNum)
		self.lblBass.grid(row=2, column=0, padx=5, pady=5, stick='w')
		self.entBass.grid(row=2, column=1, padx=5, pady=5, stick='w')

		ttk.Separator(self.frame, orient=HORIZONTAL).grid(row=0, column=0, columnspan=10, sticky='ew', padx=5, pady=5)

		ttk.Label(self.frame, text="Diameter of Pipes",
				  style='Big_Font.TLabel').grid(row=1, column=0, columnspan=10, padx=5, pady=5)

		num = 1

		for n in range(2, 17):
			ttk.Label(self.frame, text="{}:".format(num)).grid(row=n, column=0)
			self.entry_pipenum.append(ttk.Entry(self.frame, width=8, text=num, font=10))
			self.entry_pipenum[num].grid(row=n, column=1, padx=5, pady=5)
			num += 1
		for n in range(2, 17):
			ttk.Label(self.frame, text="{}:".format(num)).grid(row=n, column=2)
			self.entry_pipenum.append(ttk.Entry(self.frame, width=8, text=num, font=10))
			self.entry_pipenum[num].grid(row=n, column=3, padx=5, pady=5)
			num += 1
		for n in range(2, 17):
			ttk.Label(self.frame, text="{}:".format(num)).grid(row=n, column=4)
			self.entry_pipenum.append(ttk.Entry(self.frame, width=8, text=num, font=10))
			self.entry_pipenum[num].grid(row=n, column=5, padx=5, pady=5)
			num += 1
		for n in range(2, 17):
			ttk.Label(self.frame, text="{}:".format(num)).grid(row=n, column=6)
			self.entry_pipenum.append(ttk.Entry(self.frame, width=8, text=num, font=10))
			self.entry_pipenum[num].grid(row=n, column=7, padx=5, pady=5)
			num += 1
		for n in range(2, 15):
			ttk.Label(self.frame, text="{}:".format(num)).grid(row=n, column=8)
			self.entry_pipenum.append(ttk.Entry(self.frame, width=8, text=num, font=10))
			self.entry_pipenum[num].grid(row=n, column=9, padx=5, pady=5)
			num += 1

		ttk.Button(self.frame, text='Calculate', command=self.cmdCalc).grid(row=15, column=8, columnspan=2,
																			rowspan=2, padx=5, pady=5,sticky='ns')

		self.master.protocol("WM_DELETE_WINDOW", self.on_closing)



		#...........................................Widgets for second window......................................
		#.................................................Result Window............................................

		self.results = Toplevel(self.master)
		self.results.state("withdrawn")

		self.frmresultY = ttk.Frame(self.results)
		self.frmresultY.grid(row=1, column=0, rowspan=10, padx=5, pady=5)
		self.frmRows = ttk.Frame(self.results, relief=RIDGE)
		self.frmRows.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
		self.frmAlign = ttk.Frame(self.results, relief=RIDGE)
		self.frmAlign.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
		self.frmTotals = ttk.Frame(self.results, relief=RIDGE)
		self.frmTotals.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

		ttk.Separator(self.frmresultY, orient=HORIZONTAL).grid(row=0, column=1, columnspan=15, sticky='ew')
		ttk.Separator(self.frmresultY, orient=VERTICAL).grid(row=0, column=0, rowspan=22, sticky='ns')

		for n in range(1, 17, 4):
			ttk.Label(self.frmresultY, text="#", style='Bold.TLabel').grid(row=1, column=n)
		for n in range(3, 17, 4):
			ttk.Label(self.frmresultY, text="Y", style='Bold.TLabel', width=8, anchor='center').grid(row=1, column=n)

		ttk.Separator(self.frmresultY, orient=HORIZONTAL).grid(row=2, column=1, columnspan=15, sticky='ew')

		num = 1
		for x in range(1, 13, 4):
			for n in range(3, 22):
				ttk.Label(self.frmresultY, text=num, style='Bold.TLabel').grid(row=n, column=x, padx=5, pady=8)
				num += 1

		for n in range(3, 19):
			ttk.Label(self.frmresultY, text=num, style='Bold.TLabel').grid(row=n, column=13, padx=5, pady=8)
			num += 1

		for n in range(2, 14, 2):
			ttk.Separator(self.frmresultY, orient=VERTICAL).grid(row=0, column=n, rowspan=22, sticky='ns')

		ttk.Separator(self.frmresultY, orient=VERTICAL).grid(row=0, column=14, rowspan=19, sticky='ns')
		ttk.Separator(self.frmresultY, orient=VERTICAL).grid(row=0, column=16, rowspan=19, sticky='ns')
		ttk.Separator(self.frmresultY, orient=HORIZONTAL).grid(row=22, column=0, columnspan=13, sticky='ew')
		ttk.Separator(self.frmresultY, orient=HORIZONTAL).grid(row=19, column=12, columnspan=4, sticky='new')

		if self.XDistance < 0:
			self.lblXDistance = ttk.Label(self.frmAlign, text="{} {}".format("X Overlap:", Functions.rulerfrac(abs(self.XDistance))))
		else:
			self.lblXDistance = ttk.Label(self.frmAlign, text="{} {}".format("X Distance:", Functions.rulerfrac(self.XDistance)))

		self.lblXDistance.pack(padx=3, pady=3, anchor='nw')
		self.lblYDistance = ttk.Label(self.frmAlign, text="{} {}".format("Y Distance:", self.distance))
		self.lblYDistance.pack(padx=3, pady=3, anchor='w')
		self.lblDistAdded = ttk.Label(self.frmAlign, text="{} {}".format("Dist Added:", self.DistAdded))
		self.lblDistAdded.pack(padx=3, pady=3, anchor='w')
		self.lblSideRoom = ttk.Label(self.frmAlign, text="{} {}".format("Sides:", self.entSideRoom.get()))
		self.lblSideRoom.pack(padx=3, pady=3, anchor='w')
		self.lblEndRoom = ttk.Label(self.frmAlign, text="{} {}".format("Ends:", self.entEndRoom.get()))
		self.lblEndRoom.pack(padx=3, pady=3, anchor='w')

		self.results.protocol('WM_DELETE_WINDOW', self.on_closing)


		#.................................Widgets for Load Window.....................................................
		self.Load = Toplevel(self.master)
		self.Load.state('withdrawn')

		ttk.Label(self.Load, text="Please select file to load:").grid(row=0, column=0, columnspan=2, padx=5, pady=5)
		self.listload = Listbox(self.Load, font=12, activestyle='none', width=40)
		self.listload.grid(row=1, column=0, columnspan=2)
		self.loadscroll = ttk.Scrollbar(self.Load, command=self.listload.yview)
		self.loadscroll.grid(row=1, column=1, sticky='nse')
		self.listload.config(yscrollcommand=self.loadscroll.set)

		self.onlyfiles = next(os.walk('save_data/'))[2]

		for files in self.onlyfiles:
			self.listload.insert(END, files[:-4])

		ttk.Button(self.Load, text="Load", command=self.load_button).grid(row=2, column=0, padx=5, pady=5)
		ttk.Button(self.Load, text="Cancel", command=lambda: self.Load.state('withdrawn')).grid(row=2, column=1, padx=5, pady=5)

		self.Load.protocol('WM_DELETE_WINDOW', lambda: self.Load.state('withdrawn'))


#.............................................Functions to call..................................
	#Function for when load button on load window is clicked
	def load_button(self):
		self.load_data(self.listload.get(ACTIVE))

	#Function for when results window is closed
	def on_closing(self):
		self.results.destroy()
		self.master.destroy()

	#Function for when "wood pipes" is clicked
	def add_Wood(self):
		if self.IsWood.get() == True:
			self.lblWood1.grid(row=1, column=0, padx=5, pady=5, stick='w')
			self.lblWood2.grid(row=1, column=2, padx=5, pady=5, stick='w')
			self.entWood1.grid(row=1, column=1, padx=5, pady=5, stick='w')
			self.entWood2.grid(row=1, column=3, padx=5, pady=5, stick='w')
		else:
			self.lblWood1.grid_remove()
			self.lblWood2.grid_remove()
			self.entWood1.grid_remove()
			self.entWood2.grid_remove()

	#Function for when "Single row of bass pipes" is clicked
	def add_Bass(self):
		if self.HasBass.get() == True:
			if self.PipeRows.get() == 2:
				self.frmHeader3.grid(row=2, column=0)
			else:
				messagebox.showerror("Error", "Cannot add single row of bass pipes unless 2 rows are selected!")
				self.HasBass.set(False)
		else:
			self.frmHeader3.grid_remove()

	#Function for when "1 row of pipes" is clicked
	def selectonerow(self):
		if self.HasBass.get() == True:
			self.HasBass.set(False)
			self.frmHeader3.grid_remove()

	#Function to save data to external file
	def save_data(self):
		self.savefile = open('save_data/{} - {}.txt'.format(self.entJobName.get(),self.entRankName.get()), "w+")
		self.savefile.write('{}\n'.format(self.entJobName.get()))
		self.savefile.write('{}\n'.format(self.entRankName.get()))
		self.savefile.write('{}\n'.format(self.entSideRoom.get()))
		self.savefile.write('{}\n'.format(self.entEndRoom.get()))
		self.savefile.write('{}\n'.format(self.IsWood.get()))
		self.savefile.write('{}\n'.format(self.HasBass.get()))
		self.savefile.write('{}\n'.format(self.PipeRows.get()))
		self.savefile.write('{}\n'.format(self.entWood1.get()))
		self.savefile.write('{}\n'.format(self.entWood2.get()))
		self.savefile.write('{}\n'.format(self.entBass.get()))
		for n in range(1, 74):
			self.savefile.write('{}\n'.format(self.entry_pipenum[n].get()))
		self.savefile.close()

	# Function to clear all text entry widgets on first window
	def clearall(self):
		self.entJobName.delete(0, END)
		self.entRankName.delete(0, END)
		self.entSideRoom.delete(0, END)
		self.entEndRoom.delete(0, END)
		self.entWood1.delete(0, END)
		self.entWood2.delete(0, END)
		self.entBass.delete(0, END)
		for n in range(1, 74):
			self.entry_pipenum[n].delete(0, END)

	#Function to clear extra entry widgets added for bass and wood pipes
	def clearextra(self):
		if self.HasBass.get() == False:
			self.frmHeader3.grid_remove()
		if self.IsWood.get() == False:
			self.lblWood1.grid_remove()
			self.lblWood2.grid_remove()
			self.entWood1.grid_remove()
			self.entWood2.grid_remove()

	#Function to load data from external file into program
	def load_data(self, file2load):
		self.clearall()

		with open('save_data/{}.txt'.format(file2load)) as file:
			self.entJobName.insert(0, file.readline()[:-1])
			self.entRankName.insert(0, file.readline()[:-1])
			self.entSideRoom.insert(0, file.readline() [:-1])
			self.entEndRoom.insert(0, file.readline()[:-1])
			self.IsWood.set(str2bool(file.readline()[:-1]))
			self.HasBass.set(str2bool(file.readline()[:-1]))
			self.PipeRows.set(int(file.readline()[:-1]))
			self.entWood1.insert(0, file.readline()[:-1])
			self.entWood2.insert(0, file.readline()[:-1])
			self.entBass.insert(0, int(file.readline()[:-1]))
			for n in range(1, 74):
				self.entry_pipenum[n].insert(0, file.readline()[:-1])

			if self.IsWood.get() == True:
				self.lblWood1.grid(row=1, column=0, padx=5, pady=5, stick='w')
				self.lblWood2.grid(row=1, column=2, padx=5, pady=5, stick='w')
				self.entWood1.grid(row=1, column=1, padx=5, pady=5, stick='w')
				self.entWood2.grid(row=1, column=3, padx=5, pady=5, stick='w')

			if self.HasBass.get() == True:
				self.frmHeader3.grid(row=2, column=0)

		self.clearextra()
		self.Load.state('withdrawn')

	#Function for when load button on top bar is clicked
	def load_click(self):
		self.Load.state('normal')
		self.Load.lift()

	#Function for when "Calculate" button is clicked
	def cmdCalc(self):
		#.......................................Find the first and last pipe......................................
		for n in range(1, 74):
			if self.entry_pipenum[n].get() != "":
				self.FirstPipe = n
				break

		for n in range(self.FirstPipe, 74):
			if self.entry_pipenum[n].get() == "":
				self.LastPipe = n-1
				break
			else:
				self.LastPipe = 73

		#Find total number of pipes
		if self.HasBass.get():
			self.FirstBassPipe = self.FirstPipe
			self.FirstPipe = self.FirstPipe + int(self.entBass.get())

		if self.HasBass.get():
			self.NumberofPipes = self.LastPipe + 1 - self.FirstBassPipe
		else:
			self.NumberofPipes = self.LastPipe + 1 - self.FirstPipe

		#.........................Convert string fractions into floats to use for math..............................
		if self.firstrun:
			self.sideroom = MakeFloat(self.entSideRoom.get())
			self.endroom = MakeFloat(self.entEndRoom.get())
			if self.IsWood.get():
				self.WoodDepth1 = MakeFloat(self.WoodDepth1.get())
				self.WoodDepth2 = MakeFloat(self.WoodDepth2.get())

			if self.HasBass.get():
				for n in range(self.FirstBassPipe, self.LastPipe + 1):
					self.pipediameter[n] = MakeFloat(self.entry_pipenum[n].get())
					self.piperadius[n] = self.pipediameter[n] / 2
			else:
				for n in range(self.FirstPipe, self.LastPipe+1):
					self.pipediameter[n] = MakeFloat(self.entry_pipenum[n].get())
					self.piperadius[n] = self.pipediameter[n] / 2

		#.....................................Find X values of pipes and total width...............................
		#Pipes ARE wood
		if self.IsWood.get():
			self.TotalWidth = (self.sideroom*2)+self.WoodDepth1
			self.row1x = XofRow1(self.sideroom, self.WoodDepth1)
			if self.PipeRows.get() == 2:
				self.TotalWidth += self.XDistance+self.WoodDepth2
				self.row2x = XofRow2(self.row1x, self.XDistance, self.WoodDepth1, self.WoodDepth2)
			else:
				self.row2x = "N/A"
		#Pipes AREN'T wood
		else:
			self.TotalWidth = (self.sideroom*2)+self.pipediameter[self.FirstPipe]
			self.row1x = XofRow1(self.sideroom, self.pipediameter[self.FirstPipe])
			if self.PipeRows.get() == 2:
				self.TotalWidth += self.XDistance+self.pipediameter[self.FirstPipe+1]
				self.row2x = XofRow2(self.row1x, self.XDistance, self.pipediameter[self.FirstPipe],
									 self.pipediameter[self.FirstPipe+1])
			else:
				self.row2x = "N/A"

		if self.HasBass.get():
			self.rowbassx = self.TotalWidth / 2

		else:
			self.rowbassx = "N/A"
			self.BassNum = "N/A"

		#.........................................Set Y value of pipes.......................................
		#Check for bass and then find Y of bass pipes and first non bass pipe
		if self.HasBass.get():
			self.pipeY[self.FirstBassPipe] = MakeFloat(self.entEndRoom.get())+(self.pipediameter[self.FirstBassPipe] / 2)

			for n in range(self.FirstBassPipe+1, self.FirstPipe):
				self.pipeY[n] = self.pipeY[n - 1] + (self.pipediameter[n - 1] / 2) + self.DistAdded + (self.pipediameter[n] / 2)

			self.pipeY[self.FirstPipe] = self.pipeY[self.FirstPipe-1] + +(self.pipediameter[self.FirstPipe-1]/2)+self.DistAdded+(self.pipediameter[self.FirstPipe]/2)
		else:
			self.pipeY[self.FirstPipe] = MakeFloat(self.entEndRoom.get())+(self.pipediameter[self.FirstPipe]/2)

		#Non bass pipes
		if self.PipeRows.get() == 2:
			#First row
			for n in range(self.FirstPipe+2, self.LastPipe+1, 2):
				self.pipeY[n] = self.pipeY[n-2]+self.piperadius[n-2]+self.distance+self.piperadius[n]
			#Second row
			for n in range(self.FirstPipe+1, self.LastPipe+1, 2):
				if n == self.LastPipe:
					if self.NumberofPipes % 2 == 0:
						self.pipeY[n] = self.pipeY[n-2] + self.piperadius[n-2] + self.distance + self.piperadius[n]
					else:
						self.pipeY[n] = (((self.pipeY[n+1]-(self.pipediameter[n+1]/2)) - (self.pipeY[n-1]+(self.pipediameter[n-1]/2))) / 2) + self.pipeY[n-1] + (self.pipediameter[n-1] / 2)
				else:
					self.pipeY[n] = (((self.pipeY[n + 1] - (self.pipediameter[n + 1] / 2)) - (
					self.pipeY[n - 1] + (self.pipediameter[n - 1] / 2))) / 2) + self.pipeY[n - 1] + (
									self.pipediameter[n - 1] / 2)
		else:
			#Single row
			for n in range(self.FirstPipe+1, self.LastPipe+1):
				self.pipeY[n] = self.pipeY[n-1]+(self.pipediameter[n-1]/2)+self.distance+(self.pipediameter[n]/2)
		for n in range(self.FirstPipe+1, self.LastPipe+1):
			if self.pipeY[n] - self.pipeY[n-1] < 0.75:
				self.pipeY[n] = self.pipeY[n-1] + 0.75

		self.results.title("{} - {} Layout".format(self.entJobName.get(),self.entRankName.get()))
		ttk.Label(self.results, text="{} - {}".format(self.entJobName.get(), self.entRankName.get()),
				  style='Big_Font.TLabel').grid(row=0, column=0, columnspan=2, padx=5, pady=5)
		self.master.state("withdrawn")
		self.results.state("normal")
		self.results.lift()

		# Show results on result window
		if self.firstrun:
			self.LengthPosition = 0
			num = 1
			for x in range(3, 15, 4):
				for n in range(3, 22):
					self.lblResult[num] = ttk.Label(self.frmresultY, text=Functions.rulerfrac(self.pipeY[num]))
					self.lblResult[num].grid(row=n, column=x, padx=2, pady=6, sticky='w')
					num += 1
			for n in range(3, 19):
				self.lblResult[num] = ttk.Label(self.frmresultY, text=Functions.rulerfrac(self.pipeY[num]))
				self.lblResult[num].grid(row=n, column=15, padx=2, pady=6, sticky='w')
				num += 1

			if self.XDistance < 0:
				self.lblXDistance.config(text="{} {}".format("X Overlap:", Functions.rulerfrac(abs(self.XDistance))))
			else:
				self.lblXDistance.config(text="{} {}".format("X Distance:", Functions.rulerfrac(self.XDistance)))

			self.lblYDistance.config(text="{} {}".format("Y Distance:", self.distance))
			self.lblDistAdded.config(text="{} {}".format("Dist Added:", self.DistAdded))
			self.lblSideRoom.config(text="{} {}".format("Sides:", self.entSideRoom.get()))
			self.lblEndRoom.config(text="{} {}".format("Ends:", self.entEndRoom.get()))
		else:
			self.Update()

		#Check if each row is being used and convert into fraction if so
		if isinstance(self.row1x, float):
			self.row1x = Functions.rulerfrac(self.row1x)
		if isinstance(self.row2x, float):
			self.row2x = Functions.rulerfrac(self.row2x)

		#Create labels to display rows
		if self.firstrun:
			self.lblRow1X = ttk.Label(self.frmRows, text="{} {}".format("Row One:",self.row1x))
			self.lblRow1X.pack(padx=3, pady=3, anchor='nw')
			self.lblRow2X = ttk.Label(self.frmRows, text="{} {}".format("Row Two:",self.row2x))
			self.lblRow2X.pack(padx=3, pady=3, anchor='w')
			if self.HasBass.get():
				self.lblRowMidX = ttk.Label(self.frmRows, text="{} {}".format("Middle Row:",Functions.rulerfrac(self.rowbassx)))
			else:
				self.lblRowMidX = ttk.Label(self.frmRows, text="{} {}".format("Middle Row:", self.rowbassx))
			self.lblRowMidX.pack(padx=3, pady=3, anchor='w')
			if self.HasBass.get():
				ttk.Label(self.frmRows, text="{} {}".format("Bass Pipes:", self.BassNum.get())).pack(padx=3, pady=3, anchor='w')
			else:
				ttk.Label(self.frmRows, text="{} {}".format("Bass Pipes:", self.BassNum)).pack(padx=3, pady=3, anchor='w')

		if self.firstrun:
			self.XDistance = 0
			self.DistAdded = 0

		#Calculate total length of toe board
		self.TotalLength = self.pipeY[self.LastPipe] + self.piperadius[self.LastPipe] + self.endroom

		if self.firstrun:
			self.lblTotalLength = ttk.Label(self.frmTotals, width=21, text="{} {}".format("Total Length:", Functions.rulerfrac(self.TotalLength)))
			self.lblTotalLength.grid(row=0, column=0, columnspan=2, padx=3, pady=3, sticky='w')
			ttk.Button(self.frmTotals, text="-", width=5, command=self.DecLength).grid(row=1, column=0, padx=3, pady=2, sticky='ew')
			ttk.Button(self.frmTotals, text="+", width=5, command=self.IncLength).grid(row=1, column=1, padx=3, pady=2, sticky='ew')

			self.lblTotalWidth = ttk.Label(self.frmTotals, text="{} {}".format("Total Width:", Functions.rulerfrac(self.TotalWidth)))
			self.lblTotalWidth.grid(row=2, column=0, columnspan=2, padx=3, pady=3, sticky='w')
			ttk.Button(self.frmTotals, text="-", width=5, command=self.DecWidth).grid(row=3, column=0, padx=3, pady=2, sticky='ew')
			ttk.Button(self.frmTotals, text="+", width=5, command=self.IncWidth).grid(row=3, column=1, padx=3, pady=2, sticky='ew')
			ttk.Button(self.frmTotals, text="Print To File", command=self.printlayout).grid(row=4, column=0, pady=3, padx=3, sticky='ew', columnspan=2)

		self.firstrun = False
		self.lblTotalLength.config(text="{} {}".format("Total Length:", Functions.rulerfrac(self.TotalLength)))

	#Method to print layout to a file for printing later
	def printlayout(self):
		safe_jobname = ""
		for letters in self.entJobName.get():
			if letters == " ":
				new_letter = r"\ "
			elif letters == "'":
				new_letter = r"\'"
			else:
				new_letter = letters

			safe_jobname = "{}{}".format(safe_jobname, new_letter)

		# safe_rankname = ""

		# for letters in self.entRankName.get():
		#     if letters == " ":
		#         new_letter = r"\ "
		#     elif letters == "'":
		#         new_letter = r"\'"
		#     else:
		#         new_letter = letters

		#     safe_jobname = "{}{}".format(safe_jobname, new_letter)

		os.system("mkdir {}/print_files/{}".format(os.getcwd(), safe_jobname))
		filename = "{}{} -  {}{}".format("print_files/{}/".format(self.entJobName.get()),self.entJobName.get(),self.entRankName.get(),".txt")
		Functions.print2newfile(filename, "Job:", self.entJobName.get(),
							" 1:", Functions.rulerfrac(self.pipeY[1]), "38:", Functions.rulerfrac(self.pipeY[38]))

		Functions.print2file(filename, "Rank:", self.entRankName.get(),
								" 2:", Functions.rulerfrac(self.pipeY[2]), "39:", Functions.rulerfrac(self.pipeY[39]))

		Functions.print2file(filename, "", "",
							 " 3:", Functions.rulerfrac(self.pipeY[3]), "40:", Functions.rulerfrac(self.pipeY[40]))

		Functions.print2file(filename, "Side Room:", self.entSideRoom.get(),
							" 4:", Functions.rulerfrac(self.pipeY[4]), "41:", Functions.rulerfrac(self.pipeY[41]))

		Functions.print2file(filename, "EndRoom:", self.entEndRoom.get(),
							" 5:", Functions.rulerfrac(self.pipeY[5]), "42:", Functions.rulerfrac(self.pipeY[42]))

		Functions.print2file(filename, "", "",
							 " 6:", Functions.rulerfrac(self.pipeY[6]), "43:", Functions.rulerfrac(self.pipeY[43]))

		if self.HasBass.get():
			Functions.print2file(filename, "Bass Pipes:", self.BassNum.get(),
								" 7:", Functions.rulerfrac(self.pipeY[7]), "44:", Functions.rulerfrac(self.pipeY[44]))
		else:
			Functions.print2file(filename, "Bass Pipes:", self.BassNum,
								 " 7:", Functions.rulerfrac(self.pipeY[7]), "44:", Functions.rulerfrac(self.pipeY[44]))

		Functions.print2file(filename, "Wood Pipes:", self.IsWood.get(),
							" 8:", Functions.rulerfrac(self.pipeY[8]), "45:", Functions.rulerfrac(self.pipeY[45]))

		Functions.print2file(filename, "", "",
							 " 9:", Functions.rulerfrac(self.pipeY[9]), "46:", Functions.rulerfrac(self.pipeY[46]))

		Functions.print2file(filename, "Number of Rows:", self.PipeRows.get(),
							"10:", Functions.rulerfrac(self.pipeY[10]), "47:", Functions.rulerfrac(self.pipeY[47]))

		Functions.print2file(filename, "Row 1 X:", self.row1x,
							"11:", Functions.rulerfrac(self.pipeY[11]), "48:", Functions.rulerfrac(self.pipeY[48]))

		Functions.print2file(filename, "Row 2 X:", self.row2x,
							"12:", Functions.rulerfrac(self.pipeY[12]), "49:", Functions.rulerfrac(self.pipeY[49]))

		if self.HasBass.get():
			Functions.print2file(filename, "Row Mid X:", Functions.rulerfrac(self.rowbassx),
								 "13:", Functions.rulerfrac(self.pipeY[13]), "50:", Functions.rulerfrac(self.pipeY[50]))
		else:
			Functions.print2file(filename, "Row Mid X:", self.rowbassx,
								"13:", Functions.rulerfrac(self.pipeY[13]), "50:", Functions.rulerfrac(self.pipeY[50]))

		Functions.print2file(filename, "", "",
							 "14:", Functions.rulerfrac(self.pipeY[14]), "51:", Functions.rulerfrac(self.pipeY[51]))

		Functions.print2file(filename, "Y Distance:", Functions.rulerfrac(self.distance),
							 "15:", Functions.rulerfrac(self.pipeY[15]), "52:", Functions.rulerfrac(self.pipeY[52]))

		if self.XDistance < 0:
			Functions.print2file(filename, "X Overlap:", Functions.rulerfrac(abs(self.XDistance)),
							 	"16:", Functions.rulerfrac(self.pipeY[16]), "53:", Functions.rulerfrac(self.pipeY[53]))
		else:
			Functions.print2file(filename, "X Distance:", Functions.rulerfrac(self.XDistance),
							 	"16:", Functions.rulerfrac(self.pipeY[16]), "53:", Functions.rulerfrac(self.pipeY[53]))

		if self.HasBass.get():
			Functions.print2file(filename, "Bass Distance:", Functions.rulerfrac(self.DistAdded),
								"17:", Functions.rulerfrac(self.pipeY[17]), "54:", Functions.rulerfrac(self.pipeY[54]))
		else:
			Functions.print2file(filename, "Bass Distance:", "N/A",
								 "17:", Functions.rulerfrac(self.pipeY[17]), "54:", Functions.rulerfrac(self.pipeY[54]))

		Functions.print2file(filename, "", "",
							 "18:", Functions.rulerfrac(self.pipeY[18]), "55:", Functions.rulerfrac(self.pipeY[55]))

		Functions.print2file(filename, "Total Length:", Functions.rulerfrac(self.TotalLength),
							 "19:", Functions.rulerfrac(self.pipeY[19]), "56:", Functions.rulerfrac(self.pipeY[56]))

		Functions.print2file(filename, "Total Width:", Functions.rulerfrac(self.TotalWidth),
							 "20:", Functions.rulerfrac(self.pipeY[20]), "57:", Functions.rulerfrac(self.pipeY[57]))

		r1 = 21
		r2 = 58
		for x in range(0, 16):
			Functions.print2file(filename, "", "",
								"{}{}".format(r1, ":"), Functions.rulerfrac(self.pipeY[r1]), "{}{}".format(r2, ":"),
								Functions.rulerfrac(self.pipeY[r2]))
			r1+=1; r2+=1

		Functions.print2file(filename, "", "","37:", Functions.rulerfrac(self.pipeY[37]), "", "")

		messagebox.showinfo("Info", "Successfully saved to file!")

		safe_filename = ""
		for letters in filename:
			if letters == " ":
				new_letter = r"\ "
			elif letters == "'":
				new_letter = r"\'"
			else:
				new_letter = letters

			safe_filename = "{}{}".format(safe_filename, new_letter)

		# Opens file in text editor
		os.system("gedit {}/{}".format(os.getcwd(), safe_filename))

		# Prints file to default printer
		# os.system("lpr {}/{}".format(os.getcwd(), safe_filename))


	#Method to update result page
	def Update(self):
		self.lblTotalLength.config(text="{} {}".format("Total Length:", Functions.rulerfrac(self.TotalLength)))
		self.lblTotalWidth.config(text="{} {}".format("Total Width:", Functions.rulerfrac(self.TotalWidth)))
		self.lblRow1X.config(text="{} {}".format("Row One:", Functions.rulerfrac(self.row1x)))
		self.lblRow2X.config(text="{} {}".format("Row Two:", Functions.rulerfrac(self.row2x)))
		if self.HasBass.get():
			self.lblRowMidX.config(text="{} {}".format("Middle Row:", Functions.rulerfrac(self.rowbassx)))
		else:
			self.lblRowMidX.config(text="{} {}".format("Middle Row:", self.rowbassx))
		if self.HasBass.get():
			for n in range(self.FirstBassPipe, self.LastPipe+1):
				self.lblResult[n].config(text=Functions.rulerfrac(self.pipeY[n]))
		else:
			for n in range(self.FirstPipe, self.LastPipe+1):
				self.lblResult[n].config(text=Functions.rulerfrac(self.pipeY[n]))

		if self.XDistance < 0:
			self.XRelation = "Overlap"
			self.lblXDistance.config(text="{} {}".format("X Overlap:", Functions.rulerfrac(abs(self.XDistance))))
		else:
			self.XRelation = "Distance"
			self.lblXDistance.config(text="{} {}".format("X Distance:", Functions.rulerfrac(self.XDistance)))

		self.lblYDistance.config(text="{} {}".format("Y Distance:", Functions.rulerfrac(self.distance)))
		self.lblDistAdded.config(text="{} {}".format("Dist Added:", Functions.rulerfrac(self.DistAdded)))
		self.lblSideRoom.config(text="{} {}".format("Sides:", self.entSideRoom.get()))
		self.lblEndRoom.config(text="{} {}".format("Ends:", self.entEndRoom.get()))

	#Method for when length is increased
	def IncLength(self):
		self.distance += 0.0625
		self.LengthPosition += 1
		self.DistAdded = self.LengthPosition * 0.0625
		self.cmdCalc()


	#Method for when length is decreased
	def DecLength(self):
		if self.LengthPosition > 0:
			self.distance -= 0.0625
			self.LengthPosition -= 1
			self.DistAdded = self.LengthPosition * 0.0625
			self.cmdCalc()

	#Method for when width is increased
	def IncWidth(self):
		self.XDistance += .0625

		if self.XDistance >= 0:
			self.distance = 0
		else:

			if self.IsWood.get():
				self.WidthPosition += 1

			self.Pipe1Width = self.pipediameter[self.FirstPipe]
			self.Pipe2Width = self.pipediameter[self.FirstPipe + 1]
			self.Pipe3Width = self.pipediameter[self.FirstPipe + 2]

			if not self.IsWood.get():
				self.ChordLength1 = Functions.ChordLength(self.Pipe1Width / 2, ((self.Pipe1Width / 2) - abs(self.XDistance)))
				self.ChordLength2 = Functions.ChordLength(self.Pipe2Width / 2, ((self.Pipe2Width / 2) - abs(self.XDistance)))
				self.ChordLength3 = Functions.ChordLength(self.Pipe3Width / 2, ((self.Pipe3Width / 2) - abs(self.XDistance)))
				self.ChordRemainder1 = (self.Pipe1Width - self.ChordLength1) / 2
				self.ChordRemainder3 = (self.Pipe3Width - self.ChordLength3) / 2

				self.distance = self.ChordLength2 - (self.ChordRemainder1 + self.ChordRemainder3)

				if self.distance < 0:
					self.distance = 0

				self.LengthPosition = 0
				self.DistAdded = 0

		self.cmdCalc()

	#Method for when width is decreased
	def DecWidth(self):
		if self.XDistance > 0:
			self.XDistance = self.XDistance - .0625
		else:
			if self.IsWood.get():
				if self.WidthPosition > 0:
					self.WidthPosition -= 1
					self.XDistance -= .0625
				else:
					messagebox.showerror("Error", "Cannot decrease width if pipes are wood!")

			else:
				if self.HasBass.get():
					if (self.sideroom * 2) + self.pipediameter[self.FirstBassPipe] >= self.TotalWidth:
						messagebox.showerror("Error", "Cannot decrease width any more!")
					else:
						self.XDistance -= .0625

						self.Pipe1Width = self.pipediameter[self.FirstPipe]
						self.Pipe2Width = self.pipediameter[self.FirstPipe + 1]
						self.Pipe3Width = self.pipediameter[self.FirstPipe + 2]

						self.ChordLength1 = Functions.ChordLength(self.Pipe1Width / 2, ((self.Pipe1Width / 2) - abs(self.XDistance)))
						self.ChordLength2 = Functions.ChordLength(self.Pipe2Width / 2, ((self.Pipe2Width / 2) - abs(self.XDistance)))
						self.ChordLength3 = Functions.ChordLength(self.Pipe3Width / 2, ((self.Pipe3Width / 2) - abs(self.XDistance)))
						self.ChordRemainder1 = (self.Pipe1Width - self.ChordLength1) / 2
						self.ChordRemainder3 = (self.Pipe3Width - self.ChordLength3) / 2

						self.distance = self.ChordLength2 - (self.ChordRemainder1 + self.ChordRemainder3)

						if self.distance < 0:
							self.distance = 0

						self.LengthPosition = 0
						self.DistAdded = 0
				else:
					self.XDistance -= .0625

					self.Pipe1Width = self.pipediameter[self.FirstPipe]
					self.Pipe2Width = self.pipediameter[self.FirstPipe + 1]
					self.Pipe3Width = self.pipediameter[self.FirstPipe + 2]

					self.ChordLength1 = Functions.ChordLength(self.Pipe1Width / 2,
															  ((self.Pipe1Width / 2) - abs(self.XDistance)))
					self.ChordLength2 = Functions.ChordLength(self.Pipe2Width / 2,
															  ((self.Pipe2Width / 2) - abs(self.XDistance)))
					self.ChordLength3 = Functions.ChordLength(self.Pipe3Width / 2,
															  ((self.Pipe3Width / 2) - abs(self.XDistance)))
					self.ChordRemainder1 = (self.Pipe1Width - self.ChordLength1) / 2
					self.ChordRemainder3 = (self.Pipe3Width - self.ChordLength3) / 2

					self.distance = self.ChordLength2 - (self.ChordRemainder1 + self.ChordRemainder3)

					if self.distance < 0:
						self.distance = 0

					self.LengthPosition = 0
					self.DistAdded = 0

		self.cmdCalc()

#Function to convert fraction into float
def MakeFloat(stringfrac):
	return float(sum(Fraction(s) for s in stringfrac.split()))

#Function to find x of first row
def XofRow1(sideroom, firstpipe):
	return sideroom+(firstpipe/2)

#Function to find x of second row
def XofRow2(x1, middle, firstpipe, secondpipe):
	return x1+(firstpipe/2)+middle+(secondpipe/2)

#Function to convert string to boolean
def str2bool(str):
	return str.lower() in "true"

if __name__ == "__main__":
	root = Tk()
	app = Board_Layout(root)
	root.mainloop()
