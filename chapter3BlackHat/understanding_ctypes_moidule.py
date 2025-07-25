from ctypes import *
import socket
import struct
class IP(Structure):
    _fields_=[
    #(name of the field->internet header length,data type->unsigned 8bit byte,number of bits this field occupies)    
        ("ihl",c_ubyte,4),#4 bit unsigned char
        ("version",c_ubyte,4), #4 bit unsigned char
        ("tos",c_ubyte,8), #1 byte char 
        #(name of field,unsigned short,number of bits this field occupies)
        ("len",c_ushort,16), #2 byte unsigned short
        ("id",c_ushort,16),#2 byte unsigned short
        ("offset",c_ushort,16),#2 byte unsigned short
        ("ttl",c_ubyte,8),  #1 byte char
        ("protocol_num",c_ubyte,8), #1 byte char
        ("sum",c_ushort,16),  #2 byte unsigned short
        ("src",c_uint32,32),     # 4 byte unsigned int
        ("dst",c_uint32,32)     # 4 byte unsigned int   
    ]
    def __new__(cls,socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)
    def __init__(self, socket_buffer=None):
        #human readable ip addresses
        self.src_address=socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address=socket.inet_ntoa(struct.pack("<L",self.dst))
        #whats happening here
        #we are converting raw 32 bit source ip to readable string
        #struct.pack->returns 4 byte binary string from integer
        # < ->little endian byte order L ->unsigned long 