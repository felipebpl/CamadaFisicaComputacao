from enlace import *
import time
import numpy as np
from classes import Datagram,Head,Payload
    
serialName = "COM1"

def create_head(self, keep, repeat):
    #head_list.append((self.type).to_bytes(1, 'big'))
    head_list = []
    head_list.append(int(self.total).to_bytes(1, 'big'))
    head_list.append(int(self.size).to_bytes(1, 'big'))
    head_list.append(int(self.pkg_number).to_bytes(1, 'big'))
    head_list.append(keep)
    head_list.append(repeat)
    head = b''.join(head_list)

    while len(head) <= 10:
        head += b'\xFF'

    return head

def main():
    results = []
    id = b''
    datagram = Datagram(serialName)

    try:
        packages = 255
        c = 1

        handshake = True
        while handshake:

            print("----------------------------------------")
            print("Servidor aberto com sucesso!")
            print("----------------------------------------")
            rxBuffer, nRx = datagram.com1.getData(1)

            time.sleep(1) 
            datagram.com1.sendData(b'Funcionando')
            time.sleep(1)
            datagram.com1.rx.clearBuffer()

            handshake = False

        while True:

            rxBuffer, nRx = datagram.com1.getData(1)

            while c < packages:

                print("Recebendo Head")
                
                head, nRx = datagram.com1.getData(10)
                payload_size = head[0]
                payload_id = head[1] .to_bytes(1, 'big')
                package_nbr = head[2]

                print("Id do pacote: "'{}'.format(payload_id))
                print("Quantidade de pacotes: "'{}'.format(package_nbr))
                payload, payloadSize = datagram.com1.getData(payload_size)

                EOP, nRx = datagram.com1.getData(4)
                if EOP == b'\x00\x00\x00\x00':
                    print("Tudo certo!")
                    head = create_head(b'\x01', b'\x00')
                    sendNext = datagram.create_datagram(head)
                    datagram.com1.sendData(sendNext)
                    results.append(payload)
                    c = int.from_bytes(payload_id, "big")

                else:
                    print("Erro")
                    datagram.com1.rx.clearBuffer()
                    head = create_head(b'\x00', b'\x01')
                    reSend = datagram.create_datagram(head)
                    datagram.com1.sendData(reSend)
            
            
            print("Fim")    

            all_results = b''

            for i in results:
                all_results += i

            abre = open("br.png", 'wb')
            abre.write(all_results)
            abre.close
            

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        datagram.com1.disable()

if __name__ == "__main__":
    main()