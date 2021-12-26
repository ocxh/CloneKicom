import kavcore.k2engine

def listvirus_callback(plugin_name, vnames):
    for vname in vnames:
        print '%-50s [%s.kmd]' %(vname, plugin_name)

k2 = kavcore.k2engine.Engine(debug=True)
if k2.set_plugins('plugins'):
    kav = k2.create_instance()
    if kav:
        print '[*] Success : create_instance'

        ret = kav.init()
        info = kav.getinfo()

        vlist = kav.listvirus(listvirus_callback)

        print '[*] Used Callback    : %d' %len(vlist)

        vlist = kav.listvirus()
        print '[*] Not used Callback : %d' % len(vlist)

        ret, vname, mid, eid = kav.scan('./plugins/eicar.txt')
        if ret:
            kav.disinfect('./plugins/eicar.txt', mid, eid)

        kav.uninit()
        