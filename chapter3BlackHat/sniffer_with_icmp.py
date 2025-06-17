import ipaddress
import os
import socket
import struct
import sys
class IP:
    def __init__(self,buff=None):
        header=struct.unpack('<BBHHHBBH4s4s',buff)
        self.ver=header[0]>>4
        self.ihl=header[0] & 0xF
        self.tos=header[1]
        self.len=header[2]
        self.id=header[3]
        self.offset=header[4]
        self.ttl=header[5]
        self.protocol_num=header[6]
        self.sum=header[7]
        self.src=header[8]
        self.dst=header[9]
        # human readable ip addresses
        self.src_address=ipaddress.ip_address(self.src)
        self.dst_address=ipaddress.ip_address(self.dst)
        #map protocol constants to their names
        self.protocol_map={1:"ICMP",6:"TCP",17:"UDP"}
        try:
            self.protocol=self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s No protocol for %s' %(e,self.protocol_num))
            self.protocol=str(self.protocol_num)
class ICMP:
     def __init__(self,buff):
          header=struct.unpack('<BBHHH',buff)
          self.type=header[0]
          self.code=header[1]
          self.sum=header[2]
          self.id=header[3]
          self.seq=header[4]
def sniff(host):
        # should look familier from previous example
        if os.name=='nt':   #windows
            socket_protocol=socket.IPPROTO_IP    #socket.IPPROTO_IP -> used when working with raw IP packets on windows tells socket to recieve all kinds of ip packets irrespective of protocol 
        else:  #posix
            socket_protocol=socket.IPPROTO_ICMP  #used in linux/macos when you only want to capture ICMP packets like ping      
        sniffer=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol) #creates a raw socket.... raw socket gives us access to the headers and payload of packets... you can capture low level network traffic (Like IP,ICMP,TCP headers),whch normal sockets hide
        #this sniffer sockket we just created help us to sniff socket at low level captures raw IP/ICMP data 
        sniffer.bind((host,0))
               #setsockopt(level             ,option          ,value)
        sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)  #sets a socket opotion that tell the raw socket how to handle ip headers  here level=socket.IPPROTO_IP were configuring option at IP protocol level IP_HDRINCL->IP header included value=1 means enable the option (1 means true)  
        if os.name=='nt':
            sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON) #turn on the promocious mode ,ioctl ->input output control for performing low level low level input output control operations on socket specific to windows platform think of it like we are sending special commands to network driver SIO_RCVALL->contrl code which tells windows to receive all packets not just ones which are addressed to your machine RCVALL_ON -> flag to enable promiscuous mode
            #WHAT IS PROMISCUOUS MODE
            # Normally your network adapter only process packets which are
            # ->addressed to your machine 
            # -> Or broadcast/Multcast traffic 
            # in promiscuous mode the adapter passes all traffic it sees on the network (regardless of destination) up to your application allowing to sniff all packets on the network segment   
        try:
                while True:
                    #read a packet 
                    raw_buffer=sniffer.recvfrom(65535)[0]  #recvfrom returns a tuple (data,address) data->raw bytes of the packet address->source ip address the packet came from
                    #create a IP header from first 20 bytes 
                    ip_header=IP(raw_buffer[0:20])
                    #print the detected protocol and hosts                    
                    print('Protocol: %s %s  -> %s' %(ip_header.protocol,ip_header.src_address,ip_header.dst_address))
                    if ip_header.protocol=="ICMP":
                         print('Protocol: %s %s -> %s' %(ip_header.protocol,ip_header.src_address,ip_header.dst_address))
                         print(f'Version: {ip_header.ver}')
                         print(f'Header length: {ip_header.ihl} TTL:{ip_header.ttl}')
                         #calculate where our ICMP PACKET STARTS
                         offset=ip_header.ihl*4
                         buf=raw_buffer[offset:offset+8]
                         #creating our ICMP structure
                         icmp_header=ICMP(buf)
                         print('ICMP-> Type: %s Code: %s\n'%(icmp_header.type,icmp_header.code))
        except KeyboardInterrupt:
                # if we are on Windows turn off promiscuous mode 
                  if os.name=='nt':
                      sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
                  sys.exit()
if __name__=='__main__':
    if len(sys.argv)==2:
        host=sys.argv[1]
    else:
        host=''
    sniff(host)                 

        