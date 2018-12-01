#!/bin/python
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile

import sounddevice as sd
sd.default.device = 7

clipDuration = 5

fs, cleanData = wavfile.read('spacejam.wav')
cleanData = cleanData[:, 0] # Left channel
cleanData = cleanData[int(len(cleanData)/2):int(len(cleanData)/2 + clipDuration * fs)]

noise = wavfile.read('noise.wav')[1]
noise = noise[int(len(noise)/2): int(len(noise)/2) + clipDuration * fs]

dirtyData = cleanData * 0.1 + noise * 1.5
dirtyData = dirtyData.astype(np.int16)
#sd.play(dirtyData, fs)

fxClean, txClean, spectogramClean = signal.spectrogram(cleanData, fs)
spectogramClean[spectogramClean == -np.inf] = 0
spectogramClean = 20 * np.log10(spectogramClean)

fxDirty, txDirty, spectogramDirty = signal.spectrogram(dirtyData, fs)
spectogramDirty[spectogramDirty == -np.inf] = 0
spectogramDirty = 20 * np.log10(spectogramDirty)

freqsAt0Clean = spectogramClean[:,0]
freqsAt0Dirty = spectogramDirty[:,0]

indClean = signal.find_peaks(freqsAt0Clean)[0]
indDirty = signal.find_peaks(freqsAt0Dirty)[0]
#ind = signal.find_peaks_cwt(freqsAt0, np.arange(1,10))

if 1:
    plt.figure()

    plt.subplot(211)
    plt.plot(fxClean, freqsAt0Clean)
    plt.stem(fxClean[indClean],freqsAt0Clean[indClean], linefmt=':', basefmt=' ')
    plt.title('DTFT Clean t=0')

    plt.subplot(212)
    plt.plot(fxDirty, freqsAt0Dirty)
    plt.stem(fxDirty[indDirty],freqsAt0Dirty[indDirty], linefmt=':', basefmt=' ')
    plt.title('DTFT Dirty t=0')

    plt.xlabel('Frequency [Hz]')
    plt.ylabel('dB')

if 1:
    plt.figure()

    plt.subplot(211)
    plt.pcolormesh(txClean, fxClean, spectogramClean)
    plt.colorbar()

    x = [0]
    y = [indClean]
    for xe, ye in zip(x, y):
        plt.scatter([xe] * len(ye), fxClean[ye])
    
    plt.title('Clean Spectogram')

    plt.subplot(212)
    plt.pcolormesh(txDirty, fxDirty, spectogramDirty)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Clean Spectogram')
    plt.colorbar()

plt.show()
