#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import random
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

# Comandos existentes:
# Os comandos enviados devem ser uma sequência de 10 a 30 comandos. Essa sequência é construída com uma
# combinação de possíveis 6 comandos:
# Comando 1: 00FF (2 bytes)
# Comando 2: 00 (1 byte)
# Comando 3: 0F (1 byte)
# Comando 4: F0 (1 byte)
# Comando 5: FF00 (2 bytes)
# Comando 6: FF (1 bytes) 



def random_commands():
    n = random.randint(10,30)
    commands = [b'00FF',b'00',b'0F',b'F0',b'FF00',b'FF']
    commands_list = list()
    for i in range(n):
        commands_list.append(random.choice(commands))
    array_commands = np.asarray(commands_list)
    return array_commands

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("----------------------------------------")        
        print("Comunicação aberta com sucesso!")
        print("----------------------------------------")

        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.

        comandos = random_commands()
        
        txBuffer = comandos

        com1.sendData(txBuffer)

        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.

        txLen = len(txBuffer)
       
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
       
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        
        rxBuffer, nRx = com1.getData(txLen)
        print("recebeu {}" .format(rxBuffer))
            
    
        # Encerra comunicação
        print("----------------------------------------")
        print("Comunicação encerrada")
        print("----------------------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()