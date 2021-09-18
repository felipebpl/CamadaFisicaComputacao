#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from numpy.core.fromnumeric import size
from enlace import *
import time
import random
import numpy as np
from classes import Datagram,Head,Payload


serialName = "COM3"     


def main():
    try:
        com1 = enlace(serialName)
        
        com1.enable()
        
        print("----------------------------------------")
        print("Comunicação aberta com sucesso!")


        time.sleep(1)

        while True:

            print("----------------------------------------")
            com1.sendData(b'Servidor pronto para receber dados?')
            
            t1 = time.time()

            tamanho, nRx = com1.getData(1)

            t2 = time.time()
            
            dif = t2 - t1

            if dif > 5:
                print("----------------------------------------")
                check = input('Servidor inativo. Tentar novamente? [Y/N]')
                print("----------------------------------------")

                if check.upper() == "Y": 
                    #go back to the top of while
                    continue    

                elif check.upper() == 'N':

                    print('Encerrando Comunicação')
                    print("----------------------------------------")
                    com1.disable()

                else:
                    print("Digite Y ou N")
                    # volta pro input

            else: 
                print('Começando o envio dos pacotes')
                print("----------------------------------------")
                False
                break
                             
                
        # if len(tamanho) > 0 :
        #     recebeu = int.from_bytes(tamanho, byteorder='big')
        #     print(recebeu)
        #     break

        img_path = 'imgs/br_flag.png'
        with open(img_path, 'rb') as f:
            ByteImage = f.read()

        payload = Payload(ByteImage)

        total_packages = payload.total_packages()
        package_size = payload.package_size()
        package_number = payload.packages_number()

        head = Head(total_packages,package_size,package_number)
        head.create_head()

        datagrama = Datagram(head,payload)
        datagrama.create_datagram()
    
        # txBuffer = np.asarray(datagrama)
        txBuffer = payload.build_package()

        com1.sendData(txBuffer)

        while True:
            tamanho, nRx = com1.getData(1)
            if len(tamanho) > 0 :
                recebeu = int.from_bytes(tamanho, byteorder='big')
                print(recebeu)
                break

        com1.disable()
    
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()