import os
import hashlib
import sys
import zlib 
import StringIO
import scanmod

eicar = 'C:/Users/gksru/Documents/programming/anti-virus/eicar.txt'
dummy = 'C:/Users/gksru/Documents/programming/anti-virus/Dummy.txt'


VirusDB = []
vdb=[]
vsize=[]

def DecodeKMD(fname):
    try:
        fp = open(fname, 'rb')
        buf = fp.read()
        fp.close()
        
        buf2 = buf[:-32]
        fmd5 = buf[-32:]
        
        f = buf2
        for i in range(3):
            md5 = hashlib.md5()
            md5.update(f)
            f = md5.hexdigest()
        
        if f != fmd5:
            raise SystemError
        
        buf3 = ''
        for c in buf2[4:]:
            buf3 += chr(ord(c) ^ 0xFF)
        buf4 = zlib.decompress(buf3)
        return buf4
    except:
        pass
    
    return None

def LoadVirusDB():
    buf = DecodeKMD('virus.kmd')
    fp=StringIO.StringIO(buf)
    
    while True:
        line = fp.readline()
        if not line: break
        
        line = line.strip()
        VirusDB.append(line)
        
    fp.close()

def MakeVirusDB():
    for pattern in VirusDB:
        t=[]
        v = pattern.split(':')
        t.append(v[1])
        t.append(v[2])
        vdb.append(t)
        
        size = int(v[0])
        if vsize.count(size) == 0:
            vsize.append(size)
        
        
if __name__=='__main__':
    LoadVirusDB()
    MakeVirusDB()
    
    if len(sys.argv) != 2:
        print 'Usage : main.py [file]'
        exit(0)
        
    fname = sys.argv[1]
    ret, vname = scanmod.ScanMD5(vdb, vsize, fname)
    if ret == True:
        print '%s : %s' %(fname, vname)
    else:
        print '%s : ok' %(fname)
else:
    print '%s : ok' %(fname)