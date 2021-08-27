from enlace import *
import time
import random
import numpy as np


serialName = "COM4"

def main():
    com1 = enlace(serialName)

    com1.enable()



    txLen = len(txBuffer)
    rxBuffer, nRx = com1.getData(txLen)