#!/usr/bin/python

from __future__ import with_statement, print_function
import sys
import struct
#import binascii

MAX_PATH_LEN=16384

#only needed for precice size
#(defined as general integer)
file_fmt="IIQIIII"
file_size=struct.calcsize(file_fmt)
#buf=sys.stdin.read(file_size)
crc32_sum = 0 #binascii.crc32(buf)

#The = turns the system-sizes into
#natural (=32 byte int) sizes, replicating
#uint32 behaviour.
result_fmt="=IIQ"
result_size=struct.calcsize(result_fmt)

ext_fmt = "=I"
ext_size=struct.calcsize(ext_fmt)
#read string later, once lenght is known!
#'p' for pascal string not applicable, since max_name_len bigger and therefore,
#first FOUR bytes are required for exact length!


#pipe has to be OPEN, otherwise sending VM won't start to write.
#pipe is open once it's ready to be read (by sending VM) AND write
#(by the following command).
with open(sys.argv[1], 'w') as f:
    stream = sys.stdin.read(result_size)
    error, _pad, crc32 = struct.unpack_from(result_fmt, stream)
    if error==None: #... nothing could be read.
        #... WTF is errno EAGAIN? Need to know dat shit!
        #Since we don't know, we jut hope for the best!
        exit(1) #hopefully remote as produced error message

    last_namelen, = struct.unpack_from(ext_fmt, sys.stdin.read(ext_size))
    #don't allow last_name to send more bytes than it should!
    last_namelen = min(last_namelen, MAX_PATH_LEN)

    name_fmt = "=%is" %last_namelen
    name_size = struct.calcsize(name_fmt)

    #This is the last thing we have to read from pipe!
    last_name, = struct.unpack_from(name_fmt, sys.stdin.read(name_size))

    if last_name == None:
        print("Failed to get last filename!", file=sys.stderr)
    else:
        #This is the one and only write to pipe!
        f.write(last_name)

if not error==0:
    if error==17:
        print("This file already exists!", file=sys.stderr)
    else:
        print("There was an error, I can tell you which one once I've found <errno.h> ... (ARGH!)", file=sys.stderr)
        print("Errno: %i" %error, file=sys.stderr)

#no error. We should calculate our own crc, but we would need the file for that,
#so we would need the file-stream and thereby open dom0 to bugs in crc32.
#another option would be to compare from-vm-crc32 and to-vm-crc32.
#Haven't found good solution to implement this yet, until then
#we don't check crc. Just hope everyhint went okay, I guess ...

#gracefull exit
sys.stdin.close()
sys.stderr.close()
sys.stdout.close()
exit(0 if error==0 else 1)
