import os
import sys
import hashlib

fp = open(sys.argv[1],'rb')
buffer=fp.read()
fp.close()

md5 = hashlib.md5()
md5.update(buffer)
fmd5 = md5.hexdigest()

print(fmd5)