#!/usr/local/bin/python

import cgi
import datetime
import json
from datetime import timedelta

launch = datetime.datetime(2012,01,01)
text = '../protected/odenCondensed.txt'
key = 'tale'

class oden:
	"""
		Slow-brewed story.
		Reveals 1 character per hour after launch.
	"""
	def __init__(self):
		self.file = text 
		self.made = launch 
	def told(self):
		"""
		Returns the character-hours since launch
		"""
		secs = toseconds(datetime.datetime.now() - self.made)
		return int(secs/3600)
	def tail(self,start):
		"""
		Given the character-hours you have, returns the rest of the story so far.
		"""
		return filetext(self.file)[start:self.told()]
	def till(self):
		"""
		Returns the number of seconds until the next character will be available.
		By default, on the next hour.
		"""
		now = datetime.datetime.now()
		if now.hour < 23:
			later = now.replace(hour=now.hour+1, minute=0, second=0, microsecond=0)
		else:
			later = now.replace(hour=0, minute=0, second=0, microsecond=0)
		return int(toseconds(later-now))
	def talk(self,start):
		"""
		Given character-hours, returns JSON object with rest of story so far and milliseconds until next character.
		"""
		return json.dumps({"till" : str(self.till()*1000), "tail" : self.tail(start)})
	
def toseconds(timedelta):
	"""Workaround for datetime.timedelta.to_seconds(), which is unsupported in Python 2.6.6"""
	return (timedelta.days * 3600 * 24) + timedelta.seconds

def filetext(file):
	"""Dump the full text of a file"""
	socket = open(file,'r')
	text = socket.read()
	socket.close()
	return text

def listen():
	"""
	API function.
	Client must POST form with key and character-hours to get a response.
	"""		
	form = cgi.FieldStorage()
	story = oden()
	if key in form:
		print "Content-Type: text/plain"
		print
		print story.talk(int(form[key].value))

listen()


