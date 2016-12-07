#!/usr/bin/python

import time
import threading

class Playback(threading.Thread): 
 
    debug = False 
 
    def __init__(self, recordings,gap): 
        threading.Thread.__init__(self) 
        self.gap = gap
        self.stopped = False
        self.recordings = self.harmonize(recordings)
        if Playback.debug:
            print("init playbackThread")

    def harmonize(self, recordings):
        eps = 0.05
        harmonized = list(recordings)
        total = sum(recordings)
        for i in range(len(harmonized)):
            f = harmonized[i]

            best = total/4.0
            if abs(best-f) < eps:
                harmonized[i] = best
                print recordings[i], harmonized[i], recordings[i] - harmonized[i], "1/4"
                continue

            best = total/8.0
            if abs(best-f) < eps:
                harmonized[i] = best
                print recordings[i], harmonized[i], recordings[i] - harmonized[i], "1/8"
                continue

            best = total/12.0
            if abs(best-f) < eps:
                harmonized[i] = best
                print recordings[i], harmonized[i], recordings[i] - harmonized[i], "1/12"
                continue

            best = total/16.0
            if abs(best-f) < eps:
                harmonized[i] = best
                print recordings[i], harmonized[i], recordings[i] - harmonized[i], "1/16"
                continue

        return harmonized

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
