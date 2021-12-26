import os
import hashlib

class KavMain:
    def init(self, plug_path):
        return 0
    
    def uninit(self):
        return 0
        
    def scan(self, filehandle, filename):
        try:
            mm = filehandle #filehandle is not fp. it is mmap.
            
            size = os.path.getsize(filename)
            if size == 68:
                m = hashlib.md5()
                m.update(mm[:68])
                fmd5 = m.hexdigest()
                
                if fmd5 == '44d88612fea8a8f36de82e1278abb02f':
                    return True, 'EICAR-Test-File (not a virus)'
        except IOError:
            pass
        
        return False,'',-1
            
    def disinfect(self, filename, malware_id):
        vlist = list()
        vlist.append('EICAR-Test-File (not a virus)')
        
        return vlist
        
    def getinfo(self):
        info = dict()
        
        info['author'] = 'ocxh'
        info['version'] = '1.0'
        info['title'] = 'EICAR Scan Engine'
        info['kmd_name'] = 'eicar'
        
        return info