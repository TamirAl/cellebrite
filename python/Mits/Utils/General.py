import Mits.Configuration.Config as MitsConfig
import subprocess
from array import array
import struct
import string
import re
from time import ctime, time


from Mits.Utils.upy import upy


# This function is not needed on the UFED, as it is used only with legacy
# code that will not be ported to UFED
# Used by gen_response function
import Crypto.Cipher.ARC4 as RC4




def gen_response(challange):
    """
    generates the response for the challange that the bootloader presents
    when it starts.
    """


    key = [0x04, 0x30, 0xA0, 0xE3, 0x00, 0x20, 0x8D, 0xE2, 0x00, 0x10, 0xA0, 0xE3, 0x04, 0x0, 0xA0, 0xE1]
    challange = [challange>>0 & 0xff, challange>>8 & 0xff, challange>>16 & 0xff, challange>>24 & 0xff]
    key = zip(key,challange*4)
    key = "".join([chr(x^y) for x,y in key])
##    print key.encode('hex')
    rc = RC4.new(key)
    rc.decrypt("\0"*1024).encode('hex')
    return struct.unpack(">I",rc.decrypt("\0"*4))[0]






validFilenameChars = "-_.()[] %s%s" % (string.ascii_letters, string.digits)


def removeDisallowedFilenameChars(filename):
    return ''.join(c for c in filename if c in validFilenameChars)




def hex_to_bin(path):
    """
    takes the path of a hex file, and creates a bin file from it. (adds .bin extention)
    hex - this ugly ascii format that has a CRC at the end of every line
    bin - normal binary format


    the function returns the load address of the binary code as extracted from the hex
    """


    data = file(path,"rb").read()
    lines = data.split("\r\n")


    load_address = eval ("0x"+ lines[0][9:-2])


    lines = lines[2:]
    f = file(path + ".bin","wb")
    for l in lines:
        f.write(l[9:-2].decode('hex'))
    f.close()


    return load_address


TIME_NAME = 1


def timed_xrange(start,stop=None,step=None, bytes_per_iteration = 1):
    """
    timed_xrange([start,] stop[, step]) -> integer iterator with time
    """
    global TIME_NAME
    #check params
    if not stop and not step:
        stop = start
        start = 0
        step = 1
    if not step:
        step = 1


    #do loop
    start_time = time()
    last_print_time = 0


    i = start
    prev = start
    prev_time = start_time
    TIME_NAME += 1
    upy.ui_create_progress_bar(str(TIME_NAME), 100)
    while (True):
        if step > 0:
            if i >= stop:
                break
        elif step < 0:
            if i <= stop:
                break
        else:
            raise Exception("Step must not be 0")




        current_time = time()
        if last_print_time < current_time - 5:
            last_print_time = current_time
            #calculate presentage
            presentage = float(i-prev)/(stop-prev)
            progress = float(i-start)/(stop-start)
            upy.ui_update_progress(int(progress * 100))
            if presentage == 0:
                out = False
            else:
                out = True
                eta = ((current_time - prev_time) / presentage) - (current_time - prev_time)
                speed = float(i-prev) / (current_time - prev_time) / 1024
                speed *= bytes_per_iteration
                prev_time = current_time
                prev = i
            if out:
                str_ = "ETA %02d:%02d - %02d%%. 0x%08X (%.02f KB/s)"%(eta/60, eta%60, progress * 100, i, speed)
                print (str_)
                upy.ui_print_during_dump(str_)
            else:
                upy.ui_print_during_dump("calculating time...")
                print "calculating time..."
        yield i


        i += step
    upy.ui_close_progress_bar()




#pack and unpack functions:
#pack converts from a number variable to a binary data string, (unpack does the opposite).
#function naming convention is pack<BB><E>()  where:
#   BB is the bit size of the number variable (i.e 16 means WORD, 32 means DWORD)
#   E is the endian and sign: B of big endian, L for little endian, wile capital letter means unsigned, and lower case letter means signed. (i.e L means unsigned little endian, while b means signed big endian)


def pack64L(data):
    return struct.pack("<Q",data)


def pack64B(data):
    return struct.pack(">Q",data)


