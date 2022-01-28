import os
import hashlib

#check virus pattern
def SearchVDB(vdb, fmd5):
    for t in vdb:
        if t[0] == fmd5: #same md5 hash?
            return True, t[1] #return virus pattern

    return False, "" #no virus

def ScanMD5(vdb, vsize, fname):
    ret = False
    vname = ""
    
    size = os.path.getsize(fname)
    if vsize.count(size):
        fp = open(fname, 'rb')
        buf = fp.read()
        fp.close()
        
        m = hashlib.md5()
        m.update(buf)
        fmd5 = m.hexdigest()
        
        ret, vname = SearchVDB(vdb, fmd5)
    
    return ret, vname
    
def ScanStr(fp, offset, mal_str):
    size = len(mal_str)
    
    fp.seek(offset)
    buf = fp.read(size)
    
    if buf == mal_str:
        return True
    else:
        return False
        
def ScanVirus(vdb, vsize, sdb, fname):
    #ScanMD5
    ret, vname = ScanMD5(vdb, vsize, fname)
    if ret == True:
        return ret, vname
    
    #ScanStr
    fp = open(fname, 'rb')
    for t in sdb:
        if ScanStr(fp, t[0], t[1]) == True:
            ret = True
            vname = t[2]
            break
    fp.close()
    
    return ret, vname
    