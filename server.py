from enlace import *
import time
import random
import numpy as np


serialName = "COM4"

def main():
    try:


        while True:

            com1 = enlace(serialName)

            com1.enable()

            txBuffer = com1.rx.getBufferLen()
            
            txLen = len(txBuffer)
            
            rxBuffer, nRx = com1.getData(txLen)

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()