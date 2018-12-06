from scipy import signal
from scipy.io import wavfile

import numpy as np

import hashlib

def FindPeaks(spectrogram, fx, tx):
    """
    Finds frequncy peaks and signifcant time delta peaks

    Args:
        spectrogram: spectrogram of audio data (1 channel)
        fx: a vector of frequency bins,
        tx: vector of time bins

    Returns:
        vector of significant time delta peak indices
        vector of frequency peaks for each time delta
    """

    # Shitty high pass
    highpassWc = 5000
    highpassIndex = -1
    for i, f in enumerate(fx):
        if f > highpassWc:
            highpassIndex = i
            break

    if highpassIndex == -1:
        raise RuntimeError('Frequency vector doesn\'t span high enough')

    # Sum up spectrogram values for frequiences above highpassWc for each time slice of STFT
    freqMagSums = [np.sum(spectrogram[highpassIndex:, i]) for i in range(0, spectrogram.shape[1])]
    
    # Continuous Wavelet Transform to find peaks for time axis
    windowTime = [5]
    timePeaks = signal.find_peaks_cwt(freqMagSums, windowTime)

    # Continuous Wavelet Transform to find frequency peaks for each time peak
    freqPeaks = []
    windowFreq = [10]
    for peakIndex in timePeaks:
        freqsAtTime = spectrogram[:,peakIndex]
        freqPeaks.append(signal.find_peaks_cwt(freqsAtTime, windowFreq))
    
    return timePeaks, freqPeaks 

def GenerateHash(peakFreqs, peakTDeltas):
    """
    Hashes data containing audio clip fingerprint

    Args:
        peakFreqs: blah
        peakTDeltas: blah blah
    
    Returns:
        String of hash containing audio clip fingerprint
    """
    MIN_HASH_TIME_DELTA = 0
    MAX_HASH_TIME_DELTA = 200
    FAN_VALUE = 5

    for i in range(len(peakFreqs)):
        for j in range(1, FAN_VALUE):

            if i + j < len(peakFreqs):
                f1 = peakFreqs[i]
                f2 = peakFreqs[i + j]
                t1 = peakTDeltas[i]
                t2 = peakTDeltas[i + j]
                timeDelta = t2 - t1

                if timeDelta >= MIN_HASH_TIME_DELTA and timeDelta <= MAX_HASH_TIME_DELTA:
                    freqHash = hashlib.sha1(f"${f1}|${f2}|${timeDelta}".encode()).hexdigest()
                    yield (freqHash[0:20], t1)

def GenerateSpectrogram(data, fs):
    """
    Generate and cleanse spectrogram of an audio clip.

    Args:
        data: raw audio data
        fs: sampling frequency of the data

    Returns:
        fx, a vector of frequency bins,
        tx, vector of time bins,
        2d array containing spectrogram data (of 1 channel) mapped by fx & tx
    
    Raises:
        Execption for audio data of greater than 2 channels
    """
    fx, tx, spectrogram = signal.spectrogram(data, fs)

    spectrogram[spectrogram == -np.inf] = 0
    spectrogram = 20 * np.log10(spectrogram)
    spectrogram = spectrogram/np.amax(spectrogram)

    return fx, tx, spectrogram
