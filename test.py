#/usr/bi/python

import RPi.GPIO as GPIO
import time, sys

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

statusModePressed = 0 # 0 on a PullUp circuit, 1 on a PullDown circuit

history = []
lastStatus = -1
lastTime = 0.0


def switchEvent(channel):
	global lastStatus, switch, history, mode, lastTime
	eps = 0.01
	tm = time.time()

	status = GPIO.input(switch)

	print(tm-lastTime, " channel ", channel," status:", GPIO.input(switch))

	if mode == PLAYBACK:
		mode = RECORDING
		print( "turned to recording" )
		history = []
	else:
		history.append(tm)

	GPIO.output(redLED, 0)
	channel = GPIO.wait_for_edge(switch,GPIO.RISING,2000)
	print( channel, " EDGE")
	if channel is None:

		mode = PLAYBACK	

	GPIO.output(redLED, 0)

#GPIO.add_event_detect(switch, GPIO.FALLING, bouncetime=50)
#GPIO.add_event_callback(switch, switchEvent)

def play(duration):
	print("play ", duration)
	ledDuration = 0.2
	GPIO.output(redLED, 1)
	time.sleep( ledDuration )
	GPIO.output(redLED, 0)
	if duration - ledDuration > 0.0:
		time.sleep(duration - ledDuration)


## main

try:
	while True:
		if mode == PLAYBACK:
			playbackPos = playbackPos + 1
			if playbackPos == len(history):
				playbackPos = 1
			print("play ", playbackPos, " " , len(history))
			play(history[playbackPos] - history[playbackPos-1])
		else:
			channel = GPIO.wait_for_edge(switch,GPIO.FALLING,1000)
			if channel != 0:	
				switchEvent(channel)

except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()
