#!/usr/bin/python

import time
import threading

class Playback(threading.Thread): 
 
    debug = False 
 
    def __init__(self, recordings,gap): 
        threading.Thread.__init__(self) 
        self.gap = gap
        self.stopped = False
        self.recordings = list(recordings) # copy list
        if Playback.debug:
            print("init playbackThread")

    def run(self): 
        if Playback.debug:
            print "playback start", self.recordings 
        time.sleep(max(0,self.recordings[0]-self.gap)) # close gap
        i=1
        while True:
            if i == len(self.recordings):
                i = 0
            if self.stopped:
                if Playback.debug:
                    print("playback stopped")
                return

            if Playback.debug:
                print("playback ",i)
            h = self.recordings[i]
            t1 = time.time()
            self.play(h)
            t2 = time.time()
            rest = h - (t2-t1)
            if rest > 0:
                time.sleep(h - (t2-t1))
            i = i+1
        if Playback.debug:
            print("playback finished")
        self.stopped = True

    def stop(self): 
        self.stopped = True

    def play(self,duration): 
        if Playback.debug:
            print duration
