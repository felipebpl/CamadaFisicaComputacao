#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from enlace import *
import time
import numpy as np
from classes import Datagram,Head,Payload
import sys

img_path = "br.png"
with open(img_path, 'rb') as f:
    ByteImage = f.read()

serialName = "COM5"

def main():
    pkg = Datagram(door=serialName)
    payload = Payload(ByteImage)
    eop = b'\xFF\xAA\xFF\xAA'

    size_list= payload.package_size()
    total_pkg = payload.total_packages()
    pkg_nbr = payload.packages_number()
    pkg_list = payload.build_package()

    test_error = True
    
    try:
        
        print("----------------------------------------")
        print("Comunicação aberta com sucesso!")
        print("----------------------------------------")
        print(f'Pacotes a serem enviados: {pkg_nbr}')
        print("----------------------------------------")

        ENVIO = False
        cont = 0 
        tipo =  1

        if tipo == 1: 

            HANDSHAKE = True
            
            head = Head(tipo, total_pkg, 0, 0, 0,0,0,0).create_head()

            while HANDSHAKE:
                
                print("########## HANDSHAKE ############")

                print('Servidor pronto para receber dados?')

                timeout =  time.time() + 5

                t1 = head + eop

                print(f't1: {t1}')

                txBuffer = t1

                pkg.com1.sendData(txBuffer)

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
                            tipo = 3 
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

        if tipo == 3:
            cont = 1 
            ENVIO = True
    
            while ENVIO:
                print('# COMEÇANDO ENVIO DOS PACOTES #')
                print("----------------------------------------------------------")
                while cont <= pkg_nbr:
                    sending = True
                    while sending:
                        # def __init__(self, tipo, total, pkg_number, payload_size, pacote_solicitado, last_pkg, CRC8, CRC9):
                        head = Head(tipo, total_pkg, pkg_nbr[cont-1], size_list[cont-1], 0, 0, 0, 0).create_head()

                        print("----------------------------------------")
                        print(f'HEAD {head} ')
                        print("----------------------------------------")
                        pacote = pkg.create_datagram(head, pkg_list[cont-1][0])
                        print(f'PACOTE {cont}: {pacote} ')
                        
                        # if test_error and i==2:
                        #     #vídeo 4 -> tamanho errado = 70
                        #     headClass = Head(70, pkg_nbr[i-1], payload.total_packages())
                        #     head = headClass.create_head()
                        #     pacote = pkg.create_datagram(head, pkg_list[i-2][0])
                        #     test_error = False
                        #     print("----------------------------------------")
                        #     print("Enviou errado")
                        
                        time.sleep(0.1)
                        pkg.com1.sendData(pacote)

                        timer1 = time.time()
                        timer2 = time.time()

                        print("----------------------------------------")
                    
                        print("Pacote enviado")
                        print("----------------------------------------")

                        print("Esperando Resposta")
                        
                        head, nRx = pkg.com1.getData(10)
                        tipo = head[0]

                        if tipo == 4:
                            cont +=1
                        
                        else:
                            if timer2 > 20:
                                #envia msg tipo 5
                                #encerra com
                                pass
                            else:
                                #recebe msg
                                # pkg.com1.getData()
                                if tipo == 6:
                                    #corrige cont
                                    #envia msg tipo 3
                                    # reset timer 1 e 2
                                    pass
                                else:
                                    #volta tudo
                                    pass

                        rxBuffer, nRx = pkg.com1.getData(14)
                        # print(f'i = {i}')
                        keep = rxBuffer[3]
                        repeat = rxBuffer[4]

                        if keep == 1 and repeat == 0:
                            sending = False
                            print("----------------------------------------")
                            print("Pacote recebido.")
                            break

            print("######### FIM DE ENVIO DOS PACOTES ##########")

            pkg.com1.disable()

    except Exception as exception:
        print(exception)
        pkg.com1.disable()

if __name__ == "__main__":
    main()