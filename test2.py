#!/usr/bin/python

import RPi.GPIO as GPIO
import time, sys

redLED = 23
switch = 21
DOWN = 0
UP = 1
ledStatus = 0
status = UP

GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch, GPIO.IN)
GPIO.setup(redLED, GPIO.OUT)
GPIO.output(redLED, ledStatus)


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
		if status == UP:
			GPIO.wait_for_edge(switch,GPIO.BOTH)
			GPIO.output(redLED, 1)
			status = DOWN
		else:
			channel = GPIO.wait_for_edge(switch,GPIO.BOTH, 1000)
			GPIO.output(redLED, 0)
			if channel == 0:
				print("BREAK")
			status = UP
except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()
