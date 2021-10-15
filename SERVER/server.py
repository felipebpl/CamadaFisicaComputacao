from enlace import *
import time
from classes import Datagram,Head,Payload
from Log import Log
import sys
import traceback as tb

serialName = "COM4"

img_path = "imgs/br_flag.png"
with open(img_path, 'rb') as f:
    ByteImage = f.read()

def main():
    results = []
    eop = b'\xFF\xAA\xFF\xAA'
    pkg = Datagram(serialName)
    payload = Payload(ByteImage)
    
    total_pkg = payload.total_packages()
    pkg_nbr = payload.packages_number()
    pkg_list = payload.build_package()

    # pkg.com1.fisica.flush()

    try:
        packages = 255
        c = 1

        ocioso = True
        while ocioso:
            print("----------------------------------------")
            print("Servidor aberto com sucesso!")
            print("----------------------------------------")
            rxBuffer, nRx = pkg.com1.getData(14)

            t1 = rxBuffer
            log_t1 = Log(t1,'receb')
            t1_msg = log_t1.create_log()
            log_t1.write_log(t1_msg, "SERVER/logs/Server1.txt")

            print('ID: ', rxBuffer[2])

            if rxBuffer[2] == 12:
                print("----------------------------------------")
                print("ID CORRETO !")
                print("----------------------------------------")
                ocioso = False
                break

            else:
                print("----------------------------------------")
                print('ID ERRADO !')
                print("----------------------------------------")
                time.sleep(1)
                continue

        time.sleep(1)
        
        head_t2 = Head(2, total_pkg, 0, 0,0,0,0,0).create_head()
        t2 = head_t2 + eop
        pkg.com1.sendData(t2)

        log_t2 = Log(t2,'envio')
        t2_msg = log_t2.create_log()
        log_t2.write_log(t2_msg, "SERVER/logs/Server1.txt")


        timer = time.time()
        while c <= total_pkg:

            head, nRx = pkg.com1.getData(10)

            t3 = head
            log_t3 = Log(t3,'receb')
            t3_msg = log_t3.create_log()
            log_t3.write_log(t3_msg, "SERVER/logs/Server1.txt")

            msg_type = head[0]

            if msg_type == 3:

                payload_size = head[5]
                payload_id = head[4]
                packages = head[3]
                crc = head[8:10]

                print("Tipo do pacote: "'{}'.format(msg_type))
                print("----------------------------------------")
                print("Tamanho do payload: "'{}'.format(payload_size))
                print("----------------------------------------")
                print("Quantidade de pacotes: "'{}'.format(packages))
                print("----------------------------------------")
                print("CRC: "'{}'.format(crc))
                print("----------------------------------------")

                payload, nRx = pkg.com1.getData(payload_size)

                results.append(payload)

                eop, nRx = pkg.com1.getData(4)
            
                if eop == b'\xFF\xAA\xFF\xAA' and payload_id == c: 

                    print(f"Tudo Certo -> EOP {eop} // payload_id {payload_id} = c {c}")

                    print(f'ULTIMO PACOTE RECEBIDO = {payload_id} COM SUCESSO')
                    print("----------------------------------------")

                    head_t4 = Head(4, total_pkg, c, payload_size, 0, payload_id, 0,0).create_head()

                    t4 = head_t4 + eop
        
                    pkg.com1.sendData(t4)

                    log_t4 = Log(head_t4,'envio')
                    t4_msg = log_t4.create_log()
                    log_t4.write_log(t4_msg, "SERVER/logs/Server1.txt")
                    c += 1 
                
                else:
                    print(f'ERRO NO PACOTE {c}')
                    print("----------------------------------------")

                    head_t6 = Head(6, total_pkg, c, payload_size, 0, payload_id, 0,0).create_head()
                    # pacote = pkg.create_datagram(head_t6, pkg_list[c-1][0])
                    # pkg.com1.sendData(pacote)

                    t6 = head_t4 + eop

                    pkg.com1.sendData(t6)

                    log_t6 = Log(head_t6,'envio')
                    t6_msg = log_t6.create_log()
                    log_t6.write_log(t6_msg, "SERVER/logs/Server1.txt")

            else:

                time.sleep(1)

                if time.time() - timer > 20:
                    print(f'TIMEOUT')
                    print("----------------------------------------")

                    # ocioso = True 
                    head_t5 = Head(5, total_pkg, c, payload_size, 0, payload_id, 0,0).create_head()
                    # pacote = pkg.create_datagram(head_t5, pkg_list[c-1][0])
                    # pkg.com1.sendData(pacote)

                    t5 = head_t5 + eop

                    pkg.com1.sendData(t5)

                    log_t5 = Log(head_t5,'envio')
                    t5_msg = log_t5.create_log()
                    log_t5.write_log(t5_msg, "SERVER/logs/Server1.txt")

                    print("########## ENCERRANDO COMUNICAÇÃO ###########")
                    pkg.com1.disable()
                    sys.exit()


                else:

                    if rxBuffer == "REENVIE":
                        last_pkg = payload_id
                        print(f'ULTIMO PACOTE RECEBIDO = {last_pkg} COM SUCESSO')
                        print("----------------------------------------")

                        head_t4 = Head(4, total_pkg, c, payload_size, 0, last_pkg, 0,0).create_head()
                        
                        t4 = head_t4 + eop 
            
                        pkg.com1.sendData(t4)

                        log_t4 = Log(head_t4,'envio')
                        t4_msg = log_t4.create_log()
                        log_t4.write_log(t4_msg, "SERVER/logs/Server1.txt")
                        timer = time.time()

                    
        print("FIM DE ENVIO DOS PACOTES")    

        all_results = b''

        for i in results:
            all_results += i

        print(all_results)

        abre = open("imgs/br_flag_written.png", 'wb')
        abre.write(all_results)
        abre.close()

        pkg.com1.disable()
        

    except Exception as erro:
        print(tb.format_exc())
        print("ops! :-\\")
        print(erro)
        pkg.com1.disable()

if __name__ == "__main__":
    main()