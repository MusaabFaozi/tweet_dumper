import threading as mt
import tweet_dumper as td
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

class SendData():
	"""docstring for SendData"""
	def __init__(self, twitter_username, lang, dest):
		self.twitter_username = twitter_username
		self.lang = lang
		self.dest = dest
		
class MainControl():
	"""
		This class controls comunications between GUI classes and actual program. It
	has 0 methods to achieve this reponsibility. The following explains the responsibility
	of each method:
	#	
	#
	#
	#
	"""
	def __init__(self, GUI):
		self.GUI = GUI
		self.twitter_username = '' #send to tweet_dumper (1)
		self.validated = True
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
		twitter_username = self.twitter_username
		lang = self.lang
		dest = self.dest

