#!/usr/bin/env python

import sys
import soundfile as sf
import os
import json
from utils.analysis import AbsMovingAvg, Derivative

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
derivSml = Derivative(2)
derivLrg = Derivative(10)

avgSmlValues = []
avgLrgValues = []
derivSmlValues = []
derivLrgValues = []

def proc(d):
    avgSml.add(d)
    avgLrg.add(d)
    

    avgSmlValues.append(avgSml.value())
    avgLrgValues.append(avgLrg.value())
    derivSml.add(avgSml.value() * 20)
    derivLrg.add(avgLrg.value() * 200)

    derivSmlValues.append(derivSml.value())
    derivLrgValues.append(derivLrg.value())

[proc(float(d)) for d in data]

allData["movingAvgSmall"] = avgSmlValues
allData["movingAvgLarge"] = avgLrgValues
allData["derivSmlValues"] = derivSmlValues
allData["derivLrgValues"] = derivLrgValues

graphs.write("const data = ");
graphs.write(json.dumps(allData))
graphs.write(";");
graphs.close() 



