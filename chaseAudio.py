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
    def __init__(self, midiOut):
        self.midiOut = midiOut
        self.note = 0

    def on(self, velocity):
        self.note = scale.noteFrom(int(velocity * 100) % noteSpan)
        self.midiOut.note_on(self.note, int(26 + (velocity * 100)), 0)

    def off(self):
        self.midiOut.note_off(self.note, 0, 0)


import time
import sounddevice as sd
def audioCapture(device, shouldStop, callback):
    print("starting audio capture")
    with sd.InputStream(samplerate=44100.0, device=device, channels=1, callback=callback, blocksize=44) as stream:
        stream.start()
        while not shouldStop.is_set():
            time.sleep(1)


midiDevices = UsbMidiDevices()
midiOut = MidiOut(midiDevices)
consumer = Consumer(midiOut.io)
chaser = Chaser(consumer, 0.04, 0.0039)
callback = lambda indata, frames, t, status: [chaser.add(v[0]) for v in indata]

devices = UsbAudioDevices()
audioDevice = [k for k in devices.keys()][0]
print("using %s" % devices[audioDevice])

import readchar
import threading

shouldStop = threading.Event()
thread = threading.Thread(target=audioCapture, args=(audioDevice,shouldStop,callback,), daemon=True)
thread.start()

print("press 'q' to exit")
while not shouldStop.is_set():
    c = readchar.readchar()
    if c == "q":
        print("stopping...")
        shouldStop.set()
        thread.join()

midiOut.io.write_short(0xB0, 0x7B, 0)

del midiOut
del midiDevices
print("done")



        
    


