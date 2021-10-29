#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas

import numpy as np
from numpy.lib.function_base import append
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import sys
from suaBibSignal import *
import peakutils


# funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def getTecla(picos):

    if int(picos[0]) == 697:
        if int(picos[1]) == 1209:
            return '1'
        elif int(picos[1]) == 1336:
            return '2'
        elif int(picos[1]) == 1477:
            return '3'

    elif int(picos[0]) == 770:
        if int(picos[1]) ==1209 :
            return '4'
        elif int(picos[1]) == 1336:
            return '5'
        elif int(picos[1]) == 1477:
            return '6'

    elif int(picos[0]) == 852:
        if int(picos[1]) ==1209 :
            return '7'
        elif int(picos[1]) == 1336:
            return '8'
        elif int(picos[1]) == 1477:
            return '9'
    elif int(picos[0]) == 941:
        return '0'

    else:
        print('ERRO')




def main():

    sinal = signalMeu()

    # declare um objeto da classe da sua biblioteca de apoio (cedida)
    # declare uma variavel com a frequencia de amostragem, sendo 44100

    # voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:

    fs = 44100

    sd.default.samplerate = fs  # taxa de amostragem
    sd.default.channels = 2  # voce pode ter que alterar isso dependendo da sua placa

    duration = 5  # tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao
    # use um time.sleep para a espera

   # faca um print informando que a gravacao foi inicializada

   # declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ...
   # calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)

    numAmostras = duration * fs
    audio = sd.rec(int(numAmostras), samplerate=fs, channels=2)

    print('INICANDO GRAVAÇÃO')
    sd.wait()
    print("...     FIM")

    # analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    # grave uma variavel com apenas a parte que interessa (dados)

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    # t = np.linspace(inicio,fim,numPontos)
    t = np.linspace(-duration/2, duration/2, duration*fs)

    # plot do gravico  áudio vs tempo!

    yAudio = audio[:, 1]

    # yAudio2 = yAudio[0]

    samplesAudio = len(yAudio)

    print(yAudio,  samplesAudio)

    xf, yf = sinal.calcFFT(yAudio, fs)

    index = peakutils.indexes(np.abs(yf), thres=0.4, min_dist=10)

    print("index de picos {}" .format(index))

    pico_freqs = []

    for freq in xf[index]:
        print("freq de pico sao {}" .format(freq))
        pico_freqs.append(freq)

    print(pico_freqs)


    tecla_apertada = getTecla(pico_freqs)

    print(tecla_apertada)

    print(f'A TECLA APERTADA FOI {tecla_apertada}')

    # Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias

    plt.figure("F(y)")
    plt.plot(xf, np.abs(yf))
    plt.grid()
    plt.title('Fourier audio')

    plt.figure('tempo x sinal')
    plt.plot(t, yAudio)
    plt.grid()
    plt.title('Gráfico no tempo do sinal recebido')
    plt.show()

    sys.exit()

    # esta funcao analisa o fourier e encontra os picos
    # voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    # voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    # frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.

    # printe os picos encontrados!

    # encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    # print a tecla.

    # Exibe gráficos
if __name__ == "__main__":
    main()