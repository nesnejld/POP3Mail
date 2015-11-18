#!/usr/bin/python
import os
import sys
import base64
import json
import poplib
import csv
def deletefrom(fromname) :
#    fromname="CampusTech - Academic Deals"
    filename="messages.json"
    deletefile=open(filename,"r")
    a= json.load(deletefile)
    kk = {}
    for k in a.keys() :
        if not kk.has_key(len(a[k])) :
            kk[len(a[k])]=[]
        kk[len(a[k])].append(k)
    total=0
    for k in  kk.keys():
        total+=k*len(kk[k])
    aaa=[] 
    for f in fromname:
        aaa.extend(a[f])
    a=aaa
    aa={}
    for aaa in a:
        aa[aaa["message-id"]]=aaa
    mail=poplib.POP3('incoming.verizon.net')
    mail.user('vze2bxny')
    mail.pass_('joh97car')
    lll=mail.list()
    for ll in lll[1]:
        which=int(ll.split(' ')[0])
        if which % 100 == 0 :
            print which
#        print which
        msg=mail.top(which,0)
        m = []
        for mm in msg[1] :
            if len(mm) == 0 :
                break
            if mm[0] == ' ' :
                m[len(m)-1]=m[len(m)-1]+mm
            else :
                m.append(mm)
        result={'msgnum': which}
        for l in m :           
            tokens=l.split(': ',1)
            if len(tokens) < 2:
                value=""
            else :
                value = tokens[1].rstrip()
            if tokens[0].lower()=="message-id" :
                result["message-id"]=tokens[1]
                break
            if False:
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
                                result['fromname'] = name.rstrip().strip()
                            else:
                                fromuserid=value.rstrip()                            
                            result['fromuserid'] = fromuserid
                        break
        if result.has_key("message-id") and aa.has_key(result["message-id"]) :
            print result["msgnum"]
            mail.dele(result["msgnum"])
            del aa[result["message-id"]]
            print len(aa)
            if len(aa) == 0:
                break
    mail.quit()
    sys.exit(0)
def deletecsv(deletefile) :
    aa={}
    with open(deletefile, 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            aa[row[3]]=row
    mail=poplib.POP3('incoming.verizon.net')
    mail.user('vze2bxny')
    mail.pass_('joh97car')
    lll=mail.list()
    for ll in lll[1]:
        which=int(ll.split(' ')[0])
        if which % 100 == 0 :
            print 'Processing: '+str(which)
#        print which
        if True:
            uidl=mail.uidl(which).split(' ')[2]
            if aa.has_key(uidl) :
                print 'Deleting: '+str(which)+' '+uidl
                mail.dele(which)
                del aa[uidl]
                print len(aa)
                if len(aa) == 0:
                    break
        else :
            msg=mail.top(which,0)
            m = []
            for mm in msg[1] :
                if len(mm) == 0 :
                    break
                if mm[0] == ' ' :
                    m[len(m)-1]=m[len(m)-1]+mm
                else :
                    m.append(mm)
            result={'msgnum': which}
            for l in m :           
                tokens=l.split(': ',1)
                if len(tokens) < 2:
                    value=""
                else :
                    value = tokens[1].rstrip()
                if tokens[0].lower()=="message-id" :
                    result["message-id"]=tokens[1]
                    break
            if result.has_key("message-id") and aa.has_key(result["message-id"]) :
                print result["msgnum"]
                mail.dele(result["msgnum"])
                del aa[result["message-id"]]
                print len(aa)
                if len(aa) == 0:
                    break
    mail.quit()
    sys.exit(0)

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
        uidl = line.split(' ')[1]
        result["uidl"]=uidl
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
                            result['fromname'] = name.rstrip().strip()
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
if __name__=='__main__':
    print sys.argv
    i=0
    df = []
    csvfilename=None
    jsonfilename=None
    while (i < len(sys.argv)) :
        if sys.argv[i] == '-df' :
            i+=1
            df.append(sys.argv[i])
        if sys.argv[i] == '-d' :
            i+=1
            deletecsv(sys.argv[i])
            sys.exit(0)
        if sys.argv[i] == '--csv' :
            i+=1
            csvfilename=sys.argv[i]
        if sys.argv[i] == '--json' :
            i+=1
            jsonfilename=sys.argv[i]
        i+=1
    if len(df) :
        deletefrom(df)
        sys.exit(0)
    if True :
        f=open('messages.out','r')
        for i in range(0,55):
            line = f.readline().rstrip()
            if line.startswith('TOP ') :
                break
        #    print line
        aline = [line]
        jsonobject={}
        if csvfilename:
            csvfile=open(csvfilename,"w")
        while True:
            lines = readmessage(f,aline)
            if type(lines) == str:
                break
            if lines.has_key("fromname") :
                if csvfilename :
                    csvfile.write('"'+lines["fromname"]+'","'+lines["fromuserid"]+'",'+str(lines["msgnum"])+',"'+lines["uidl"]+'","'+lines["message-id"]+'"\n')
                if not jsonobject.has_key(lines["fromname"]):
                    jsonobject[lines["fromname"]]=[]
                jsonobject[lines["fromname"]].append(lines)
        #    print lines
                pass
        if csvfilename:
            csvfile.close()
        if jsonfilename:
            jsonfile=open(jsonfilename,"w");
            json.dump(jsonobject,jsonfile,indent=1)
            jsonfile.close()
            jsonfile=open(jsonfilename,"r")
            jsonobject=json.load(jsonfile)
            jsonfile.close()
