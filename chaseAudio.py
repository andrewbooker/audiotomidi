#!/usr/bin/env python

import sounddevice as sd
from utils.analysis import AbsMovingAvg, Threshold


device = 7
import time


class Consumer():
    def on(self):
        print("on")

    def off(self):
        print("off")
        

class Chaser():
    def __init__(self, consumer):
        self.avg = AbsMovingAvg(44)
        self.thrOn = Threshold(lambda: 0.04)
        self.thrOff = Threshold(lambda: 0.001)
        self.state = 0
        self.consumer = consumer
        
    def _add(self, v):
        self.avg.add(v)
        self.thrOn.add(self.avg.value())
        self.thrOff.add(self.avg.value())

        if self.thrOn.value() == 1 and self.state == 0:
            self.consumer.on()
            self.state = 1
        elif self.thrOff.value() == 0 and self.state == 1:
            self.state = 0
            self.consumer.off()

    def callback(self):
        return lambda indata, frames, t, status: [self._add(v[0]) for v in indata]
    
consumer = Consumer()
chaser = Chaser(consumer)


print("starting audio capture on %s" % device)
with sd.InputStream(samplerate=44100.0, device=device, channels=1, callback=chaser.callback(), blocksize=44) as stream:
    time.sleep(1)
    stream.start()
    while True:
        time.sleep(0.1)


