import socket
import threading
ip=""
port=5001
def handle_client(client_socket):
    with client_socket as sock:
        req=sock.recv(1024)
        print(f'recieved:{req.decode("utf-8")}')
        sock.send(b"ACK")
        sock.send(b"hello")
def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    print(f"listening on ip:{ip} port:{port}")
    while True:
        client,addr=server.accept()
        print(f"accepted connection from addr0:{addr[0]} addr1:{addr[1]}")                           
        client_handler=threading.Thread(target=handle_client,args=(client,))
        client_handler.start()   
if __name__=='__main__':
    main()