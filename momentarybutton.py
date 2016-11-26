#!/usr/bin/python
import RPi.GPIO as GPIO
import threading
import time

class MomentaryButton(object):
	def __init__(self,pin,statusModePressed, bouncetime):
		self.pin = pin
		self.status = 1
		self.timerThread = None
		self.statusModePressed = statusModePressed # 0 on a PullUp circuit, 1 on a PullDown circuit

		def callback(channel):
			time.sleep(0.005)
			gpiostatus = GPIO.input(pin)
			if gpiostatus == self.status:
				return
			self.status = 1 - self.status
			print self.status
			if self.status == self.statusModePressed:
				def timerEvent():
					self.pressedLong()

				self.timerThread = threading.Timer(1, timerEvent, ())
				self.timerThread.daemon = True
				self.timerThread.start()

				self.pressed()
			else:
				if self.timerThread != None:
					self.timerThread.cancel()
				self.released()

		GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=bouncetime)
		GPIO.add_event_callback(pin, callback)


	def pressed(self):
		print "pressed"
	def pressedLong(self):
		print "pressed long"
	def released(self):
		print "released"

