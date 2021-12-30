import hashlib
import os
import sys
import zlib
import StringIO

#virus.db file -> VirusDB[](LoadVirusDB)
VirusDB = []
#VirusDB -> vdb, vsize(MakeVirusDB)
vdb = []
vsize = []

def DecodeKMD(fname):
    try:
        fp = open(fname, 'rb')
        buf = fp.read()
        fp.close()
        
        buf2 = buf[:-32] #encrypt msg
        fmd5 = buf[-32:] #md5 hash
        
        f=buf2
        for i in range(3):
            md5 = hashlib.md5()
            md5.update(f)
            f = md5.hexdigest()
        if f != fmd5: #fname's md5 != origin md5?
            raise SystemError
        
        buf3 = ''
        for c in buf2[4:]: #0xFF XOR
            buf3 += chr(ord(c) ^ 0xFF)
        
        buf4 = zlib.decompress(buf3) #decompress
        return buf4
    except:
        pass

def LoadVirusDB():
    buf = DecodeKMD('virus.kmd') #decrypt
    fp = StringIO.StringIO(buf) 
    
    while True:
        line = fp.readline()
        if not line: break
        
        line = line.strip()
        VirusDB.append(line)
    fp.close()
    
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
    LoadVirusDB()
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