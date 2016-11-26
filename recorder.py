#!/usr/bin/python

import time

class Recorder(object):

    def __init__(self): 
		self.recordings = []
		self.lastRecord = 0
		print("init Recorder")

    def record(self): 
		now = time.time();
		if self.lastRecord != 0:
			self.recordings.append(now-self.lastRecord)
			print(len(self.recordings), " ", self.recordings[-1]);
		self.lastRecord = now

    def empty(self): 
		return len(self.recordings) > 0

