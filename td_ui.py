import tkinter as tk
from tkinter.filedialog import *
import getpass
import MainControl as mc
import tweet_dumper as td
		
class Titlebar(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.app_title = tk.Label(self,
			text = "Tweet Downloader App",
			font=("Helvetica", 18),
			pady = 10)

		self.app_title.pack()
class TweetInput(tk.Frame):
	def __init__(self, parent, *args, **kwargs):

		self.parent = parent
		tk.Frame.__init__(self, parent, *args, **kwargs)

		self.tweet_account_label = tk.Label(self,
			text = "Twitter Account:", #label text
			font=("Helvetica")).grid(row=1,column=0,sticky=tk.E)

		self.twitter_account = tk.StringVar() #stores value for tweet_account
		self.tweet_account = tk.Entry(self,
			textvariable = self.twitter_account).grid(row=1,column=1,sticky=tk.W, columnspan=100)
		self.language_label = tk.Label(self,
			text = "Language: ",
			font=("Helvetica")).grid(row=2,column=0,sticky=tk.E)

		self.lang = tk.IntVar() #stores value of chosen language
		self.radio_lang_en  = tk.Radiobutton(self, 
              text="English",
              variable=self.lang, 
              value=1).grid(row=2,column=1)
		self.radio_lang_ar = tk.Radiobutton(self, 
              text=("Arabic"),
              variable=self.lang, 
              value=2).grid(row=2,column=2)

		self.lang.set(1)

		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)

		self.grid_rowconfigure(2, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1,weight=1)
		self.grid_columnconfigure(2,weight=1)

	def getTweetAccount(self):
		twitterAccount = self.twitter_account.get()
		return twitterAccount

	def getLanguage(self):
		language = self.lang.get()
		return language
class FileInput(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.label = tk.Label(self,
			text = "File directory:",
			font=("Helvetica")).grid(row=1, column=0, sticky = tk.E)

		#make a default directory as an entry
		self.dest = tk.StringVar(self, value='/Users/{}/Documents/tweet_dumper'.format(getpass.getuser()))
		self.dest_entry = tk.Entry(self, textvariable= self.dest)
		self.dest_entry.grid(row=1,column=1,sticky=tk.W)

		#button to allow the user to choose custom destination
		self.choose_dir = tk.Button(self, text="choose",command = self.callback).grid(row=1,column=2)

		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=4)
		self.grid_columnconfigure(2, weight=1)

	def callback(self):
		print("FileInput: click!")
class Statusbar(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.dimensions = tk.StringVar()
		self.dimensions.set("1x1")
		print(self.dimensions.get())

		#prints the dimensions of the program window
		self.show_dimensions = tk.Label(self,
			textvariable = self.dimensions,
			font=("Helvetica")).grid(row=1, column=0)

		#prints the internet connectivity status
		self.connectivity_status = tk.StringVar()
		self.connected = tk.Label(self,
			textvariable = self.connectivity_status,
			font=("Helvetica")).grid(row=1, column=1)

		#prints whether data has been downloaded or not
		self.data_downloaded = tk.Label(self,
			text = "No data has been downloaded",
			font=("Helvetica")).grid(row=1, column=2)

		#TODO (2): fix the style for the status bar
class SendButton(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		#button to communicate with tweet_dumper
		self.choose_dir = tk.Button(self,
			text="Dowload Tweets",
			font=("Helvetica", 16),
			command = self.callback,
			width = 30).grid(row=1,column=0)

	def callback(self):
		print("SendButton: click!")
		self.parent.control_center.send_data()
class LogData(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		#text field to print log for program to use as a feedback method
		self.log = tk.Text(self,
			bg="#ECECEC",
			state="disabled")
		self.scrollbar = tk.Scrollbar(self)

		self.scrollbar.pack(side="right", fill="y")
		self.log.pack(side="left", fill="y")

		self.log.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.log.yview)

class MainApplication(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		#Initializers for the GUI
		self.parent.title("Tweet Downloader") #title at window top
		self.parent.geometry('640x480+300+150') #initial dimensions + position in screen
		self.parent.minsize(400,350) #set the minimum window size for the program

		#Build the GUI components by calling their classes
		self.title = Titlebar(self) #make title for GUI
		self.tweet_input = TweetInput(self, borderwidth = 3, relief="groove") #create input field
		self.file_input = FileInput(self, borderwidth = 2, relief="groove") #choose file destination
		self.status_bar = Statusbar(self, borderwidth = 3, relief="sunken", bg="#ECECEC") #show program status
		self.send_button = SendButton(self)
		self.log_data = LogData(self, borderwidth = 3, relief="sunken", width=500)
		self.control_center = mc.MainControl(self) #responsible for all updates to the program

		print("here1")

		self.status_bar.pack(fill="x", side="bottom")
		self.title.pack(side="top",fill="x",pady=10)
		self.tweet_input.pack(ipady=10,ipadx=10)
		self.file_input.pack(pady=20)
		self.send_button.pack()
		self.log_data.pack(pady=10)


if __name__ == "__main__":

	root = tk.Tk()
	MainApplication(root).pack(side="top", fill="both", expand=True)
	root.mainloop()
