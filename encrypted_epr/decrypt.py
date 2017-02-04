import os
import sys
import hashlib
from Crypto.Cipher import AES
import mmap

Majic=bytes("Cellebrite EPR File\x1A",'utf-8')
keydata=bytes('Cellebrite EPR file version 1 AES key','utf-8')
hash=hashlib.sha256(keydata)

def decrypt_CBC(data,hash,iv):
    aes = AES.new(hash.digest(), AES.MODE_CBC, iv) #Decodieren
    try:
        for x in range(int(len(data)/16)):
            yield aes.decrypt(bytes(data[x*16:(x+1)*16]))
    except Exception as e:
        print("Exception decrypt_CBC {1}".format(str(e)))
        pass
    
    

def decrypt_file(filename,hash):
    with open(filename,"rb") as cfile:
        map=mmap.mmap(cfile.fileno(), 0, access=mmap.ACCESS_COPY)
        data=memoryview(map)
        if data[:len(Majic)]==Majic:
            ddata=data[len(Majic)+1:]
            iv=bytearray(ddata[:16])
            with open(filename+".zip","wb") as ofile:
                for decrypted in decrypt_CBC(ddata[16:],hash,bytes(iv)):
                    ofile.write(decrypted)
        else:
            print("{0} is not a good file".format(name))


def do_decrypt(basedir,hash):
    print("Im {0} running".format(basedir))
    for root, dirs, files in os.walk(basedir):
        for name in files:
            if ".epr"==name[-4:]:
                print("{0} processing".format(name))
                decrypt_file(os.path.join(root,name),hash)


decrypt_file("ufedsamsungpack_v2.epr",hash)


