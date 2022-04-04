import sys
import zlib
import hashlib
import os

#encryption
def main():
    if len(sys.argv) != 2:
        print 'Usage : kmake.py [file]'
        return
    #file name
    fname = sys.argv[1]
    tname = fname
    #read file
    fp = open(tname, 'rb')
    buf = fp.read()
    fp.close()
    #zlib compress
    buf2 = zlib.compress(buf)
    # XOR 0xFF
    buf3 = ''
    for c in buf2:
        buf3 += chr(ord(c) ^ 0xFF)
    #ADD KAVM header msg and MD5
    buf4 = 'KAVM' + buf3
    f=buf4
    for i in range(3):
        md5 = hashlib.md5()
        md5.update(f)
        f = md5.hexdigest()
    buf4 += f
    #new file ?.kmd
    kmd_name = fname.split('.')[0] + '.kmd'
    fp = open(kmd_name, 'wb')
    fp.write(buf4)
    fp.close()
    #result msg
    print '%s -> %s' %(fname, kmd_name)

if __name__ == '__main__':
    main()