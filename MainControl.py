import threading as mt
import tweet_dumper as td
import time
import requests 

class UpdateCenter():
	"""docstring for UpdateCenter"""
	def __init__(self, main):
		self.main = main
		self.GUI = main.GUI

		self.t1 = mt.Thread(target = self.update, name='Thread-1')
		self.t1.daemon = True
		self.t1.start()

	def update(self):

		print("process starts...")
		self.GUI.status_bar.connectivity_status.set(self.internet_on())
		while True:
			var = "{}x{}".format(self.GUI.winfo_width(), self.GUI.winfo_height())
			#time.sleep(0.05)
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

	def send_data(self):
		twitter_username = self.twitter_username
		lang = self.lang
		dest = self.dest