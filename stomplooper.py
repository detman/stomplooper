#!/usr/bin/python

import RPi.GPIO as GPIO
import time, sys
import threading
import subprocess

from playback import Playback
from recorder import Recorder
from momentarybutton import MomentaryButton

redLED = 23
yellowLED = 24
switch = 21

GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch, GPIO.IN)

GPIO.setup(redLED, GPIO.OUT)
GPIO.output(redLED, 0)

GPIO.setup(yellowLED, GPIO.OUT)
GPIO.output(yellowLED, 0)

def playAudio():
    #subprocess.Popen(["mpg123", "beat1.mp3"])    
    pass

class LEDBlinker(Playback):

    def play(self,duration):
        playAudio()
        ledDuration = 0.1 if duration > 0.2 else duration/2
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
        playAudio()
        if self.playback != None:
            if self.playback.is_alive():
                self.playback.stop()
                GPIO.output(yellowLED,0)
                self.recorder = Recorder() # create new recorder; drop old recording
            if self.playback.stopped: # may be finished or stopped
                self.playback = None
        self.recorder.record()
        if 1 == len(self.recorder.recordings):
            self.timer_timeout = self.recorder.recordings[0] # use first delay for timer timeout
		

    def pressedLong(self):
        print "pressed long", len(self.recorder.recordings)
        if len(self.recorder.recordings) > 0:
            self.playback = LEDBlinker(self.recorder.recordings)
            self.playback.start()
            GPIO.output(yellowLED,1)
        self.recorder = Recorder() # create new recorder; drop old recording and status

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

