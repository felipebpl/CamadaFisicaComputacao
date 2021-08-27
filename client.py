#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from enlace import *
import time
import random
import numpy as np

serialName = "COM4"

def random_commands():
    print("oi")
    n = random.randint(10,30)
    commands = [b'00FF',b'00',b'0F',b'F0',b'FF00',b'FF']
    commands_list = list()
    for i in range(n):
        commands_list.append(random.choice(commands))
    array_commands = np.asarray(commands_list)
    print(array_commands)
    return array_commands

def main():
    try:
        com1 = enlace(serialName)
        
        com1.enable()
        
        print("----------------------------------------")
        print("Comunicação aberta com sucesso!")
        print("----------------------------------------")
        
        comandos = random_commands()
        print("oi")
        print(comandos)
        txBuffer = comandos

        com1.sendData(txBuffer)

    
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()