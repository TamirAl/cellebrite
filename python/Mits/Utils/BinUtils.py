import os 

def hex_to_bin(path):    """    takes the path of a hex file, and creates a bin file from it. (adds .bin extention)    hex - this ugly ascii format that has a CRC at the end of every line    bin - normal binary format
    the function returns the load address of the binary code as extracted from the hex    """        data = file(path,"rb").read()    lines = data.split("\r\n")
    load_address = eval ("0x"+ lines[0][9:-2])
    lines = lines[2:]    f = file(path + ".bin","wb")    for l in lines:        f.write(l[9:-2].decode('hex'))    f.close()
    return load_address

def endian_reverse(b):    """    reverse the endian of a four byte string    """        ret = ""    for i in xrange(0,len(b),4):        ret += b[i+3] + b[i+2] + b[i+1] + b[i]    return ret
def get_bits(opcode, start, end):    return (((opcode) >> (start)) & ((1 << ((end) - (start)+1)) -1))    
def hex_print(src, length=32):    FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])    result=[]    for i in xrange(0, len(src), length):        s = src[i:i+length]        hexa = ' '.join(["%02X"%ord(x) for x in s])        printable = s.translate(FILTER)        printable = printable.ljust(length)        result.append("%04X | %-*s| %s |\r\n" % (i, length*3, hexa, printable))    return ''.join(result)
