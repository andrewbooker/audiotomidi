#!/usr/bin/env python

import sys
import soundfile as sf
import os
import json

infile = sys.argv[1]
workingDir = os.path.dirname(infile)
print("loading %s" % infile)
(data, sampleRate) = sf.read(infile, dtype="float32")

print("%d samples found" % len(data))

graphs = open("examplewave/data.js", "w")

allData = {}
allData["original"] = [float(d) for d in data]

graphs.write("const data = ");
graphs.write(json.dumps(allData))
graphs.write(";");
graphs.close() 



