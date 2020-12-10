#!/usr/bin/python
import json
import sys

with open(sys.argv[1], "r") as input_file:
	data = json.load(input_file)

res = ""
resAlt = ""
prevTime = None
for packet in data:
	currTime = float(packet["_source"]["layers"]["frame"]["frame.time_relative"])
	if prevTime != None:
		if abs(currTime - prevTime) >= 2:
			res += "1"
			resAlt += "0"
		else:
			res += "0"
			resAlt += "1"
	prevTime = currTime

# Last bit (could be 0 or 1)
res += "1"

# Split in chunks of 8 bits and print in ASCII
chunks = [ res[i:i+8] for i in range(0, len(res), 8) ]
print( "".join(chr(int(b, 2)) for b in chunks) )




