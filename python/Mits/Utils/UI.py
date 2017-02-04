"""    User Interface Module    used to gather all user interface methods
"""
from Mits.Utils.SerialScan import WinScan

def get_serial_port():    """    Scans for avaliable serial ports    and let user choose one port    """
    while(True):        print "Available Serial Ports: "        ports = WinScan().comports()        ports_num =  [port[0] for port in ports]
        ports = WinScan().comports()        ports_txt =  [port[2]  for port in ports]
        print "\t" + "\r\n\t".join(ports_txt)        try:            port = int(input("Select Port (Enter for rescan): "))#            if not (port in ports_num):#                print "Invalid port number!\r\n"#                continue
        except SyntaxError, e:            print ""            continue        break
    return port