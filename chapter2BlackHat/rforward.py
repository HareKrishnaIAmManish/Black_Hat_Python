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
def parse_options():
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
def main():
    pass
if __name__ == "__main__":
    main()