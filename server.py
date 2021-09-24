from enlace import *
import time
import numpy as np
from classes import Datagram,Head,Payload
    
serialName = "COM5"

img_path = "br.png"
with open(img_path, 'rb') as f:
    ByteImage = f.read()

def c_head(keep, repeat):
    #head_list.append((self.type).to_bytes(1, 'big'))
    head_list = []
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    

    head_list.append(keep)
    head_list.append(repeat)
    head = b''.join(head_list)

    while len(head) != 10:
        head += b'\x00'

    return head

def main():
    main = True
    results = []
    id = b''
    eop = b'\xFF\xAA\xFF\xAA'
    pkg = Datagram(serialName)
    payload = Payload(ByteImage)
    
    size_list= payload.package_size()
    total_pkg = payload.total_packages()
    pkg_nbr = payload.packages_number()
    pkg_list = payload.build_package()

    try:
        packages = 255
        c = 1

        ocioso = True
        while ocioso:

            print("----------------------------------------")
            print("Servidor aberto com sucesso!")
            print("----------------------------------------")
            rxBuffer, nRx = pkg.com1.getData(14)

            if rxBuffer[2] == b'\x0c':
                print(rxBuffer)
                ocioso = False
                break

            else:
                print('Id errado')
                time.sleep(1)
                continue

        time.sleep(1)

        tipo = 2

        if tipo == 2:

            head = Head(tipo, total_pkg, 0, 0,0,0,0,0).create_head()

            pkg.com1.sendData()
        
        while c < packages:

            print("Recebendo Head")
            print("----------------------------------------")
            head, nRx = pkg.com1.getData(10)

            payload_size = head[0]
            payload_id = head[1] .to_bytes(1, 'big')
            packages = head[2]

            print("Id do pacote: "'{}'.format(payload_id))
            print("----------------------------------------")
            print("Quantidade de pacotes: "'{}'.format(packages))
            print("----------------------------------------")
            payload, nRx = pkg.com1.getData(payload_size)

            EOP, nRx = pkg.com1.getData(4)
            print(f'EOP -> {eop} == {EOP}')
            print("----------------------------------------")

            if EOP == eop:
                print("Tudo certo!")
                print("----------------------------------------")
                head = c_head(b'\x01', b'\x00')
                sendNext = pkg.create_datagram(head)
                pkg.com1.sendData(sendNext)
                results.append(payload)
                c = int.from_bytes(payload_id, "big")

            else:
                print("Erro")
                print("----------------------------------------")
                pkg.com1.rx.clearBuffer()
                head = c_head(b'\x00', b'\x01')
                reSend = pkg.create_datagram(head)
                pkg.com1.sendData(reSend)
        
        
        print("FIM")    

        all_results = b''

        for i in results:
            all_results += i

        abre = open("br.png", 'wb')
        abre.write(all_results)
        abre.close()

        pkg.com1.disable()
        

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        pkg.com1.disable()

if _name_ == "_main_":
    main()