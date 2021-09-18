from enlace import *
import time
import random
import numpy as np
import client
from classes import Datagram,Head,Payload,Handshake
    
serialName = "COM3"

def main():
    try:
        com1 = enlace(serialName)

        com1.enable()

        print("----------------------------------------")
        print("Servidor aberto com sucesso!")
        print("----------------------------------------")
        rxBuffer, nRx = com1.getData(1)

        time.sleep(1) 
        print("----------------------------------------")
        com1.sendData('Sim, manda papi')
        print("----------------------------------------")
        time.sleep(1)
        com1.rx.clearBuffer()
        

        while True:

            rxBuffer, nRx = com1.getData(1)
    
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()