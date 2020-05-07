#!/usr/bin/env python

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
from mediautils.mididevices import UsbMidiDevices, MidiOut
from mediautils.audiodevices import UsbAudioDevices

checkImport("compositionutils")
from compositionutils.scale import Scale, Modes

tonic = sys.argv[1] if len(sys.argv) > 1 else "C"
mode = sys.argv[2] if len(sys.argv) > 2 else "aeolian"
print(tonic, mode)

noteSpan = 15
scale = Scale(noteSpan, tonic, Modes.named(mode))


class Consumer():
    def __init__(self, midiOut, register):
        self.midiOut = midiOut
        self.note = 0
        self.register = register

    def on(self, velocity):
        self.note = scale.noteFrom(int(velocity * 100) % noteSpan) + (12 * self.register)
        self.midiOut.note_on(self.note, int(26 + (velocity * 100)), 0)

    def off(self):
        self.midiOut.note_off(self.note, 0, 0)


import time
import sounddevice as sd
def audioCapture(deviceIdx, channels, shouldStop, callback):
    print("starting audio capture")
    with sd.InputStream(samplerate=44100.0, device=deviceIdx, channels=channels, callback=callback, blocksize=44) as stream:
        stream.start()
        while not shouldStop.is_set():
            time.sleep(1)


midiDevices = UsbMidiDevices()
midiOut = MidiOut(midiDevices)

audioDevices = UsbAudioDevices()
aidx = [k for k in audioDevices.keys()][0]
audioDevice = audioDevices[aidx]
print("using", audioDevice)
channelCount = audioDevice[1]

import threading
shouldStop = threading.Event()


consumerTop = Consumer(midiOut.io, 1)
consumerBass = Consumer(midiOut.io, -1)
chaserTop = Chaser(consumerTop, 0.04, 0.0039)
chaserBass = Chaser(consumerBass, 0.04, 0.0039)
chasers = [chaserTop, chaserBass]
cs = range(channelCount)
callback = lambda indata, frames, t, status: [[chasers[i].add(v[i]) for i in cs] for v in indata]


threads = []

threads.append(threading.Thread(target=audioCapture, args=(aidx,channelCount,shouldStop,callback,), daemon=True))
[t.start() for t in threads]

import readchar
print("press 'q' to exit")
while not shouldStop.is_set():
    c = readchar.readchar()
    if c == "q":
        print("stopping...")
        shouldStop.set()
        [t.join() for t in threads]

midiOut.io.write_short(0xb0, 0x7b, 0) # all notes off

del midiOut
del midiDevices
print("done")



        
    


