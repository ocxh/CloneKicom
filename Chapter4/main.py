import hashlib
import os

fp = open('eicar.txt', 'rb')
fbuf = fp.read()
fp.close()

m = hashlib.md5()
m.update(fbuf)
fmd5 = m.hexdigest()

print("\n")
if fmd5 == "44d88612fea8a8f36de82e1278abb02f":
    print "eicar virus!"
    #os.remove('eicar.txt')
else:
    print "No eicar Virus"