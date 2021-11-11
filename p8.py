import soundfile as sf
from funcoes_LPF import *
import sounddevice as sd
from suaBibSignal import *
from scipy import signal
import sys

def normalize(audio):
    audio[:,0] = audio[:,0]/abs(audio[:,0]).max()
    audio[:,1] = audio[:,1]/abs(audio[:,1]).max()
    return audio

def main():

    signal = signalMeu()

    data, samplerate = sf.read("audio.wav")

    normalized_audio = normalize(data)

    duration = len(normalized_audio)/samplerate

    print(f'Duração = {duration}')

    t = np.linspace(0.0, duration, len(normalized_audio))

    # tf, yf = signal.generateSin(normalized_audio, 1, 5, samplerate)

    #Gráfico 1: Sinal de áudio original normalizado – domínio do tempo
    plt.figure(figsize = (15, 10))
    plt.plot(t, normalized_audio)
    plt.title('Sinal de áudio original normalizado pelo domínio do tempo')
    plt.show()

    print(f'SampleRate: {samplerate}')
    print('-'*50)

    print(f'Data: {data}')
    print('-'*50)

    fcutt = 4000

    filtered_audio = LPF(normalized_audio[:,0], fcutt, samplerate)

    # Gráfico 2: Sinal de áudio filtrado – domínio do tempo. (repare que não se nota diferença).
    plt.figure(figsize = (15, 10))
    plt.plot(t, filtered_audio)
    plt.title('Sinal de áudio filtrado pelo domínio do tempo. ')
    plt.show() 

    signal.plotFFT(filtered_audio, samplerate, 'Sinal Filtrado')  #Gráfico 3: Sinal de áudio filtrado – domínio da frequência.  

    portadora = 14000

    tempo, amp = signal.generateSin(portadora, 1, 5, samplerate) 

    tempo = tempo[0:155232]
    amp = amp[0:155232]

    mod = amp * filtered_audio
    dmod = mod * amp

    # Gráfico 4: sinal de áudio modulado – domínio do tempo
    plt.figure(figsize = (15, 10))
    plt.plot(t, mod)
    plt.title('Sinal de áudio modulado pelo domínio do tempo ')
    plt.show() 

    signal.plotFFT(mod, samplerate, 'Sinal Modulado')  #Gráfico 5: sinal de áudio modulado – domínio da frequência

    signal.plotFFT(dmod, samplerate, 'Sinal Demodulado') #Gráfico 6: sinal de áudio demodulado – domínio da frequência

    filtered_audio2 = LPF(dmod, fcutt, samplerate) 

    signal.plotFFT(filtered_audio2, samplerate, 'Sinal Demodulado e Filtrado') #Gráfico 7: sinal de áudio demodulado e filtrado – domínio da frequência.

    # sd.play(filtered_audio2, samplerate)
    # sd.wait()

    sys.exit()

if __name__ == "__main__":
    main()