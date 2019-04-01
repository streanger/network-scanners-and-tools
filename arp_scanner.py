import sys
import socket
from scapy.all import Ether, ARP, srp, get_windows_if_list

def your_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return ip
    
    
def arp_scanner(_interface):
    locals = []
    _range = "172.31.98.1/24"
    ip, ntBits = _range.split('/')
    ip_addresses = []
    st_bit = ip.split('.')[3:4][0]   #Since it's an IPv4
    for n in range(1, int(ntBits)+1):
        eval_ip = ".".join( ip.split('.')[:-1] ) + '.' + str(n)
        ip_addresses.append( eval_ip )

    for ip in ip_addresses:
        _pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
        ans, unans = srp( _pkt, iface=_interface, timeout=0.1, verbose=False)
        for snt, recv in ans:
            if recv:
                print("\t--> Host Alive: %s - %s" % (recv[ARP].psrc, recv[Ether].src))
                locals.append(recv[ARP].psrc)
    return locals
    
    
def main():
    interfaces = get_windows_if_list()
    localsDictio = {}
    localsIpList = []
    for key, _ in enumerate(interfaces):
        name = interfaces[key]['name']
        mac = interfaces[key]['mac']
        print("{}, mac: {}, found:".format(name, mac))
        try:
            locals = arp_scanner(name)
            localsDictio[name] = locals
            localsIpList = [ip for locals in list(localsDictio.values()) for ip in locals]
        except KeyboardInterrupt:
            print("CTRL+C pressed. Exiting. ")
            continue
    return localsIpList
    
    
if __name__ == "__main__":
    locals = main()
    
    
'''
based on:
    https://www.shellvoide.com/python/how-to-build-an-arp-scanner-python-using-scapy/
    
    
started to work:
    -26.02.2019
    
'''