def pack32L(data):
    return struct.pack("<I",data)


def pack32B(data):
    return struct.pack(">I",data)


def pack24L(data):
    return struct.pack("<I",data)[:-1]


def pack24B(data):
    return struct.pack(">I",data)[1:]


def pack16L(data):
    return struct.pack("<H",data)


def pack16B(data):
    return struct.pack(">H",data)


def pack8B(data):
    return chr(data)


def unpack8B(data):
    return ord(data)


def unpack16B(data):
    return struct.unpack(">H", data)[0]


def unpack16L(data):
    return struct.unpack("<H", data)[0]


def unpack16l(data):
    return struct.unpack("<h", data)[0]


def unpack24L(data):
    return struct.unpack("<I", data + '\0')[0]


def unpack24l(data):
    return struct.unpack("<i", '\x00'+data)[0] >> 8


def unpack24B(data):
    return struct.unpack(">I", '\0' + data)[0]


def unpack32L(data):
    return struct.unpack("<I", data)[0]


def unpack32B(data):
    return struct.unpack(">I", data)[0]


def unpack32l(data):
    return struct.unpack("<i", data)[0]


def pack32l(data):
    return struct.pack("<i",data)




def unpack64L(data):
    return struct.unpack("<Q", data)[0]


def unpack64B(data):
    return struct.unpack(">Q", data)[0]


def unpack64l(data):
    return struct.unpack("<q", data)[0]


def pack64l(data):
    return struct.pack("<q",data)




def pack64l(data):
    return struct.pack("<q",data)


def pack642b(data):
    return struct.pack(">q",data)




def get_log_path(prefix, middle):
    if prefix:
        prefix = prefix.strip() + " "
    string = r"%s%s %s.log" % \
                (prefix, middle, ctime().replace(":","."))
    string = MitsConfig.DUMP_PATH + removeDisallowedFilenameChars(string)
    return string




def get_dump_file_name(prefix, middle, start=None, end=None, baseAddr=None):
    # if there is a prefix, add a space between it to the middle name
    if prefix:
        prefix = prefix.strip() + " "
    if start != None and end != None:
        if baseAddr is not None:
            string = r"%s%s [0x%x](0x%08X - 0x%08X) %s.bin" % \
                    (prefix, middle, baseAddr, start, end, ctime().replace(":","."))
        else:
            string = r"%s%s (0x%08X - 0x%08X) %s.bin" % \
                    (prefix, middle, start, end, ctime().replace(":","."))
    else:
        string = r"%s%s %s.bin" % \
                (prefix, middle, ctime().replace(":","."))
    string = removeDisallowedFilenameChars(string)
    return string




def get_dump_path(prefix, middle, start=None, end=None, baseAddr=None):
    fn = get_dump_file_name(prefix, middle, start, end, baseAddr)
    string = MitsConfig.DUMP_PATH + fn
    return string










def xor_strings(s1, s2):
    """XOR chars of two strings."""
    a1 = array('B', s1)
    a2 = array('B', s2)
    l = min(len(a1), len(a2))
    for i in xrange(l):
        a1[i] ^= a2[i]
    return a1[:l].tostring()


def get_stdout(command, redirect_err_to_out = False):
    """ get stdout of command. for example get_stdout("netstat")"""
    def my_split(str):
        return [p.replace('"','') for p in re.split("( |\\\".*?\\\"|'.*?')", str) if p.strip()]


    p = subprocess.Popen(my_split(command), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    std, err = p.communicate()
    if err and not redirect_err_to_out:
        raise Exception(err)
    return std + err


def blockify(s, block_size):
	return [s[i:i + block_size] for i in xrange(0, len(s), block_size)]








def rev_byte(b):
    "Reverses the bits in a byte"
    return reduce(
        (lambda a , b : a | b),
        [((1 << (7 - r)) if ((1 << r) & b) else 0) for r in range(8)]
        )


rev_array = [rev_byte(b) for b in range(0x100)]


def rev8(in_str):
    "Reverses the bits in each byte of a string"
    return "".join([chr(rev_array[ord(b)]) for b in in_str])
