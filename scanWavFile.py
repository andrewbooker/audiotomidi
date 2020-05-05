#!/usr/bin/env python

from utils.analysis import AbsMovingAvg, Threshold, Derivative
from utils.chaser import Chaser

import os
import sys
parentDir = os.path.dirname(os.getcwd())
sys.path.append(parentDir)
def checkImport(lib):
    if not os.path.exists(os.path.join(parentDir, lib)):
        print("%s library not found." % lib)
        print("please clone github.com/andrewbooker/%s.git into %s" % (lib, parentDir))
        exit()

checkImport("mediautils")
from mediautils.usbdevices import UsbMidiDevices, MidiOut


## ===== composer =====

checkImport("compositionutils")
from compositionutils.scale import Scale, Modes

tonic = "C"
mode = "aeolian"
print(tonic, mode)

noteSpan = 15
scale = Scale(noteSpan, tonic, Modes.named(mode))


class Consumer():
    def __init__(self, midiOut):
        self.midiOut = midiOut
        self.note = 0

    def on(self, velocity):
        self.note = scale.noteFrom(int(velocity * 100) % noteSpan)
        self.midiOut.note_on(self.note, int(26 + (velocity * 100)), 0)

    def off(self):
        self.midiOut.note_off(self.note, 0, 0)

## =====




midiDevices = UsbMidiDevices()
midiOut = MidiOut(midiDevices)
consumer = Consumer(midiOut.io)
chaser = Chaser(consumer, 0.6, 0.2)


import soundfile as sf

infile = sys.argv[1]
workingDir = os.path.dirname(infile)
print("loading %s" % infile)
(data, sampleRate) = sf.read(infile, dtype="float32")


for s in range(len(data)):
    chaser.add(data[s])


del midiOut
del midiDevices
print("done")
    
