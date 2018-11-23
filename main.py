#!/bin/python
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile

fs, data = wavfile.read('spacejam.wav')
leftChannelData = data[:, 0]

f, t, spectogramX = signal.spectrogram(leftChannelData, fs)
spectogramX = 20 * np.log10(spectogramX)
spectogramX[spectogramX == -np.inf] = 0
print(np.shape(spectogramX))

if 1:
    plt.pcolormesh(t, f, spectogramX)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()
    plt.show()
