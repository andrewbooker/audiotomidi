#!/usr/bin/env python

import sys
import soundfile as sf
import os
import json
from utils.analysis import AbsMovingAvg

infile = sys.argv[1]
workingDir = os.path.dirname(infile)
print("loading %s" % infile)
(data, sampleRate) = sf.read(infile, dtype="float32")

print("%d samples found" % len(data))

graphs = open("./examplewave/data.js", "w")

allData = {}
allData["original"] = [float(d) for d in data]

avgSml = AbsMovingAvg(3)
avgLrg = AbsMovingAvg(400)

avgSmlValues = []
avgLrgValues = []

def proc(d):
    avgSml.add(d);
    avgLrg.add(d);

    avgSmlValues.append(avgSml.value())
    avgLrgValues.append(avgLrg.value())

[proc(float(d)) for d in data]

allData["movingAvgSmall"] = avgSmlValues
allData["movingAvgLarge"] = avgLrgValues

graphs.write("const data = ");
graphs.write(json.dumps(allData))
graphs.write(";");
graphs.close() 



