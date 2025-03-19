import paramiko
def ssh_command(ip, port, user, passwd, cmd):
     client = paramiko.SSHClient()
     client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
     client.connect(ip, port=port, username=user,password=passwd)
     #client.exec_command->executes command on remote ssh server
     #client.exec_command returns three values->stdin,stdout,stderr
     #_ means Ignoring stdin
     _,stdout,stderr =client.exec_command(cmd) 
     #stdout.readlines() → Reads all lines of output from the command
     #stderr.readlines() → Reads any error messages from the command
     output = stdout.readlines() + stderr.readlines() 
     if output: 
        print('--- Output ---') 
        for line in output: 
            print(line.strip()) #strip-># Removes extra spaces and newlines
if __name__ == '__main__': 
 import getpass 
 # user = getpass.getuser() 
 user = input('Username: ') 
 password = getpass.getpass() #securely take a password input from the user without displaying it on the screen
 ip = input('Enter server IP: ') or '192.168.1.203' 
 port = input('Enter port or <CR>: ') or 2222 
 cmd = input('Enter command or <CR>: ') or 'id' 
 ssh_command(ip,port,user,password,cmd)
 
