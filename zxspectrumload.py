
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
#pip install numpy scipy matplotlib

# Frequências usadas pelo ZX Spectrum
FREQ_0 = 1300  # Frequência para o bit 0
FREQ_1 = 2600  # Frequência para o bit 1
SAMPLING_RATE = 44100  # Taxa de amostragem para o arquivo WAV

def detect_frequency(samples):
    # Calcula a FFT (Fast Fourier Transform) para detectar a frequência dominante
    fft_result = np.fft.fft(samples)
    frequencies = np.fft.fftfreq(len(samples), 1 / SAMPLING_RATE)
    peak_frequency = abs(frequencies[np.argmax(np.abs(fft_result))])
    return peak_frequency

def zx_wave_to_text(filename):
    # Ler o arquivo WAV
    sampling_rate, data = read(filename)
    data = data / 32767.0  # Normalizar para o intervalo de -1 a 1
    
    if data.ndim > 1:  # Se o áudio for estéreo, pegar apenas um canal
        data = data[:, 0]

    # Parâmetros de detecção de bits
    bit_duration = int(SAMPLING_RATE / 220.0)
    threshold = (FREQ_0 + FREQ_1) / 2.0
    
    # Detectar os bits na onda
    bits = []
    for i in range(0, len(data), bit_duration):
        bit_samples = data[i:i + bit_duration]
        if len(bit_samples) == bit_duration:
            frequency = detect_frequency(bit_samples)
            bit = '0' if frequency < threshold else '1'
            bits.append(bit)

    # Converter os bits em bytes
    binary_data = ''.join(bits)
    byte_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    
    # Convert bytes to text
    text = ''.join([chr(int(byte, 2)) for byte in byte_data if int(byte, 2) != 0])
    return text

def main():
    # Get filename from user
    input_filename = input("Enter the name of the WAV file: ")
    
    # Convert ZX Spectrum WAV format to text
    text = zx_wave_to_text(input_filename)
    
    # Print the extracted text
    print("Extracted text:")
    print(text)
print("\x1bc\x1b[47;34m")
if __name__ == "__main__":
    main()
