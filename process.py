#!/usr/bin/python
import os
def readmessage(f,aline) :
    lines = [] 
    line = aline[0]
    result = {}
    if line.startswith('TOP ') :
        msgnum = int(line.split(' ')[1])
        result["msgnum"]=msgnum
        while True:
            line = f.readline().rstrip()
            if line.startswith('TOP ') :
                break
            lines.append(line)
            if line.lower().startswith("subject: ") :
                result["subject"] = line[len("subject: "):]
            if line.lower().startswith("date: ") :
                result["date"] = line[len("date: "):]
            if line.lower().startswith("from: ") :
                result["from"] = line[len("from: "):]
            if line.lower().startswith("reply-to: ") :
                result["reply-to"] = line[len("reply-to: "):]
    aline[0]=line
    result["lines"]=lines
    return result
f=open('messages.out','r')
for i in range(0,55):
    line = f.readline().rstrip()
    if line.startswith('TOP ') :
        break
    print line
aline = [line]
while True:
    lines = readmessage(f,aline)
    print lines
