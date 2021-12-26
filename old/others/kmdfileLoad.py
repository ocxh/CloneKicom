import k2rsa
import k2kmdfile

''' kmdfile.py memory loading

pu = k2rsa.read_key('key.pkr')
k = k2kmdfile.KMD('dummy.kmd', pu)

module = k2kmdfile.load('dummy', k.body)
print dir(module)
'''

''' 1. return the function of kmdfile.load 
pu = k2rsa.read_key('key.pkr')
k = k2kmdfile.KMD('dummy.kmd', pu)
module = k2kmdfile.load('dummy', k.body)
kav = module.KavMain()
kav.init('.') #reset plugin engine
print kav.getinfo()
kav.uninit()
'''

''' 2. use imort dummy
pu = k2rsa.read_key('key.pkr')
k = k2kmdfile.KMD('dummy.kmd', pu)
module = k2kmdfile.load('dummy', k.body)
import dummy

kav2 = dummy.KavMain()
kav2.init('.')
print kav2.listvirus()
kav2.uninit()
'''