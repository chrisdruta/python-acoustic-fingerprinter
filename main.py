#!/bin/python
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from scipy import stats
from scipy import signal
from scipy.io import wavfile

import sounddevice as sd
#sd.default.device = 7

clipDuration = 5

fs, cleanData = wavfile.read('spacejam.wav')
cleanData = cleanData[:, 0] # Left channel
cleanData = cleanData[int(len(cleanData)/2):int(len(cleanData)/2 + clipDuration * fs)]

noise = wavfile.read('noise.wav')[1]
noise = noise[int(len(noise)/2): int(len(noise)/2) + clipDuration * fs]

test = noise * 1.5
test = test.astype(np.int16)

"""
ff, tt, test = signal.spectrogram(noise, fs)
test[test == -np.inf] = 0
test = np.log10(test)
plt.figure()
plt.pcolormesh(tt, ff, test)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar()
plt.title('test')"""


dirtyData = cleanData * 0.1 + noise * 1.5
dirtyData = dirtyData.astype(np.int16)
sd.play(dirtyData, fs)

fxClean, txClean, spectrogramClean = signal.spectrogram(cleanData, fs)
spectrogramClean[spectrogramClean == -np.inf] = 0
spectrogramClean = 20 * np.log10(spectrogramClean)
spectrogramClean = spectrogramClean/np.amax(spectrogramClean)

fxDirty, txDirty, spectrogramDirty = signal.spectrogram(dirtyData, fs)
spectrogramDirty[spectrogramDirty == -np.inf] = 0
spectrogramDirty = 20 * np.log10(spectrogramDirty)
spectrogramDirty = spectrogramDirty/np.amax(spectrogramDirty)

times = []
peaksClean = []
peaksDirty = []
window = [10]
test = []

highpassWc = 5000
# Shitty highpass
for i, f in enumerate(fxClean):
    if f > highpassWc:
        highpassIndex = i
        break

for i in range(0, spectrogramClean.shape[1]):

    test.append(np.sum(spectrogramClean[highpassIndex:,i]))

    times.append(i)
    freqsAtiClean = spectrogramClean[:,i]
    freqsAtiDirty = spectrogramDirty[:,i]
    
    peaksClean.append(signal.find_peaks_cwt(freqsAtiClean, window))
    peaksDirty.append(signal.find_peaks_cwt(freqsAtiDirty, window))

hmm = [round(t) for t in test]
hmmAmp = [h * 200 for h in hmm]
hmmX = txClean[np.arange(0, len(hmm), 1)]

window2 = [1]
peaks = signal.find_peaks_cwt(hmm, window2)

if 1:
    plt.figure()

    plt.subplot(211)
    plt.pcolormesh(txClean, fxClean, spectrogramClean)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()
    plt.plot(hmmX, hmmAmp, '-k')
    plt.stem(txClean[peaks], [fxClean[60]] * len(txClean[peaks]))

    #for xe, ye in zip(times, peaksClean):
    #    plt.scatter([txClean[xe]] * len(ye), fxClean[ye], edgecolors='black')

    plt.title('Clean spectrogram')

    plt.subplot(212)
    plt.pcolormesh(txDirty, fxDirty, spectrogramDirty)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()

    #for xe, ye in zip(times, peaksDirty):
    #    plt.scatter([txDirty[xe]] * len(ye), fxDirty[ye], edgecolors='black')
    
    plt.title('Dirty spectrogram')
    plt.tight_layout()
    plt.show()
