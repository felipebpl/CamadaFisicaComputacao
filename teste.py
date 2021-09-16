#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from enlace import *
import time
import random
import numpy as np

serialName = "COM6"

class Datagram:
    def __init__(self, head, payload, eop):
        self.head = head
        self.payload = payload
        self.eop = b'\x01\x02\x03\x04'

    def create_datagram(self):
        return (self.head + self.payload + self.eop)

class Head:
    def __init__(self, data, size, pkg_number):
        self.data = data
        self.size = size
        self.pkg_number = pkg_number
    
    def create_head(self):
        self.array_data = np.asarray(self.data)
        self.array_size = np.asarray(self.size)
        self.array_pkgnumber = np.asarray(self.pkg_number)

        return self.data == [b'self.data', b'self.size', b'pkg_number', b'00',b'00', b'00', b'00', b'00', b'00', b'00']

class Payload:
    def __init__(self):
        
        
        


print(Head.create_head())

#if __name__ == "__main__":
#    main()