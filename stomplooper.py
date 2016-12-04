#!/usr/bin/python

import RPi.GPIO as GPIO
import time, sys
import threading
import subprocess

from playback import Playback
from recorder import Recorder
from footswitch import Footswitch

switch = 19
yellowLED = 21
redLED = 23

RESET_DURATION = 2.0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch, GPIO.IN)

GPIO.setup(redLED, GPIO.OUT)
GPIO.output(redLED, 0)

GPIO.setup(yellowLED, GPIO.OUT)
GPIO.output(yellowLED, 0)

def playAudio():
#    subprocess.Popen(["mpg123", "-q", "beat2.mp3"])    
    pass

Playback.debug = 0
class LEDBlinker(Playback):

    def play(self,duration):
        playAudio()
        ledDuration = 0.1 if duration > 0.2 else duration/2
        GPIO.output(redLED, 1)
        time.sleep( ledDuration )
        GPIO.output(redLED, 0)
        
class MyButton(Footswitch):

    def __init__(self,pin,statusModePressed, bouncetime, timer_timeout):
        Footswitch.__init__(self,pin,statusModePressed, bouncetime )
        self.recorder = Recorder()
        self.playback = None

        self.lastPressed = 0
        self.acceptRelease = False
        self.timerThread = None
        self.timer_timeout = timer_timeout

    def pressed(self):
        print "pressed"
        GPIO.output(redLED, 1)
        playAudio()
        if self.playback != None:
            if self.playback.is_alive():
                self.playback.stop()
                GPIO.output(yellowLED,0)
                self.recorder = Recorder() # create new recorder; drop old recording
            self.playback = None
        self.recorder.record()

        if len(self.recorder.recordings) > 0 and self.timer_timeout > 0.0:
            self.startTimer(self.recorder.recordings[0])

    def released(self,duration):
        print "released", duration
        GPIO.output(redLED, 0)

        self.stopTimer()

        if self.playback != None:
            return

        if len(self.recorder.recordings) > 0:
            # if button was pressed more than 2/3 of the first recorded duration, start the playback
            if duration > 0.66 * self.recorder.recordings[0]:
                print "start PB in by release", duration
                self.startPlayback(duration)
        else:
            if duration > RESET_DURATION:
                print "reset"
                self.recorder = Recorder() # reset

    def startPlayback(self, gap):
        if self.playback != None:
            return
        self.playback = LEDBlinker(self.recorder.recordings,gap)
        self.playback.start()
        GPIO.output(yellowLED,1)
        self.recorder = Recorder() # create new recorder; drop old recording and status

    def startTimer(self,timeout):
        def timerEvent():
            self.acceptRelease = False
            print "start PB by timer", timeout
            self.startPlayback(timeout)

        self.timerThread = threading.Timer(self.timer_timeout, timerEvent, ())
        self.timerThread.daemon = True
        self.timerThread.start()

    def stopTimer(self):
        if self.timerThread != None:
             self.timerThread.cancel()


## main

bttn = MyButton(switch,0, 2, 1.0)

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()

