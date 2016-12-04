#!/usr/bin/python
import RPi.GPIO as GPIO
import time

class Footswitch(object):
    debug = 0

    def pressed(self):
        if Footswitch.debug:
            print "pressed"
    def released(self,duration): 
        if Footswitch.debug:
            print "released", duration

    def __init__(self,pin,statusModePressed, bouncetime):
        self.pin = pin
        self.status = 1
        self.statusModePressed = statusModePressed # 0 on a PullUp circuit, 1 on a PullDown circuit
        self.lastPressed = 0.0

        def callback(channel):
            tm = time.time()
            time.sleep(0.005)
            gpiostatus = GPIO.input(pin)
            if gpiostatus == self.status:
                return
            self.status = 1 - self.status

            if Footswitch.debug:
                print self.status
            if self.status == self.statusModePressed:
                self.lastPressed = tm

                self.pressed()
            else:
                duration = tm - self.lastPressed
                self.lastPressed = tm
                self.released(duration)

        GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=bouncetime)
        GPIO.add_event_callback(pin, callback)


