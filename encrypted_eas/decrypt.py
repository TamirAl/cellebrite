import os
import sys
import random

class CellebriteEas(object):
    def __init__(self):
        self._box = bytearray(256)
        self.KEY_SIZE = 16 #Decodieren
        self.BOX_SIZE = 256
        self._encryptionKey=None
        
    def setKey(self,Key):
        self._encryptionKey=Key
        for index in range(256):
            self._box[index] = index;
        index1 = 0
        keylength = len(self._encryptionKey)
        for index2 in range(256):
            index1 = (index1 +  self._box[index2] + self._encryptionKey[index2 % keylength]) % 256
            num = self._box[index2]
            self._box[index2] = self._box[index1]
            self._box[index1] = num

    def crypto(self,data):
        index1 = 0
        index2 = 0
        numArray1 = bytearray(len(data))
        numArray2 = bytearray()
        numArray2+=self._box
        for index3 in range(len(data)):
            index1 = (index1 + 1) % 256
            index2 = (index2 + numArray2[index1]) % 256
            num1 = numArray2[index1]
            numArray2[index1] = numArray2[index2]
            numArray2[index2] = num1
            num2 = data[index3]
            num3 = numArray2[( numArray2[index1] + numArray2[index2]) % 256]
            numArray1[index3] = ( num2 ^ num3)&0xff
        return numArray1    
    
        
    def decrypt(self,filename):
        buffer=bytearray()
        with open(filename,"rb") as file:
            file_data=file.read()
            Key=bytearray(file_data[-16:])
            Data=bytearray(file_data[:-16])
            self.setKey(Key)
            return self.crypto(Data)
        

def decrypt_file(filename):
    enc = CellebriteEas()
    with open(filename+".dll","wb") as file:
        file.write(enc.decrypt(filename))

def do_decrypt(basedir,hash):
    print("Im {0} running".format(basedir))
    for root, dirs, files in os.walk(basedir):
        for name in files:
            if ".epr"==name[-4:]:
                print("{0} processing".format(name))
        filename=os.path.join(root,name)
        decrypt_file(filename)



decrypt_file("bb_whatsapp.eas")

