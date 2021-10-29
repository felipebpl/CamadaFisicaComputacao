import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import sys
from suaBibSignal import *
#importe as bibliotecas


def get_freqs_from_dict(dict, chave):
    
    freq1 = dict[f'{chave}'][0] 
    freq2 = dict[f'{chave}'][1] 

    return freq1, freq2


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100

    signal = signalMeu()
    fs = 44100        

    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    
    duration = 4
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array

    dic = {
        '0':[941, 1336],
        '1':[697, 1209], 
        '2':[697, 1336], 
        '3':[697, 1477], 
        '4':[770, 1209], 
        '5':[770, 1336],
        '6':[770, 1477], 
        '7':[852, 1209], 
        '8':[852, 1336], 
        '9':[852, 1477]
    }

    A = 1.5
    t   = np.linspace(-duration/2,duration/2,duration*fs)

    tecla = input('Digite uma tecla de 0 a 9: ')

    f1,f2 = get_freqs_from_dict(dic, tecla)

    x1, s1 = signal.generateSin(f1, A, duration, fs)
    x2, s2 = signal.generateSin(f2, A, duration, fs)



    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    print("Gerando Tom referente ao símbolo : {}".format(tecla))
    
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    
    tone = s1+s2

    y = s1 + s2
    plt.plot(t, y)
    plt.xlim(0,0.01)
    X, Y = signal.calcFFT(y,fs)
    plt.figure()
    plt.stem(X,np.abs(Y))
    plt.xlim(0,2500)
    #printe o grafico no tempo do sinal a ser reproduzido
    # reproduz o som
    sd.play(tone, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()