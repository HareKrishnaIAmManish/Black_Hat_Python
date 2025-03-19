import sys 
import socket 
import threading
HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])
#................................ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHI
# JKLMNOPQR
# STUVWXYZ[.]
# ^_`abcdefghijklmnopqrstuvwxyz{|}~.....................
# .............¡¢£¤¥¦§¨©ª«¬.®¯°±²³´µ¶·¸¹º
# »¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñ
# òóôõö÷øùúûüýþÿ
#print(len(repr(chr(74))))
def hexdump(src, length=16, show=True): 
 if isinstance(src, bytes): #if src type is bytes
    src = src.decode() 
 results = list() 
 for i in range(0, len(src), length): 
   word = str(src[i:i+length]) 
   printable = word.translate(HEX_FILTER) #non printable is replaced with .
   #ord gives unicode
   #0 if padding required 2 characters wide X is converts to uppercase 
   hexa = ' '.join([f'{ord(c):02X}' for c in word]) 
   hexwidth = length*3 #its a constant 2 hex digits and one spaace
   #04 ->4-digit width, padded with zeros if necessary x → Convert to lowercase hexadecimal.
   # < means left-align  hexa inside a field of 
   # width hexwidth, ensuring that all hex dumps line up neatly in columns.
   results.append(f'{i:04x}  {hexa:<{hexwidth}}{printable}') 
 if show: 
     for line in results: 
         print(line) 
 else: 
        return results
#hexdump('python rocks\n and proxies roll\n') 
def receive_from(connection): #connection is socket object
    buffer = b""
    connection.settimeout(5)
    try: 
        while True: 
            data = connection.recv(4096) 
            if not data: 
                break 
            buffer += data 
    except Exception as e: 
        pass 
    return buffer
#afterwards i will
def request_handler(buffer): 
    # perform packet modifications 
    return buffer 
def response_handler(buffer): 
    # perform packet modifications 
    return buffer
                                  #host ip           #host port
def proxy_handler(client_socket, remote_host, remote_port,receive_first): 
    #tcp server object                  
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    # connect to server
    remote_socket.connect((remote_host, remote_port))
    #if im receiving first
    if receive_first:
        #received from  host remote_socket
        remote_buffer = receive_from(remote_socket)     #remote->server
        #printing 
        hexdump(remote_buffer) 
        #handling the respose afterwards i will
        remote_buffer = response_handler(remote_buffer) 
        #if there is a remote buffer
        if len(remote_buffer): 
          #sending to localhost
          print("[<==] Sending %d bytes to localhost." %len(remote_buffer))
          client_socket.send(remote_buffer) #client socket  to host
    while True:
        #receiving from client
        local_buffer = receive_from(client_socket)
        # if local buffer is there ie something from host which is client_socket 
        if len(local_buffer):     
            line = "[==>]Received %d bytes from localhost." %len(local_buffer)
            print(line)
            hexdump(local_buffer)
            #request handler afterwards i will
            local_buffer = request_handler(local_buffer) 
            #sending to host 
            remote_socket.send(local_buffer) 
            print("[==>] Sent to remote.") #remote->server
            #recieving from host
        remote_buffer = receive_from(remote_socket)  
        #if received from remote socket ie the host ie server 
        if len(remote_buffer):
             print("[<==] Received %d bytes from remote." % len(remote_buffer)) 
             hexdump(remote_buffer)
             remote_buffer = response_handler(remote_buffer) 
             #sending to client
             client_socket.send(remote_buffer)     #client->localhost
             print("[<==] Sent to localhost.") 
        #if nothing is received from neither the host nor the server
        if not len(local_buffer) or not len(remote_buffer):
            #closing both the sockets
            client_socket.close() 
            remote_socket.close() 
            print("[*] No more data. Closing connections.") 
            break 
       #setting up a server_loop           
def server_loop(local_host, local_port,remote_host, remote_port, receive_first): 
    #server ->localhost
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    try: 
        server.bind((local_host, local_port)) 
    except Exception as e: 
        print('problem on bind: %r' % e) 
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port)) 
        print("[!!] Check for other listening sockets or correct permissions.") 
        sys.exit(0) 
        #server started at local host
    print("[*] Listening on %s:%d" % (local_host,local_port)) 
    server.listen(5) 
    while True:
        client_socket, addr = server.accept() 
        # print out the local connection information 
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1]) 
        print(line) 
        # start a thread to talk to the remote host 
        proxy_thread=threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port, receive_first)) 
        proxy_thread.start()
def main(): 
    if len(sys.argv[1:]) != 5: 
        print("Usage: ./proxy.py [localhost] [localport]",end='') 
        print("[remotehost] [remoteport] [receive_first]") 
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True") 
        sys.exit(0) 
    local_host = sys.argv[1] 
    local_port = int(sys.argv[2]) 
    remote_host = sys.argv[3] 
    remote_port = int(sys.argv[4]) 
    receive_first = sys.argv[5] 
    if "True" in receive_first: 
        receive_first = True 
    else: 
        receive_first = False 
    server_loop(local_host, local_port, 
        remote_host, remote_port, receive_first) 
if __name__ == '__main__': 
    main()     