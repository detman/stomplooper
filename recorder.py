#!/usr/bin/python

import time

class Recorder(object):

    debug = 0
    def __init__(self): 
        self.recordings = []
        self.lastRecord = 0
        if Recorder.debug:
            print("init Recorder")

    def record(self): 
        now = time.time();
        if self.lastRecord != 0:
            self.recordings.append(now-self.lastRecord)
            if Recorder.debug:
                print(len(self.recordings), " ", self.recordings[-1]);
        self.lastRecord = now

    def empty(self): 
        return len(self.recordings) > 0

    def minInterval(self):
        return 0 if len(self.recording) == 0 else self.recording[0]
