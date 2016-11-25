#!/usr/bin/python

import RPi.GPIO as GPIO
import time, sys
import threading

redLED = 23
switch = 21
ledStatus = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch, GPIO.IN)
GPIO.setup(redLED, GPIO.OUT)
GPIO.output(redLED, ledStatus)


RECORDING = 0
PLAYBACK  = 1
mode = RECORDING
playbackPos = -1
timerThread = None

statusModePressed = 0 # 0 on a PullUp circuit, 1 on a PullDown circuit

lastStatus = 1
lastTime = 0.0

class playbackThread(threading.Thread): 
 
    def __init__(self): 
		threading.Thread.__init__(self) 
		self.stopped = False
		self.lastHit = 0
		self.history = []
		print("init playbackThread")

    def run(self): 
		print("playback start")
		i=0;
		while True:
			h = self.history[i]
			if self.stopped:
				print("playback stopped")
				return
			print(i,h)
			light(h)
			i = i+1
			if i == len(self.history):
				i = 0
		print("playback finished")
		self.stopped = True

    def pressed(self): 
		now = time.time();
		if self.lastHit != 0:
			self.history.append(now-self.lastHit)
			print(len(self.history), " ", self.history[-1]);
		self.lastHit = now

    def stop(self): 
		self.stopped = True

playback = None

def start_playback():
	global playback
	playback.start()

def switchEvent(channel):
	global lastStatus, switch, history, mode, lastTime, timerThread, playback
	eps = 0.01
	status = 1 - lastStatus
	lastStatus = status
	tm = time.time()

	diff = "" if GPIO.input(switch) == status else "DIFF"
	#print(tm-lastTime, " status:", status, " ", diff)
	lastTime = tm

	if status == statusModePressed:
		if playback != None:
			if playback.is_alive():
				playback.stop()
			if playback.stopped: # may be finished or stopped
				playback = None

		if playback == None:
			playback = playbackThread()

		playback.pressed()
		timerThread = threading.Timer(1, start_playback, ())
		timerThread.daemon = True
		timerThread.start()
	else:
		if timerThread != None:
			timerThread.cancel()

	GPIO.output(redLED, 1 - status)

GPIO.add_event_detect(switch, GPIO.BOTH, bouncetime=20)
GPIO.add_event_callback(switch, switchEvent)

def light(duration):
	ledDuration = 0.1
	GPIO.output(redLED, 1)
	time.sleep( ledDuration )
	GPIO.output(redLED, 0)
	if duration - ledDuration > 0.0:
		time.sleep(duration - ledDuration)


## main

try:
	while True:
		time.sleep(5)
except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()
