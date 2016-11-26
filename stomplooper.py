#!/usr/bin/python

import RPi.GPIO as GPIO
import time, sys
import threading

from playback import Playback
from recorder import Recorder
from momentarybutton import MomentaryButton

redLED = 23
switch = 21

GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch, GPIO.IN)

GPIO.setup(redLED, GPIO.OUT)
GPIO.output(redLED, 0)

class LEDBlinker(Playback):

	def play(self,duration):
		ledDuration = 0.1
		GPIO.output(redLED, 1)
		time.sleep( ledDuration )
		GPIO.output(redLED, 0)
		
class MyButton(MomentaryButton):

	def __init__(self,pin,statusModePressed, bouncetime):
		MomentaryButton.__init__(self,pin,statusModePressed, bouncetime)
		self.recorder = Recorder()
		self.playback = None

	def pressed(self):
		print "pressed"
		GPIO.output(redLED, 1)
		if self.playback != None:
			if self.playback.is_alive():
				self.playback.stop()
				self.recorder = Recorder() # create new recorder; drop old recording
			if self.playback.stopped: # may be finished or stopped
				self.playback = None
		self.recorder.record()

	def pressedLong(self):
		print "pressed long"
		self.playback = LEDBlinker(self.recorder.recordings)
		self.playback.start()

	def released(self):
		print "released"
		GPIO.output(redLED, 0)

## main

bttn = MyButton(switch,0, 2)

try:
	while True:
		time.sleep(5)
except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()

