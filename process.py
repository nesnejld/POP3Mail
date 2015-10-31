#!/usr/bin/python
import os
import base64
def readmessage(f,aline) :
    lines = [] 
    line = aline[0]
    result = {}
    result["message-id"]='<noid>'
    if line.startswith('TOP ') :
        msgnum = int(line.split(' ')[1])
        result["msgnum"]=msgnum
        line = f.readline().rstrip() # +OK
        line = f.readline().rstrip()
        line = f.readline().rstrip()
        while True:
            l=line
            while True:
                line = f.readline().rstrip()
                if len(line.strip())==0:
                    break
                if line[0]!=' ':
                    break
                l+=line
            lines.append(l)
            tokens=l.split(': ',1)
            if len(tokens) < 2:
                value=""
            else :
                value = tokens[1].rstrip()
            for tag in ['subject','date','from','to','message-id'] :
                if tokens[0].lower() == tag :
                    result[tag] = value
                    if tag=='from' :
                        if value.find('<') > 0:
                            name = value[0:value.find('<')].rstrip()
                            fromuserid = value[value.find('<')+1:len(value)-1]
                            if name[0]=='"' or name=="'":
                                name = name[1:len(name)-1]
                            for locale in [ 'utf-8', 'ISO-8859-15', 'ISO-8859-1'] :
                                if name.lower().find(('=?'+locale).lower()) ==0 :
                                    name=name[len('=?'+locale):]
                                    if name.find('?B?') == 0:
                                        name=name[3:name.find('?=',3)]
                                        try :
                                            name=base64.b64decode(name)
                                            while True:
                                                try:
                                                    name=name.decode(locale).encode('utf-8')
                                                    break;
                                                except UnicodeDecodeError as e:
                                                    name=name[0:e.start]+name[e.end:]
                                        except :
                                            name='Error:'+name
                                    elif name.find('?Q?') == 0:
                                        name=name[3:name.find('?=',3)]
                            result['fromname'] = name.rstrip()
                        else:
                            fromuserid=value.rstrip()                            
                        result['fromuserid'] = fromuserid
                    break
            if len(line.strip())==0:
                line=f.readline().rstrip()
                break
            if line.startswith('TOP ') :
                break
    else :
        return line 
    aline[0]=line
#    result["lines"]=lines
    return result
f=open('messages.out','r')
for i in range(0,55):
    line = f.readline().rstrip()
    if line.startswith('TOP ') :
        break
#    print line
aline = [line]
while True:
    lines = readmessage(f,aline)
    if type(lines) == str:
        break
    if lines.has_key("fromname") :
        print '"'+lines["fromname"]+'", "'+lines["fromuserid"]+'", '+str(lines["msgnum"])+', "'+lines["message-id"]+'"'
#    print lines
        pass
