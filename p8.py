import soundfile as sf
from funcoes_LPF import *
import sounddevice as sd
from suaBibSignal import *
from scipy import signal


def normalize(audio):
    audio[:,0] = audio[:,0]/abs(audio[:,0]).max()
    audio[:,1] = audio[:,1]/abs(audio[:,1]).max()
    return audio

def main():

    signal = signalMeu()

    data, samplerate = sf.read("audio.wav")

    normalized_audio = normalize(data)

    print(f'SampleRate: {samplerate}')
    print('-'*50)
    print(f'Data: {data}')
    print('-'*50)
    print(f'Normalized: {normalized_audio}')
    print('-'*50)

    fcutt = 4000

    filtered_audio = LPF(normalized_audio[:,0], fcutt, samplerate)

    print(f'Filtered: {filtered_audio}')
    print('-'*50)

    x1, s1 = signal.generateSin(filtered_audio, 1.5, 4, samplerate)

    sd.play(s1, samplerate)
    sd.wait()

if __name__ == "__main__":
    main()