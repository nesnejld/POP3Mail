#!/usr/bin/python
import json
import os
import glob
subjects={}
_from={}
for f in glob.glob("../json/*.json") :
    j=json.load(open(f,"r"))
    if len(j["tolist"]) > 3:
        print f+" "+json.dumps(j["tolist"]) 
    if not subjects.has_key(j["subject"]) :
        subjects[j["subject"]]=[]
    subjects[j["subject"]].append(j["id"])
    if not _from.has_key(j["fromlist"][0]) :
        _from[j["fromlist"][0]]=[]
    _from[j["fromlist"][0]].append(j["id"])
keys = subjects.keys()
keys.sort()
f=open("subjects.lst",'w')
for k in keys:
    s=""
    try:
        s+=str(k)+"\n"
        for i in subjects[k] :
            s+=str(i)+" "
        s+='\n'
        f.write(s)           
    except:
        pass
f.close()
f=open("from.lst",'w')
keys = _from.keys()
keys.sort()
for k in keys:
    s=""
    try:
        s+=str(k)+"\n"
        for i in _from[k] :
            s+=str(i)+" "
        s+='\n'
        f.write(s)           
    except:
        pass
f.close()
