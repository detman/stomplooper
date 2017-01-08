#!/usr/bin/python

import time
import threading
from neopixel import *

class Wheeler(threading.Thread): 
 
    debug = False 
 
    def __init__(self, duration, strip): 
        threading.Thread.__init__(self) 
        self.duration = duration
        self.strip = strip
	self.color = Color(255,0,0)
	self.black = Color(0,0,0)
        if Wheeler.debug:
            print("init Wheeler")

    def run(self): 
        if Wheeler.debug:
            print "playback start", self.duration 
        for i in range(12):
            self.strip.setPixelColor(i, self.black)

        for i in range(12):
            if i > 0:
                self.strip.setPixelColor(i-1, self.black)
            self.strip.setPixelColor(i, self.color)
            self.strip.show()
            time.sleep(self.duration/12.0) 
        self.strip.setPixelColor(11, self.black)
        self.strip.show()
        if Wheeler.debug:
            print("Wheeler finished")
        self.stopped = True

    def stop(self): 
        self.stopped = True

