from enlace import *
import time
import random
import numpy as np
import client


serialName = "COM4"

def main():
    try:
        com1 = enlace(serialName)

        com1.enable()

        print("----------------------------------------")
        print("Servidor aberto com sucesso!")
        print("----------------------------------------")

        while True:

            txBuffer = com1.rx.getBufferLen()

            #txLen = len(txBuffer)

            rxBuffer, nRx = com1.getData(txBuffer)

        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()