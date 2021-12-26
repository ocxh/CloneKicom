import k2rsa
import k2kmdfile


pu = k2rsa.read_key('key.pkr')
k = k2kmdfile.KMD('dummy.kmd', pu)

module = k2kmdfile.load('dummy', k.body)
print dir(module)
