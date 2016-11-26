#!/usr/bin/python

import time
import threading

class Playback(threading.Thread): 
 
    debug = 0 
 
    def __init__(self, recordings): 
        threading.Thread.__init__(self) 
        self.stopped = False
        self.recordings = recordings
        if Playback.debug:
            print("init playbackThread")

    def run(self): 
        if Playback.debug:
            print "playback start", self.recordings 
        i=0
        while True:
            if self.stopped:
                if Playback.debug:
                    print("playback stopped")
                return
            h = self.recordings[i]
            t1 = time.time()
            self.play(h)
            t2 = time.time()
            rest = h - (t2-t1)
            if rest > 0:
                time.sleep(h - (t2-t1))
            i = i+1
            if i == len(self.recordings):
                i = 0
        if Playback.debug:
            print("playback finished")
        self.stopped = True

    def stop(self): 
        self.stopped = True

    def play(self,duration): 
        if Playback.debug:
            print duration
