from enlace import *
import time
import numpy as np
from classes import Datagram,Head,Payload
    
serialName = "COM5"

def c_head(keep, repeat):
    #head_list.append((self.type).to_bytes(1, 'big'))
    head_list = []
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(int(0).to_bytes(1, 'big'))
    head_list.append(keep)
    head_list.append(repeat)
    head = b''.join(head_list)

    while len(head) != 10:
        head += b'\xaa'

    return head

def main():
    main = True
    results = []
    id = b''
    eop = b'\x00\x00\x00\x00'
    datagram = Datagram(serialName)

    try:
        packages = 255
        c = 1

        print("----------------------------------------")
        print("Servidor aberto com sucesso!")
        print("----------------------------------------")
        rxBuffer, nRx = datagram.com1.getData(14)

        time.sleep(1) 
        datagram.com1.sendData(rxBuffer)
        
        print("Funcionando")
        print("----------------------------------------")
        time.sleep(1)
        datagram.com1.rx.clearBuffer()

        while c < packages:

            print("Recebendo Head")
            print("----------------------------------------")
            head, nRx = datagram.com1.getData(10)

            payload_size = head[0]
            payload_id = head[1] .to_bytes(1, 'big')
            package_nbr = head[2]

            print("Id do pacote: "'{}'.format(payload_id))
            print("----------------------------------------")
            print("Quantidade de pacotes: "'{}'.format(package_nbr))
            print("----------------------------------------")
            payload, nRx = datagram.com1.getData(payload_size)

            EOP, nRx = datagram.com1.getData(4)
            print(f'EOP -> {eop} == {EOP}')
            print("----------------------------------------")

            if EOP == eop:
                print("Tudo certo!")
                print("----------------------------------------")
                k = b'\x01'
                r = b'\x00'
                head = c_head(k , r)
                sendNext = datagram.create_datagram(head)
                datagram.com1.sendData(sendNext)
                results.append(payload)
                c = int.from_bytes(payload_id, "big")

            else:
                print("Erro")
                print("----------------------------------------")
                datagram.com1.rx.clearBuffer()
                k = b'\x00'
                r = b'\x01'
                head = c_head(keep=k,repeat=r)
                reSend = datagram.create_datagram(head)
                datagram.com1.sendData(reSend)
        
        
        print("FIM")    

        all_results = b''

        for i in results:
            all_results += i

        abre = open("br.png", 'wb')
        abre.write(all_results)
        abre.close()

        datagram.com1.disable()
            

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        datagram.com1.disable()

if __name__ == "__main__":
    main()