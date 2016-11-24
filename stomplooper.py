#!/usr/bin/python

import RPi.GPIO as GPIO
import time, sys
from threading import Timer

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
timerThread = 0

statusModePressed = 0 # 0 on a PullUp circuit, 1 on a PullDown circuit

history = []
lastStatus = 1
lastTime = 0.0

def stop_recording():
	print("break")

def switchEvent(channel):
	global lastStatus, switch, history, mode, lastTime, timerThread
	eps = 0.01
	status = 1 - lastStatus
	lastStatus = status
	tm = time.time()

	diff = "" if GPIO.input(switch) == status else "DIFF"
	print(tm-lastTime, " status:", status, " ", diff)
	lastTime = tm

	if status == statusModePressed:
		if mode == PLAYBACK:
			mode = RECORDING
			print( "turned to recording" )
			history = []
		else:
			history.append(tm)
			timerThread = Timer(1, stop_recording(), ())
			timerThread.start()
#	else:
#		if timerThread != 0:
#			timerThread.cancel()

	GPIO.output(redLED, 1 - status)

GPIO.add_event_detect(switch, GPIO.BOTH, bouncetime=20)
GPIO.add_event_callback(switch, switchEvent)

def play(duration):
	print("play ", duration)
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
