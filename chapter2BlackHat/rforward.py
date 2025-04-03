"""
Sample script showing how to do remote port forwarding over paramiko.

This script connects to the requested SSH server and sets up remote port
forwarding (the openssh -R option) from a remote port through a tunneled
connection to a destination reachable from the local machine.
"""
import getpass
import os
import socket
import select
import sys
import threading
from optparse import OptionParser
import paramiko
SSH_PORT = 22
DEFAULT_PORT = 4000
g_verbose = True
def handler(chan, host, port):
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except Exception as e:
        verbose("Forwarding request to %s:%d failed: %r" % (host, port, e))
        return
    verbose(
        "Connected!  Tunnel open %r -> %r -> %r"
        % (chan.origin_addr, chan.getpeername(), (host, port))
    )
    while True:
        r, w, x = select.select([sock, chan], [], [])
        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            chan.send(data)
        if chan in r:
            data = chan.recv(1024)
            if len(data) == 0:
                break
            sock.send(data)
    chan.close()
    sock.close()
    verbose("Tunnel closed from %r" % (chan.origin_addr,))
def reverse_forward_tunnel(server_port, remote_host, remote_port, transport): #sets up a reverse forward tunnel
    transport.request_port_forward("", server_port) #listen on server port and forword any incoming connection
    while True:
        chan = transport.accept(1000) # waits for connection for 1 second
        if chan is None:
            continue
        thr = threading.Thread(
            target=handler, args=(chan, remote_host, remote_port)
        )
        thr.setDaemon(True)
        thr.start()
def verbose(s):
    if g_verbose:
        print(s)
HELP = """\
Set up a reverse forwarding tunnel across an SSH server, using paramiko. A
port on the SSH server (given with -p) is forwarded across an SSH session
back to the local machine, and out to a remote site reachable from this
network. This is similar to the openssh -R option.
"""
def get_host_port(spec, default_port):
    "parse 'hostname:22' into a host and port, with the port optional"
    args = (spec.split(":", 1) + [default_port])[:2]
    args[1] = int(args[1])
    return args[0], args[1]
def parse_options():
    global g_verbose #make it a global variable
    #expected useage pattern at run time
    parser = OptionParser(
        # %prog is replaced by script name at runtime 
        usage="usage: %prog [options] <ssh-server>[:<server-port>]",
        version="%prog 1.0",
        description=HELP,
    )
    # if -q or --quiet is used then verbose is set to false
    # by default verbose is set true otherwise
    parser.add_option(
        "-q",
        "--quiet",
        action="store_false",
        dest="verbose",
        default=True,
        help="squelch all informational output",
    )
    parser.add_option( #sets port or by default its DEFAULT_PORT
        "-p",
        "--remote-port",
        action="store",
        type="int",
        dest="port",
        default=DEFAULT_PORT,
        help="port on server to forward (default: %d)" % DEFAULT_PORT,
    )
    #sets user or by default it asks
    parser.add_option(
        "-u",
        "--user",
        action="store",
        type="string",
        dest="user",
        default=getpass.getuser(),
        help="username for SSH authentication (default: %s)"% getpass.getuser(),
    )
    parser.add_option( #private key file or None by default
        "-K",
        "--key",
        action="store",
        type="string",
        dest="keyfile",
        default=None,
        help="private key file to use for SSH authentication",
    )
    parser.add_option(
        "",
        "--no-key",
        action="store_false",
        dest="look_for_keys",
        default=True,
        help="don't look for or use a private key file",
    )
    parser.add_option( #if -P or --password is used then readpass is equal to true if not used defaulted to False
        "-P",
        "--password",
        action="store_true",
        dest="readpass",
        default=False,
        help="read password (for key or password auth) from stdin",
    )
    parser.add_option( #stores the ip:port of the remote host im remote variable
        "-r",
        "--remote",
        action="store",
        type="string",
        dest="remote",
        default=None,
        metavar="host:port",#tells  user that it should be written as ip:port
        help="remote host and port to forward to",
    ) 
    #options->flag based arguments 
    #args->position based arguments they dont have like this - or -- they are required in a particular order
    options,args=parser.parse_args()
    if len(args) != 1:
        parser.error("Incorrect number of arguments.")
    if options.remote is None:
        parser.error("Remote address required (-r).")
    g_verbose = options.verbose
    server_host, server_port = get_host_port(args[0], SSH_PORT)
    remote_host, remote_port = get_host_port(options.remote, SSH_PORT)
    return options, (server_host, server_port), (remote_host, remote_port)
def main():
    options, server, remote = parse_options()
    password = None
    if options.readpass:
        password = getpass.getpass("Enter SSH password: ")
    client = paramiko.SSHClient() #the client object
    client.load_system_host_keys() #loads ssh host key from systems default know hosts file
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    verbose("Connecting to ssh host %s:%d ..." % (server[0], server[1]))
    try:
        client.connect(
            server[0],
            server[1],
            username=options.user,
            key_filename=options.keyfile,
            look_for_keys=options.look_for_keys,
            password=password,
        )
    except Exception as e:
        print("*** Failed to connect to %s:%d: %r" % (server[0], server[1], e))
        sys.exit(1)
    verbose(
        "Now forwarding remote port %d to %s:%d ..."
        % (options.port, remote[0], remote[1])
    )
    try:
        reverse_forward_tunnel(
            options.port, remote[0], remote[1], client.get_transport()
        )
    except KeyboardInterrupt:
        print("C-c: Port forwarding stopped.")
        sys.exit(0)
if __name__ == "__main__":
    main()
    