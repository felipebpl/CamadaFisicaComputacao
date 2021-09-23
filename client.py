#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from numpy.core.fromnumeric import size
from enlace import *
import time
import numpy as np
from classes import Datagram,Head,Payload
import sys

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

    test_error = True
    
    try:
        
        print("----------------------------------------")
        print("Comunicação aberta com sucesso!")
        print("----------------------------------------")
        print(f'Pacotes a serem enviados: {pkg_nbr}')
        print("----------------------------------------")

        HANDSHAKE = True

        while HANDSHAKE:
            
            print("########## HANDSHAKE ############")

            print('Servidor pronto para receber dados?')

            timeout =  time.time() + 5

            handshake = b'\x01'*14

            txBuffer = handshake

            pkg.com1.sendData(txBuffer)
            # rxBuffer, nRx = pkg.com1.getData(14)

            # if rxBuffer == txBuffer:
            #     print("----------------------------------------")
            #     print('Servidor pronto !')
            #     print("----------------------------------------------------------")
            #     print("# HANDSHAKE FINALIZADO COM SUCESSO #")
            #     print("----------------------------------------")
            #     HANDSHAKE = False

            while time.time() < timeout:

                if pkg.com1.rx.getIsEmpty() != True:
                    rxBuffer, nrx = pkg.com1.getData(14) 
                    print('.....................................')      
                    print(f'rxBuffer: {rxBuffer} ')
                    print('.....................................')  

                    if rxBuffer == txBuffer:
                        print("----------------------------------------")
                        print('Servidor pronto !')
                        print("----------------------------------------------------------")
                        print("# HANDSHAKE FEITO COM SUCESSO #")
                        print("----------------------------------------")
                        HANDSHAKE = False
                        break

            if HANDSHAKE:
                print("----------------------------------------")
                check = input('Servidor inativo. Tentar novamente? [Y/N]')
                print("----------------------------------------")
                if check.upper() == "Y": 
                    print("Rodando servidor novamente")
                    continue
                #go back to the top of while 
                elif check.upper() == 'N':
                    print('Encerrando Comunicação')
                    print("----------------------------------------")
                    pkg.com1.disable()
                    sys.exit()
            else:
                pass

            print('# COMEÇANDO ENVIO DOS PACOTES #')
            print("----------------------------------------------------------")
            for i in pkg_nbr:
                sending = True
                while sending:
                    # print(payload.total_packages())
                    # print(size_list[0], pkg_nbr[0])
                    headClass = Head(size_list[i-1], pkg_nbr[i-1], payload.total_packages())
                    head = headClass.create_head()
                    print("----------------------------------------")
                    print(f'HEAD {head} ')
                    print("----------------------------------------")
                    pacote = pkg.create_datagram(head, pkg_list[i-1][0])
                    print(f'PACOTE {i}: {pacote} ')
                    
                    # if test_error and i==2:
                    #     headClass = Head(size_list[i-1], pkg_nbr[i-2], payload.total_packages())
                    #     #para testar o item 4, basta mudar o primeiro argumento do Head para um numero diferente de 114
                    #     head = headClass.create_head()
                    #     pacote = pkg.create_datagram(head, pkg_list[i-2][0])
                    #     test_error = False
                    #     print("----------------------------------------")
                    #     print("Enviou errado")
                        

                    time.sleep(0.1)
                    pkg.com1.sendData(pacote)
                    print("----------------------------------------")
                
                    print("Pacote enviado")
                    print("----------------------------------------")

                    print("Esperando Resposta")
                    rxBuffer, nRx = pkg.com1.getData(14)
                    # print(f'i = {i}')
                    keep = rxBuffer[3]
                    repeat = rxBuffer[4]

                    if keep == 1 and repeat == 0:
                        sending = False
                        print("----------------------------------------")
                        print("Pacote recebido.")

            print("######### FIM DE ENVIO DOS PACOTES ##########")

            pkg.com1.disable()

    except Exception as exception:
        print(exception)
        pkg.com1.disable()

if __name__ == "__main__":
    main()