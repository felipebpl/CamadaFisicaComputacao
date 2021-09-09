#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from enlace import *
import time
import random
import numpy as np

serialName = "COM6"

def random_commands():
    n = random.randint(10,30)
    commands = [b'\x00\xFF',b'\x00',b'\x0F',b'\xF0',b'\xFF\x00',b'\xFF']
    commands_list = list()
    lista_semflag = []
    for i in range(n):
        comando = random.choice(commands)
        if len(comando) == 2:
            commands_list.append(b'\x02')
        commands_list.append(comando)
        lista_semflag.append(comando)
    commands_list.append(b'\x01')
    commands_list = b"".join(commands_list)
    print(commands_list)
    print(lista_semflag)
    return commands_list, lista_semflag



def main():
    try:
        com1 = enlace(serialName)
        
        com1.enable()
        
        print("----------------------------------------")
        print("Comunicação aberta com sucesso!")
        print("----------------------------------------")       
        time.sleep(1) 
        com1.sendData(b'\xaa')
        time.sleep(1)
        comandos, comandos_semflag = random_commands()

        time.sleep(1)

        txBuffer = np.asarray(comandos)
        print(len(comandos_semflag))
        

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