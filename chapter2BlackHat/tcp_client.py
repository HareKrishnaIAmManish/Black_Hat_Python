import socket
target_host=""
target_port=5001
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))
client.send(b"some data i sent again once more once more ok now stop not stopping")
response=client.recv(4096)
print(response.decode())
client.close()