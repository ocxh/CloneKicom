import os
import sys
sys.path.append('/Users/ocx/programming/engine/kavcore')
import k2kmdfile

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage : kmake.py [python source]'
        exit()
        
    k2kmdfile.make(sys.argv[1], True)