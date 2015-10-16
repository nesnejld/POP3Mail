#!/usr/bin/python
import json
import os
import glob
subjects={}
for f in glob.glob("*.json") :
    j=json.load(open(f,"r"))
    if len(j["tolist"]) > 3:
        print f+" "+json.dumps(j["tolist"]) 
    if not subjects.has_key(j["subject"]) :
        subjects[j["subject"]]=[]
    subjects[j["subject"]].append(j["id"])
keys = subjects.keys()
keys.sort()
for k in keys:
    try:
        print k,
        for i in subjects[k] :
            print i,
        print
    except:
        pass
