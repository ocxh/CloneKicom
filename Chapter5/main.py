import hashlib
import os
import sys

VirusDB = [
"68:44d88612fea8a8f36de82e1278abb02f:EICAR Test", 
"22:731dd45ee12ce31d6f5f44b9d88ccde0:Dummy Test"
]

#VirusDB -> vdb
vdb = []
vsize = []
def MakeVirusDB():
    for pattern in VirusDB:
        t = []
        v = pattern.split(':')
        t.append(v[1])
        t.append(v[2])
        vdb.append(t)
        
        size = int(v[0])
        if vsize.count(size) == 0: #already exist?
            vsize.append(size)

#check virus pattern
def SearchVDB(fmd5):
    for t in vdb:
        if t[0] == fmd5: #same md5 hash?
            return True, t[1] #return virus pattern

    return False, "" #no virus

if __name__=='__main__':
    MakeVirusDB()
    
    #use command line
    if len(sys.argv) !=2:
        print "Usage : main.py [file]"
    
    fname = sys.argv[1] #[virus file]
    
    size = os.path.getsize(fname)
    if vsize.count(size):
        fp = open(fname, 'rb')
        buf = fp.read()
        fp.close()
        
        m = hashlib.md5()
        m.update(buf)
        fmd5 = m.hexdigest()
        
        #check virus pattern
        ret, vname = SearchVDB(fmd5)
        if ret:
            print "%s : %s" %(fname, vname) #"filename : virusName"
            #os.remove(fname)
        else:
            print "%s : not Virus" %(fname)
    else:
        print "%s : not Virus" %(fname)