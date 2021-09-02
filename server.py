from enlace import *
import time
import random
import numpy as np
import client


serialName = "COM5"

def main():
    try:
        com1 = enlace(serialName)

        com1.enable()

        print("----------------------------------------")
        print("Servidor aberto com sucesso!")
        print("----------------------------------------")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer
        
        lista_servidor = []

        while True:

            rxBuffer, nRx = com1.getData(1)
            
            if rxBuffer == b'\x02':
                rxBuffer, nRx = com1.getData(2)

            lista_servidor.append(rxBuffer)
            if rxBuffer == b'\x01':
                break

        com1.disable

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()