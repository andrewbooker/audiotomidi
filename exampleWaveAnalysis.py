#!/usr/bin/env python

import sys
import soundfile as sf
import os
import json
from utils.analysis import *

infile = sys.argv[1]
workingDir = os.path.dirname(infile)
print("loading %s" % infile)
(data, sampleRate) = sf.read(infile, dtype="float32")

print("%d samples found" % len(data))

graphs = open("./examplewave/data.js", "w")

allData = {}
allData["original"] = [float(d) for d in data]

avgSml = AbsMovingAvg(44)
avgLrg = AbsMovingAvg(441)
thr = Threshold(lambda: 0.1)
hyst = SchmittHysteresis(lambda: 0.08, lambda: 0.01)

avgSmlValues = []
avgLrgValues = []
thrValues = []
hystValues = []

def proc(d):
    avgSml.add(d)
    avgLrg.add(d)
    
    thr.add(avgSml.value())
    hyst.add(avgSml.value())

    avgSmlValues.append(avgSml.value())
    avgLrgValues.append(avgLrg.value())
    thrValues.append(thr.value() * 0.2)
    hystValues.append(hyst.value() * 0.25)

[proc(float(d)) for d in data]

#allData["movingAvgSmall"] = avgSmlValues
#allData["movingAvgLarge"] = avgLrgValues
allData["movingAvgSmall->threshold"] = thrValues
allData["movingAvgSmall->SchmittHysteresis"] = hystValues

graphs.write("const data = ");
graphs.write(json.dumps(allData))
graphs.write(";");
graphs.close() 



