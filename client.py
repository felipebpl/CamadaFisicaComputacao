#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

from math import log
from enlace import *
import time
from classes import Datagram,Head,Payload
import sys
from Log import Log
import traceback as tb

img_path = "imgs/br_flag.png"
with open(img_path, 'rb') as f:
    ByteImage = f.read()

serialName = "COM3"

def main():
    pkg = Datagram(door=serialName)
    payload = Payload(ByteImage)
    eop = b'\xFF\xAA\xFF\xAA'

    size_list= payload.package_size()
    total_pkg = payload.total_packages()
    pkg_nbr = payload.packages_number()
    pkg_list = payload.build_package()

    # pkg.com1.fisica.flush()

    try:
        
        print("----------------------------------------")
        print("Comunicação aberta com sucesso!")
        print("----------------------------------------")
        print(f'Pacotes a serem enviados: {pkg_nbr}')
        print("----------------------------------------")

        cont = 0 
        tipo =  1

        if tipo == 1: 

            HANDSHAKE = True
            
            head = Head(tipo, total_pkg, 0, 0, 0,0,0,0).create_head()

            while HANDSHAKE:
                
                print("########## HANDSHAKE ############")

                print('Servidor pronto para receber dados?')

                timeout =  time.time() + 5

                t1 = head + eop

                print('.....................................')      
                print(f'Mensagem t1: {t1}')
                
                pkg.com1.sendData(t1)

                log_t1 = Log(t1,'envio')
                t1_msg = log_t1.create_log()
                log_t1.write_log(t1_msg, "Client1.txt")

                while time.time() < timeout:

                    if pkg.com1.rx.getIsEmpty() != True:
                        rxBuffer, nrx = pkg.com1.getData(14) 
                        t2 = rxBuffer
                        log_t2 = Log(t2,'receb')
                        t2_msg = log_t2.create_log()
                        log_t2.write_log(t2_msg, "Client1.txt")

                        print('.....................................')      
                        print(f'Mensagem t2: {rxBuffer} ')
                        print('.....................................')    

                        if rxBuffer[1] == 25:
                            print("----------------------------------------")
                            print("ID CORRETO !")
                            print("----------------------------------------")
                            print('Servidor pronto !')
                            print("----------------------------------------------------------")
                            print("# HANDSHAKE FEITO COM SUCESSO #")
                            print("----------------------------------------")
                            HANDSHAKE = False
                            tipo = 3 
                            break

                if HANDSHAKE:
                    print("----------------------------------------")
                    check = input('Servidor inativo. Tentar novamente? [Y/N]') 
                    print("----------------------------------------")
                    if check.upper() == "Y": 
                        print("Rodando servidor novamente")
                        #go back to the top of while
                        continue
                     
                    elif check.upper() == 'N':
                        print('Encerrando Comunicação')
                        print("----------------------------------------")
                        pkg.com1.disable()
                        sys.exit()
                else:
                    pass


        cont = 1
        print('# COMEÇANDO ENVIO DOS PACOTES #')
        print("----------------------------------------------------------")

        while cont <= total_pkg:   

            timer1 = time.time()
                          
            #(tipo, total, pkg_number, payload_size, pacote_solicitado, last_pkg, CRC8, CRC9):
            head = Head(3, total_pkg, pkg_nbr[cont-1], size_list[cont-1], 0, 0, 0, 0).create_head()
            pacote = pkg.create_datagram(head, pkg_list[cont-1][0])

            print(f'PACOTE {cont}: {pacote} ')
            print("----------------------------------------------------------")
            time.sleep(1)
            pkg.com1.sendData(pacote)

            log_t3 = Log(head,'envio')
            t3_msg = log_t3.create_log()
            log_t3.write_log(t3_msg, "Client1.txt")

            print(f"CONT: {cont}")
            print("----------------------------------------")

            print("Pacote enviado")
            print("----------------------------------------")

            print("Esperando Resposta")
            print("----------------------------------------")
                                
            rxBuffer, nRx = pkg.com1.getData(14)
            
            t3_response = rxBuffer
            tipo_response = rxBuffer[0]

            print(f'%%%%%% RX BUFFER = {rxBuffer} %%%%%%%')
            print(f"****** TIPO RESPONSE = {tipo_response} ********")

            log_t3_response = Log(t3_response,'receb')
            t3_response_msg = log_t3_response.create_log()
            log_t3_response.write_log(t3_response_msg, "Client1.txt")
            
            if tipo_response == 4:
                print(f"Tipo : {tipo_response}")
                print("----------------------------------------")
                print(f"Pacote {cont} recebido com SUCESSO!")
                print("----------------------------------------")
                cont += 1
                continue
                timer1 = time.time()

            # else:
            #     print(f"****** TIPO RESPONSE ERRADO = {tipo_response} ********")

            # else: 
            #     if rxBuffer == "REENVIE":
            #         print(f'Se passaram 5 segundos, envio o pacote {cont} novamente')
            #         print("----------------------------------------------------------")
            #         pkg.com1.sendData(pacote)

            #         log_t3 = Log(head,'envio')
            #         t3_msg = log_t3.create_log()
            #         log_t3.write_log(t3_msg, "Client1.txt")
            #         pkg.com1.clearBuffer()

            #     else: 
            #         if rxBuffer == "TIMEOUT":
            #             print(f'if timeout , rxBuffer {rxBuffer[0]} =  tipo response {tipo_response}')
            #             print('[][]*15')
            #             print(f'######### TIMEOUT #########')
            #             print("----------------------------------------------------------")
            #             print(f'Se passaram 20 segundos, encerrando comunicacao')
            #             print("----------------------------------------------------------")

            #             head_t5 = Head(5, total_pkg, pkg_nbr[cont-1], size_list[cont-1], 0, rxBuffer[6], 0, 0).create_head()
            #             pacote_t5 = pkg.create_datagram(head_t5, pkg_list[cont-1][0])
            #             time.sleep(1)
            #             pkg.com1.sendData(pacote_t5)

            #             log_t5 = Log(head_t5,'envio')
            #             t5_msg = log_t5.create_log()
            #             log_t5.write_log(t5_msg, "Client1.txt")

            #             pkg.com1.disable()

            #         else:
            #             print(f'ultimo else , rxBuffer {rxBuffer[0]} =  tipo response {tipo_response}')
            #             tipo_response = 6 
            #             cont = rxBuffer[6]
            #             head_t6 = Head(tipo_response, total_pkg, pkg_nbr[cont-1], size_list[cont-1], 0, rxBuffer[6], 0, 0).create_head()
            #             pacote_t6 = pkg.create_datagram(head_t6, pkg_list[cont-1][0])

            #             print("----------------------------------------------------------")
            #             print(f'REENVIANDO PACOTE {cont}')
            #             time.sleep(1)
            #             pkg.com1.sendData(pacote_t6)
            #             print("----------------------------------------------------------")

            #             log_t6 = Log(head_t6,'envio')
            #             t6_msg = log_t6.create_log()
            #             log_t6.write_log(t6_msg, "Client1.txt")
            #             timer1 = time.time()
                            

        print("######### FIM DE ENVIO DOS PACOTES ##########")
        pkg.com1.disable()
        sys.exit()

    except Exception as exception:
        print(tb.format_exc())
        print(exception, '<- ERRO')
        pkg.com1.disable()

if __name__ == "__main__":
    main()