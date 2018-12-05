from scipy import signal
from scipy.io import wavfile

import numpy as np

import hashlib

def _binaryEncode(string):
    """
    Helper function to encode a string into bytes for hashing
    Taken from: https://stackoverflow.com/questions/18815820/convert-string-to-binary-in-python
    (Author: Ben)

    Args:
        string: input string to be byte encoded

    Returns:
        utf-8 byte encoded input string
    """
    return ' '.join(map(bin, bytearray(string, encoding='utf-8')))

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
    windowTime = [1]
    timePeaks = signal.find_peaks_cwt(freqMagSums, windowTime)

    # Continuous Wavelet Transform to find frequency peaks for each time peak
    freqPeaks = []
    windowFreq = [5]
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
    toHash = f"{peakFreqs}{peakTDeltas}"

    fingerprintHash = hashlib.sha1(_binaryEncode(toHash)).hexdigest()
    fingerprintHash = fingerprintHash[0:len(fingerprintHash)/2]

    return fingerprintHash

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
