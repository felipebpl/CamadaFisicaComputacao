#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from os import error, path
from enlace import *
from math import *


class Datagram:

    def __init__(self, door):
        self.com1 = enlace(door)
        self.com1.enable()
        self.eop = b'\xFF\xAA\xFF\xAA'

    def create_datagram(self, head, pkg=b''):
        return (head + pkg + self.eop)

# h0 – tipo de mensagem
# h1 – id do sensor
# h2 – id do servidor
# h3 – número total de pacotes do arquivo
# h4 – número do pacote sendo enviado
# h5 – se tipo for handshake:id do arquivo
# h5 – se tipo for dados: tamanho do payload
# h6 – pacote solicitado para recomeço quando a erro no envio.
# h7 – último pacote recebido com sucesso.
# h8 – h9 – CRC
# PAYLOAD – variável entre 0 e 114 bytes. Reservado à transmissão dos arquivos.
# EOP – 4 bytes: 0xFF 0xAA 0xFF 0xAA

class Head():
    def __init__(self, tipo, total, pkg_number, payload_size, pacote_solicitado, last_pkg, CRC8, CRC9):
        self.msg_type = tipo
        self.sensor_id = 25 #IP SENSOR
        self.server_id = 12
        self.total_pkg = total
        self.pkg_number = pkg_number

        if self.msg_type == 1 or self.msg_type == 2 :
            self.size = 0
        else :
            self.size = payload_size
        #else:
        #    self.size = b'\x00'
        self.pkg_solicitado = pacote_solicitado
        self.last_pkg = last_pkg
        self.crc8 = CRC8
        self.crc9 = CRC9
        self.head_list = []
    
    def create_head(self):
        self.head_list.append(int(self.msg_type).to_bytes(1, 'big'))
        self.head_list.append(int(self.sensor_id).to_bytes(1, 'big'))
        self.head_list.append(int(self.server_id).to_bytes(1, 'big'))
        self.head_list.append(int(self.total_pkg).to_bytes(1, 'big'))
        self.head_list.append(int(self.pkg_number).to_bytes(1, 'big'))
        self.head_list.append(int(self.size).to_bytes(1, 'big'))
        self.head_list.append(int(self.pkg_solicitado).to_bytes(1, 'big'))
        self.head_list.append(int(self.last_pkg).to_bytes(1, 'big'))
        self.head_list.append(int(self.crc8).to_bytes(1, 'big'))
        self.head_list.append(int(self.crc9).to_bytes(1, 'big'))
        self.head = b''.join(self.head_list)

        while len(self.head) != 10:
            self.head += b'\x00'

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
        self.packages = ceil(len(self.content)/114)
        return self.packages

    def packages_number(self):
        #retorna a lista dos pacotes separados
        self.n = []
        for size in range(len(self.package_size())):
            self.n.append(size + 1)
        return self.n


#ESPACO DE TESTE DAS CLASSES 

# img_path = "imgs/br_flag.png"
# with open(img_path, 'rb') as f:
#     ByteImage = f.read()

# payload = Payload(ByteImage)
# # print(payload.packages_number())
# total_pkg = payload.total_packages()
# pkgs = payload.build_package()
# print(pkgs)

# print(total_pkg)

# head = Head(1, total_pkg, 0, 0,0,0,0,0).create_head()
# eop = b'\xFF\xAA\xFF\xAA'
# t1 = head + eop

# print(f't1: {t1}')
