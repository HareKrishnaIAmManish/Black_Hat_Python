import os 
import paramiko 
import socket 
import sys 
import threading 
CWD = os.path.dirname(os.path.realpath(__file__)) #gives the directory
# CWD → Stores the directory where your script (ssh_rcmd.py) is located
#os.path.join(CWD, 'test_rsa.key') → Constructs the full path to test_rsa.key, assuming it's in the same directory as the script.
#paramiko.RSAKey(filename=...) → Loads an RSA private key from the specified file (test_rsa.key), which is typically used for SSH authentication.
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD,'test_rsa.key')) 
class Server (paramiko.ServerInterface): #inheritence ho raha paramiko.ServerInterface is base class provided by the paramiko library to define an SSH server
    #authentication methods
    def _init_(self): 
       self.event = threading.Event() #event object from Python's threading module The Event class object provides a simple mechanism which is used for communication between threads where one thread signals an event while the other threads wait for it
    def check_channel_request(self, kind, chanid): 
       if kind == 'session': 
            return paramiko.OPEN_SUCCEEDED 
       return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED 
    def check_auth_password(self, username, password): 
        if (username == '') and (password == ''): 
            return paramiko.AUTH_SUCCESSFUL 
        else:
            return paramiko.AUTH_FAILED
if __name__ == '__main__': 
    server = ''
    ssh_port =
    try: 
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #sock.setsockopt(level, option, value)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        sock.bind((server, ssh_port)) 
        sock.listen(100) 
        print('[+] Listening for connection ...') 
        client, addr = sock.accept() 
    except Exception as e: 
        print('[-] Listen failed: ' + str(e)) 
        sys.exit(1) 
    else: #if except fails
        print('[+] Got a connection!', client, addr)
    bhSession = paramiko.Transport(client) #creates a new SSH transport session
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)
    chan = bhSession.accept(20) #waits for a client to start a ssh session for 20 seconds
    if chan is None: 
        print('*** No channel.') 
        sys.exit(1)
    print('[+] Authenticated!')       
    print(chan.recv(1024))
    chan.send('Welcome to bh_ssh')
    try: 
        while True: 
            command= input("Enter command: ") 
            if command != 'exit': 
                chan.send(command) 
                r = chan.recv(8192) 
                print(r.decode()) 
            else: 
                chan.send('exit') 
                print('exiting') 
                bhSession.close() 
                break 
    except KeyboardInterrupt: 
        bhSession.close()
#server is sending the command client is sending the reponse             

