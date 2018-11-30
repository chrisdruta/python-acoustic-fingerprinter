#!/bin/python
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile

fs, data = wavfile.read('spacejam.wav')
monoChannelData = data[:, 0] # Left channel
monoChannelData = monoChannelData[int(9696120/2):int((9696120/2 + 5*44100))]

f, t, spectogramX = signal.spectrogram(monoChannelData, fs)
spectogramX = 20 * np.log10(spectogramX)
spectogramX[spectogramX == -np.inf] = 0

numFreqBins, numSamples = spectogramX.shape
print(numFreqBins, numSamples)

freqsAt0 = spectogramX[:,0]
noise = np.random.normal(60,5,len(freqsAt0))

freqsAt0Noise = freqsAt0 + noise
#wc = 2 * np.pi * 21000 / fs
#r = 10
#b = [1, -r*(np.e**(1j*wc) + np.e**(-1j*wc)), r**2]
#a = [-1, 0, -1]

#noise = np.abs(signal.lfilter(b, a, noise))

ind = signal.find_peaks(freqsAt0)[0]
#ind = signal.find_peaks_cwt(freqsAt0, np.arange(1,10))

if 1:
    plt.figure()
    plt.title('DTFT of mono channel Space Jam at t=0')
    plt.plot(f, freqsAt0)
    plt.stem(f[ind],freqsAt0[ind], linefmt=':', basefmt=' ')
    #plt.stem(f, noise)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('dB')

if 0:
    plt.figure()
    plt.pcolormesh(t, f, spectogramX)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()

plt.show()
