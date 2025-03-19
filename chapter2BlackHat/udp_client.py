import socket
host=""
port=5002
client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.sendto(b"fm",(host,port))
data,addr=client.recvfrom(4096)
print(data.decode())
client.close()
