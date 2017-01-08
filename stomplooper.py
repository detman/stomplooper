#!/usr/bin/python

import RPi.GPIO as GPIO
import time, sys
import threading
import subprocess

from neopixel import *

from playback import Playback
from recorder import Recorder
from footswitch import Footswitch
from wheeler import Wheeler

switch = 19
yellowLED = 21
redLED = 23

audiofile = None

RESET_DURATION = 2.0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch, GPIO.IN)

GPIO.setup(redLED, GPIO.OUT)
GPIO.output(redLED, 0)

GPIO.setup(yellowLED, GPIO.OUT)
GPIO.output(yellowLED, 0)

def playAudio():
    global audiofile
    pass
    if audiofile != None:
        #subprocess.Popen(["mpg123", "-q", audiofile])    
        subprocess.Popen(["aplay", "-q", audiofile])    

Playback.debug = 0
class LEDBlinker(Playback):

    def play(self,duration):
        playAudio()
        wheeler = Wheeler(duration,strip)
        wheeler.start()
        ledDuration = 0.1 if duration > 0.2 else duration/2
        GPIO.output(redLED, 1)
       # self.show(Color(255,0,0))
        time.sleep( ledDuration )
        GPIO.output(redLED, 0)
       # self.show(Color(0,0,0))
        
    def show(self, color):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()

class MyButton(Footswitch):

    debug = True
    def __init__(self,pin,statusModePressed, bouncetime, timer_timeout):
        Footswitch.__init__(self,pin,statusModePressed, bouncetime )
        self.recorder = Recorder()
        self.playback = None

        self.lastPressed = 0
        self.acceptRelease = False
        self.timerThread = None
        self.timer_timeout = timer_timeout

    def pressed(self):
        if MyButton.debug: 
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
        if MyButton.debug: 
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
                if MyButton.debug: 
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
            if MyButton.debug: 
                print "start PB by timer", timeout
            self.startPlayback(timeout)

        self.timerThread = threading.Timer(self.timer_timeout, timerEvent, ())
        self.timerThread.daemon = True
        self.timerThread.start()

    def stopTimer(self):
        if self.timerThread != None:
             self.timerThread.cancel()


LED_COUNT      = 12      # Number of LED pixels.
LED_CHANNEL    = 1       # PWM Channel (set to 1 when LED_PIN is 13 or 19, else 0)
LED_PIN        = 13      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

## main

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

bttn = MyButton(switch,0, 2, 1.0)

if len(sys.argv) > 1:
    audiofile = sys.argv[1]

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()
    sys.exit()

