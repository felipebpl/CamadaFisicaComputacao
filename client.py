#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from enlace import *
import time
import random
import numpy as np

serialName = "COM5"

def random_commands():
    n = random.randint(10,30)
    commands = [b'\x00\xFF',b'\x00',b'\x0F',b'\xF0',b'\xFF\x00',b'\xFF']
    commands_list = list()
    for i in range(n):
        comando = random.choice(commands)
        if len(comando) == 2:
            commands_list.append(b'\x02')
        commands_list.append(comando)
    commands_list.append(b'\x01')
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
        time.sleep(1)
        com1.sendData(b'\xaa')

        comandos = random_commands()

        txBuffer = comandos

        com1.sendData(txBuffer)
        com1.disable()

    
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()