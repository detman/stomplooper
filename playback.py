#!/usr/bin/python

import time
import threading

class Playback(threading.Thread): 
 
    def __init__(self, recorder): 
		threading.Thread.__init__(self) 
		self.stopped = False
		self.recorder = recorder
		print("init playbackThread")

    def run(self): 
		print("playback start")
		i=0
		print self.recorder.recordings
		print i,len(self.recorder.recordings)
		while True:
			if self.stopped:
				print("playback stopped")
				return
			h = self.recorder.recordings[i]
			t1 = time.time()
			self.play(h)
			t2 = time.time()
			time.sleep(h - (t2-t1))
			i = i+1
			if i == len(self.recorder.recordings):
				i = 0
		print("playback finished")
		self.stopped = True

    def stop(self): 
		self.stopped = True

    def play(self,duration): 
		print duration
