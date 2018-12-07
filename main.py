#!/bin/python
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from scipy import stats
from scipy import signal
from scipy.io import wavfile

import sounddevice as sd
sd.default.device = 7

from python_acoustic_fingerprinter import fingerprint as fp

clipDuration = 10

fs, cleanData = wavfile.read('spacejam.wav')
cleanData = cleanData[:, 0] # Left channel
cleanClipData = cleanData[int(len(cleanData)/2):int(len(cleanData)/2 + clipDuration * fs)]
#cleanData = cleanClipData

noise = wavfile.read('noise.wav')[1]
noise = noise[int(len(noise)/2): int(len(noise)/2) + clipDuration * fs]

dirtyData = cleanClipData * 1# + noise * 1
dirtyData = dirtyData.astype(np.int16)
#sd.play(dirtyData, fs)

fxClean, txClean, spectrogramClean = fp.GenerateSpectrogram(cleanData, fs)
fxDirty, txDirty, spectrogramDirty = fp.GenerateSpectrogram(dirtyData, fs)

timePeaksClean, freqPeaksClean = fp.FindPeaks(spectrogramClean, fxClean, txClean)
timePeaksDirty, freqPeaksDirty = fp.FindPeaks(spectrogramDirty, fxDirty, txDirty)

# Peaks given in indices, get the actual values
fPeakValsClean = [fxClean[i] for i in freqPeaksClean]
tPeakValsClean = txClean[timePeaksClean]

fPeakValsDirty = [fxDirty[i] for i in freqPeaksDirty]
tPeakValsDirty = txDirty[timePeaksDirty]

cleanHashes = fp.GenerateHash(fPeakValsClean, tPeakValsClean)
dirtyHashes = fp.GenerateHash(fPeakValsDirty, tPeakValsDirty)

test1 = list(cleanHashes)
test2 = list(dirtyHashes)

print(len(test1))
print(len(test2))

knownSong = {
    'id': 0,
    'offset': 0,#txClean[-1],
    'hashes': test1
}

fp.FindMatches(test2, knownSong)

if 1:
    plt.figure()

    plt.subplot(211)
    plt.pcolormesh(txClean, fxClean, spectrogramClean)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()

    for xe, ye in zip(timePeaksClean, freqPeaksClean):
        plt.scatter([txClean[xe]] * len(ye), fxClean[ye], edgecolors='black')

    plt.title('Clean spectrogram')

    plt.subplot(212)
    plt.pcolormesh(txDirty, fxDirty, spectrogramDirty)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()

    for xe, ye in zip(timePeaksDirty, freqPeaksDirty):
        plt.scatter([txDirty[xe]] * len(ye), fxDirty[ye], edgecolors='black')
    
    plt.title('Dirty spectrogram')
    plt.tight_layout()
    plt.show()
