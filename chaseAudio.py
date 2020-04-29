#!/usr/bin/env python

import os
import sys
def checkImport(lib):
    parentDir = os.path.dirname(os.getcwd())
    sys.path.append(parentDir)
    if not os.path.exists(os.path.join(parentDir, lib)):
        print("%s library not found." % lib)
        print("please clone github.com/andrewbooker/%s.git into %s" % (lib, parentDir))
        exit()

checkImport("mediautils")
from mediautils.usbdevices import UsbMidiDevices, MidiOut
checkImport("compositionutils")
from compositionutils.scale import Scale, Modes

tonic = sys.argv[1] if len(sys.argv) > 1 else "C"
mode = sys.argv[2] if len(sys.argv) > 2 else "aeolian"

noteSpan = 15
scale = Scale(noteSpan, tonic, Modes.named(mode))

print(tonic, mode)

class Consumer():
    def __init__(self, midiOut):
        self.midiOut = midiOut
        self.note = 0

    def on(self, velocity):
        self.note = scale.noteFrom(int(velocity * 10000) % noteSpan)
        self.midiOut.note_on(self.note, int(26 + (velocity * 100)), 0)

    def off(self):
        self.midiOut.note_off(self.note, 0, 0)
        
from utils.analysis import AbsMovingAvg, Threshold
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
            self.consumer.on(self.thrOn.overshoot())
            self.state = 1
        elif self.thrOff.value() == 0 and self.state == 1:
            self.state = 0
            self.consumer.off()

    def callback(self):
        return lambda indata, frames, t, status: [self._add(v[0]) for v in indata]
    
import time
import sounddevice as sd
def audioCapture(device, shouldStop):
    print("starting audio capture on %s" % device)
    with sd.InputStream(samplerate=44100.0, device=device, channels=1, callback=chaser.callback(), blocksize=44) as stream:
        stream.start()
        while not shouldStop.is_set():
            time.sleep(1)
    

midiDevices = UsbMidiDevices()
midiOut = MidiOut(midiDevices)
consumer = Consumer(midiOut.io)
chaser = Chaser(consumer)

import readchar
import threading

shouldStop = threading.Event()
thread = threading.Thread(target=audioCapture, args=(7,shouldStop,), daemon=True)
thread.start()

print("press 'q' to exit")
while not shouldStop.is_set():
    c = readchar.readchar()
    if c == "q":
        print("stopping...")
        shouldStop.set()
        thread.join()

del midiOut
del midiDevices
print("done")



        
    


