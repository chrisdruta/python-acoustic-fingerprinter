#!/bin/python
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile

fs, data = wavfile.read('spacejam.wav')
leftChannelData = data[:, 0]
print(np.amax(leftChannelData))

f, t, spectogramX = signal.spectrogram(leftChannelData, fs)

plt.pcolormesh(t, f, spectogramX)
#plt.imshow(spectogramX)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
