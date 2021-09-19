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

serialName = "COM6"

def main():
    pkg = Datagram(door=serialName)
    payload = Payload(ByteImage)

    size_list= payload.package_size()
    pkg_nbr = payload.packages_number()
    pkg_list = payload.build_package()

    print("oi")
    
    try:
        
        print("----------------------------------------")
        print("Comunicação aberta com sucesso!")

        print(pkg_nbr)


        time.sleep(1)

        while True:

            print("----------------------------------------")
            pkg.com1.sendData(b'Servidor pronto para receber dados?')
            
            t1 = time.time()
            tamanho, nRx = pkg.com1.getData(1)
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
                    pkg.com1.disable()

                else:
                    print("Digite Y ou N")
                    # volta pro input

            else: 
                print('Começando o envio dos pacotes')
                print("----------------------------------------")
                False         
                break                    
        
        for i in pkg_nbr:
            while True:
                print("oi1")
                headClass = Head(size_list[i-1], pkg_nbr[i-1], total=payload.total_packages())
                head = headClass.create_head()
                pacote = pkg.create_datagram(head, pkg_list[i-1][0])
                print("oi2")

                if error and i==2:
                    headClass = Head(size_list[i-1], pkg_nbr[i-2], total=payload.total_packages())
                    head = headClass.create_head()
                    pacote = pkg.create_datagram(head, pkg_list[i-2][0])
                    error = False
                    print("erro")


                #print(pacote)
                time.sleep(0.1)
                print("oi1")
                pkg.com1.sendData(pacote)
                print("Pacotes enviados")

                print("Esperando Resposta")
                rxBuffer, nRx = pkg.com1.getData(14)
                print(rxBuffer)
                print(i)
                keep = rxBuffer[3]
                repeat = rxBuffer[4]

                if keep == 1 and repeat == 0:
                    False
                    print("Recebi para continuar")
            
        print("Enviei Tudo")
    except Exception as exception:
        print(exception)
        pkg.com1.disable()

if __name__ == "__main__":
    main()