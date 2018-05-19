import threading as mt
import tweet_dumper as td
import re
import time
import requests 

class UpdateCenter():
	"""
		This class controls regular updates to the program GUI. It includes
	1 method to achieve this responsibility. The following discusses the goal
	of each method:
	#	update(self)
			- Input: it takes the default input "self" to get access to the 
					GUI and the status bar in the program.
			- Role: the method is run in a thread with wait time of 0.1s, so
					it runs in a rate of 10 times per second. The method pushes
					updates to (window dimensions) and (internet connectivity)
					of the program.
			- Output: N/A
	"""
	def __init__(self, main):
		self.GUI = main.GUI

		self.t1 = mt.Thread(target = self.update, name='Thread-1')
		self.t1.daemon = True
		self.t1.start()

	def update(self):

		print("process starts...")
		self.GUI.status_bar.connectivity_status.set(self.internet_on())
		while True:
			var = "{}x{}".format(self.GUI.winfo_width(), self.GUI.winfo_height())
			time.sleep(0.1)
			self.GUI.status_bar.dimensions.set(var)

	def internet_on(self):
		try:
			resp = requests.get('http://www.google.com')
			if resp.ok:
				return "Connected"
			else:
				return "Problem with requests.get()"
		except:
			return "Not connected"
		
class MainControl():
	"""
		This class controls comunications between GUI classes and actual program. It
	has 2 methods to achieve this reponsibility. The following explains the responsibility
	of each method:
	#	init()
			- Input: it takes the default (self) to get access to GUI
			- Role: it is an extension to the to the __init__() method. It will run
					one time at the beginning of the program. It will initialize the 
					log screen in the GUI
			- Output: N/A

	#	send_data()
			- Input: the default (self) to get access to the GUI and MainControl
					properties.
			- Role: it is called when send data button in the GUI. It starts by
					extracting the data from the GUI and validating them. Then,
					it initialize a process to run tweet_dumper in it.
			- Output: error_no

	#	validate_username()
			- Input: the default (self), and the username that needs to be validated
			- Role: Checks for all the components of the username entered to check if it
					follows the Twitter username standards. 
			- Output: it returns error_no = 0 if it is a valid name, and the error_no
					if otherwise.
	#
	"""

	#TODO: error control class
	#TODO: destination check
	#TODO: 
	
	def __init__(self, GUI):
		self.GUI = GUI
		self.twitter_username = '' #send to tweet_dumper (1)
		self.error_no = 0
		self.lang = 'en'   #send to tweet_dumper (2)
		self.dest = '' #send to tweet_dumper (3)
		self.downloading = False

		#self.send_data = SendData()
		self.update_center = UpdateCenter(self)
		self.init()

	def init(self):
		self.GUI.log_data.log.configure(state="normal")
		msg = "This is a message that has nothing to do with "
		msg = msg + "the program, yet is beneficial for debugging. "
		msg = msg + "I need this to go to the text field I created in the program as a test"
		self.GUI.log_data.log.insert(1.0, msg)
		self.GUI.log_data.log.configure(state="disabled")

	def send_data(self):
		self.twitter_username = self.GUI.tweet_input.twitter_username.get()
		if (self.GUI.tweet_input.lang.get() == 1):
			self.lang = 'en'
		else:
			self.lang = 'ar'
		self.dest = self.GUI.file_input.dest.get()

		(self.error_no, self.twitter_username) = self.validate_username(self.twitter_username)

		if self.error_no == 0:
			print("it went through.")
		else:
			print("error had occured. error number:{}".format(self.error_no))

	def validate_username(self, username):

		name = username
		if name == '': #check for empty text
			return 2, name #unsupported character
			print("empty")

		if name[0] == '@': #include usermnames starting with @
			if len(name) != 1:
				name = name.replace("@", "", 1)
			else: #if '@' was the only character entered
				return 2, name

		if len(name) > 15: #checks for string length
			return 1, name #string is too long
		else:
			if re.search("[^0-9a-zA-Z_]", name): #checks for illegal character
				return 2, name #unsupported character
			else:
				return 0, name

		return 0, name

