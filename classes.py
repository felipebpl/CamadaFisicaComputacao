#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from os import error, path
from enlace import *
import numpy as np
import math


class Datagram:

    def __init__(self, door):
        self.com1 = enlace(door)
        self.com1.enable()
        print('open')
        self.eop = b'\x00\x00\x00\x00'

    def create_datagram(self, head, pkg=b''):
        return (head + pkg + self.eop)

class Head():
    def __init__(self, total, size, pkg_number):

        self.head_list = []
        self.total = total
        self.size = size
        self.pkg_number = pkg_number
    
    def create_head(self):
        #head_list.append((self.type).to_bytes(1, 'big'))
        self.head_list.append(int(self.total).to_bytes(1, 'big'))
        self.head_list.append(int(self.size).to_bytes(1, 'big'))
        self.head_list.append(int(self.pkg_number).to_bytes(1, 'big'))
        self.head = b''.join(self.head_list)

        while len(self.head) <= 10:
            self.head += b'\xFF'

        return (self.head)

class Payload():
    def __init__(self, content):
        self.content = content

    def build_package(self): 
        #retorna os pacotes já separados
        self.package_list = []
        for size in range(self.total_packages()):
            self.package_list.append([self.content[size*114:(size+1)*114]])
        return self.package_list

    def package_size(self):
        #retorna o tamanho do pacote
        self.size_package = []
        for size in range(len(self.build_package())):
            self.size_package.append(len(Payload.build_package(self)[size][0]))
        return self.size_package

    def total_packages(self):
        #retorna a quantidade de pacotes
        self.packages = math.ceil(len(self.content)/114)
        return self.packages

    def packages_number(self):
        #retorna a lista dos pacotes separados
        self.n = []
        for size in range(len(self.package_size())):
            self.n.append(size + 1)
        return self.n
