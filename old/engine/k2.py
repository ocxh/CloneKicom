import sys
import os
from ctypes import windll, Structure, c_short, c_ushort, byref
from optparse import OptionParser
import kavcore.k2engine

KAV_VERSION = '0.27'
KAV_BUILDDATE = 'Oct 30 2017'
KAV_LASTYEAR = KAV_BUILDDATE[len(KAV_BUILDDATE)-4:]

FOREGROUND_BLACK = 0x0000
FOREGROUND_BLUE = 0x0001
FOREGROUND_GREE = 0x0002
FOREGROUND_CYAN = 0x0003
FOREGROUND_RED = 0x0004
FOREGROUND_MAGENTA = 0x0005
FOREGROUND_YELLOW = 0x0006
FOREGROUND_GREY = 0x0007
FOREGROUND_INTENSITY = 0x0008

BACKGROUND_BLACK = 0x0000
BACKGROUND_BLUE = 0x0010
BACKGROUND_GREEN = 0x0020
BACKGROUND_CYAN = 0x0030
BACKGROUND_RED = 0x0040
BACKGROUND_MAGENTA = 0x0050
BACKGROUND_YELLOW = 0x0060
BACKGROUND_GREY = 0x0070
BACKGROUND_INTENSITY = 0x0080

SHORT = c_short
WORD = c_ushort

class Coord(Structure):
    _fields_ = [
        ("X", SHORT),
        ("Y", SHORT)]

class SmallRect(Structure):
    _fields_ = [
        ("Left", SHORT),
        ("Top", SHORT),
        ("Right", SHORT),
        ("Bottom", SHORT)]

class ConsoleScreenBufferInfo(Structure):
    _fileds_ = [
        ("dwSize", Coord),
        ("dwCursorPosition", Coord),
        ("wAttributes", WORD),
        ("srWindow", SmallRect),
        ("dwMaximumWindowSize", Coord)]

# winbase.h
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo

def get_text_attr():
    csbi = ConsoleScreenBufferInfo()
    GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
    return csbi.wAttributes

def set_text_attr(color):
    SetConsoleTextAttribute(stdout_handle, color)

def cprint(msg, color):
    default_colors = get_text_attr()
    default_bg = default_colors & 0x00F0

    set_text_attr(color | default_bg)
    sys.stdout.write(msg)
    set_text_attr(default_colors)

    sys.stdout.flush()

def print_error(msg):
    cprint('Error: ', FOREGROUND_RED | FOREGROUND_INTENSITY)
    print (msg)

def print_k2logo():
    logo = '''    KICOM Anti-Virus II (for %s) Ver %s (%s) 
    Copyright (C) 1995-%s Kei Choi. ALL rights reserved.'''
    print '----------------------------------------------------------------'
    print (logo %(sys.platform.upper(), KAV_VERSION, KAV_BUILDDATE, KAV_LASTYEAR))
    print '----------------------------------------------------------------'
    
class OptionParsingError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg
class OptionParingExit(Exception):
    def __init__(self, status, msg):
        self.msg = msg
        self.status = status

class ModifiedOptionParser(OptionParser):
    def error(self, msg):
        raise OptionParsingError(msg)
    
    def exit(self, status=0, msg=None):
        raise OptionParsingExit(status, msg)

def define_options():
    usage = "Usage: %prog path[s] [options]"
    parser = ModifiedOptionParser(add_help_option=False, usage=usage)
    
    parser.add_option("-f", "--files", action="store_true", dest="opt_files", default=True)
    parser.add_option("-I","--list",action="store_true", dest="opt_list", default=True)
    parser.add_option("-V","--vlist",action="store_true", dest="opt_vlist", default=False)
    parser.add_option("-?","--help",action="store_true", dest="opt_help", default=False)
    
    return parser
    
def parser_options():
    parser = define_options()
    
    if len(sys.argv) < 2:
        return "NONE_OPTION", None
    else:
        try:
            (options, args) = parser.parse_args()
            if len(args) == 0:
                return options, None
        except OptionParsingError, e:
            return 'ILLEGAL_OPTION', e.msg
        except OptionParsingExit, e:
            return 'ILLEGAL_OPTION', e.msg
        
        return options, args

def print_usage():
    print '\nUsage: k2.py path[s] [options]'

def print_options():
    options_string= \
        '''Options:
                -f, --files         scan files *
                -I, --list          display all files
                -V, --vlist         display virus list
                -?, --help          this help
                                    * = default option'''
    print options_string
    
def listvirus_callback(plugin_name, vnames):
    for vname in vnames:
        print '%-50s [%s.kmd]' %(vname, plugin_name)

#main()
def main():
    options, args = parser_options()
    
    print_k2logo()
    
    if options == 'NONE_OPTION':
        print_usage()
        print_options()
        return 0
    elif options == 'ILLEGAL_OPTION':
        print_usage()
        print 'Error: %s' % args
        return 0
      
    if options.opt_help:
        print_usage()
        print_options()
        return 0
    
    k2 = kavcore.k2engine.Engine()
    if not k2.set_plugins('plugins'):
        print
        print_error('KICOM Anti-Virus Engine set_plugins')
        return 0
        
    kav = k2.create_instance()
    if not kav:
        print
        print_error('KICOM Anti-Virus Engine create_instance')
        return 0
        
    if not kav.init():
        print
        print_error('KICOM Anti-Virus Engine init')
        return 0
    
    if options.opt_vlist is True:
        kav.listvirus(listvirus_callback)
    else:
        if args:
            for scan_path in args:
                scan_path = os.path.abspath(scan_path)
                
                if os.path.exists(scan_path):
                    print scan_path
                else:
                    print_error('Invalid path: \'%s\'' %scan_path)
    kav.uninit()

if __name__ == '__main__':
    main()

