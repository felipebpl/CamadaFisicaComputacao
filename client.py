#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from numpy.core.fromnumeric import size
from enlace import *
import time
import numpy as np
from classes import Datagram,Head,Payload

img_path = "br.png"
with open(img_path, 'rb') as f:
    ByteImage = f.read()

serialName = "COM3"

def main():
    pkg = Datagram(door=serialName)
    payload = Payload(ByteImage)

    size_list= payload.package_size()
    pkg_nbr = payload.packages_number()
    pkg_list = payload.build_package()
    
    try:
        
        print("----------------------------------------")
        print("Comunicação aberta com sucesso!")
        print("----------------------------------------")
        print(f'Pacotes a serem enviados: {pkg_nbr}')

        time.sleep(1)

        HANDSHAKE = True

        while HANDSHAKE:
            print("----------------------------------------")
            print("########## HANDSHAKE ############")
            print('Servidor pronto para receber dados?')

            t_max =  time.time() + 5
            head_handshake = (1).to_bytes(10, 'big')
            eop_handshake = b'\x00\x00\x00\x00'
            mensagem = head_handshake + eop_handshake
            print(f'oi {mensagem}')

            pkg.com1.sendData(mensagem)

            while time.time() < t_max:
                if pkg.com1.rx.getIsEmpty() != True:
                    rxBuffer, nrx = pkg.com1.getData(11) 
                    print('.....................................')      
                    print(f'mensagem: {mensagem} ')
                    print(f'rxBuffer: {rxBuffer} ')
                    print('.....................................')  

                    if rxBuffer == b"Funcionando":
                        print("########## HANDSHAKE FINALIZADO COM SUCESSO ############")
                        HANDSHAKE = False

                    else: 
                        print('########## HANDSHAKE FALHOU ############')
                        
            print("----------------------------------------")
            check = input('Servidor inativo. Tentar novamente? [Y/N]')
            print("----------------------------------------")

            if check.upper() == "Y": 
                #go back to the top of while
                continue    

            elif check.upper() == 'N':
                print('Encerrando Comunicação')
                print("----------------------------------------")
                pkg.com1.disable()                           

        
        print('############## COMEÇANDO ENVIO DOS PACOTES #############')
        for i in pkg_nbr:
            while True:
                print(payload.total_packages())
                print(size_list[0], pkg_nbr[0])
                headClass = Head(size_list[i-1], pkg_nbr[i-1], payload.total_packages())
                head = headClass.create_head()
                print("----------------------------------------")
                print(f'HEAD {head} ')
                print("----------------------------------------")
                pacote = pkg.create_datagram(head, pkg_list[i-1][0])
                print(F'PACOTE {pacote} ')
                
                if i==2:
                    headClass = Head(size_list[i-1], pkg_nbr[i-2], payload.total_packages())
                    head = headClass.create_head()
                    pacote = pkg.create_datagram(head, pkg_list[i-2][0])
                    False
                    print("----------------------------------------")
                    print("Enviou errado")

                time.sleep(1)
                pkg.com1.sendData(pacote)
                print("----------------------------------------")
               
                print("Pacotes enviados")
                print("----------------------------------------")

                print("Esperando Resposta")
                rxBuffer, nRx = pkg.com1.getData(14)
                print("----------------------------------------")
                print(rxBuffer)
                print("----------------------------------------")
                print(f'i = {i}')
                keep = rxBuffer[3]
                repeat = rxBuffer[4]

                if keep == 1 and repeat == 0:
                    False
                    print("----------------------------------------")
                    print("Recebi para continuar")
        print("----------------------------------------")    
        print("Enviei Tudo")
        print("----------------------------------------")
    except Exception as exception:
        print(exception)
        pkg.com1.disable()

if __name__ == "__main__":
    main()