#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from enlace import *
import time
import random
import numpy as np
from teste import Datagram,Head,Payload

serialName = "COM3"

def main():
    try:
        com1 = enlace(serialName)
        
        com1.enable()
        
        print("----------------------------------------")
        print("Comunicação aberta com sucesso!")
        print("----------------------------------------")

        img_path = 'imgs/br_flag.png'
        with open(img_path, 'rb') as f:
            ByteImage = f.read()

        payload = Payload(ByteImage)

        total_packages = payload.total_packages()
        package_size = payload.package_size()
        package_number = payload.packages_number()

        head = Head(total=total_packages,size=package_size,pkg_number=package_number)
        head.create_head()

        datagrama = Datagram(head,payload)
        datagrama.create_datagram()
    
        # time.sleep(1) 
        # com1.sendData(b'\xaa')
        # time.sleep(1)

        txBuffer = np.asarray(datagrama)

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