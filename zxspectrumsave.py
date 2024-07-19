import numpy as np
from scipy.io.wavfile import write
import os
#pip install numpy scipy
# Frequências usadas pelo ZX Spectrum
FREQ_0 = 1300  # Frequência para o bit 0
FREQ_1 = 2600  # Frequência para o bit 1
SAMPLING_RATE = 44100  # Taxa de amostragem para o arquivo WAV

def text_to_zx_wave(text, filename):
    def create_tone(frequency, duration):
        t = np.linspace(0, duration, int(SAMPLING_RATE * duration), endpoint=False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        return wave

    def append_bit(wave, bit):
        if bit == '0':
            return np.concatenate((wave, create_tone(FREQ_0, 1/220.0)))
        else:
            return np.concatenate((wave, create_tone(FREQ_1, 1/220.0)))
    
    # Convert text to binary representation
    binary_data = ''.join(format(ord(char), '08b') for char in text)
    
    # Add pilot tone and sync byte (not fully accurate but for demonstration)
    wave = create_tone(2000, 1.0)  # 1-second pilot tone
    wave = np.concatenate((wave, create_tone(FREQ_0, 1/220.0)))  # Sync byte (just using one '0' bit for simplicity)

    # Encode the binary data into the wave
    for bit in binary_data:
        wave = append_bit(wave, bit)
    
    # Normalize wave to int16 for WAV format
    wave = np.int16(wave * 32767)
    
    # Save to WAV file
    write(filename, SAMPLING_RATE, wave)
    print(f"File '{filename}' created successfully!")

def main():
    # Get filename from user
    input_filename = input("Enter the name of the text file: ")
    
    # Read text from file
    if not os.path.isfile(input_filename):
        print(f"File '{input_filename}' not found!")
        return
    
    with open(input_filename, 'r') as file:
        text = file.read()
    
    # Convert to ZX Spectrum WAV format and save
    output_filename = "output.wav"
    text_to_zx_wave(text, output_filename)
print("\x1bc\x1b[47;34m")
if __name__ == "__main__":
    main()

