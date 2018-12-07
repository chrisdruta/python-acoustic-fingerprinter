import hashlib
import warnings

from scipy import signal
from scipy.io import wavfile

import numpy as np

def _hideWarnings(func):
    """
    Decorator function that hides annoying deprecation warnings in find_peaks_cwt
    """
    def func_wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)

    return func_wrapper

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
    # Could cause mucho trouble in magFraq
    spectrogram[spectrogram == 0] = 0.0001
    spectrogram = 20 * np.log10(spectrogram)
    spectrogram = spectrogram/np.amax(spectrogram)

    return fx, tx, spectrogram

@_hideWarnings
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
    highpassWc = 4000
    highpassIndex = -1
    for i, f in enumerate(fx):
        if f > highpassWc:
            highpassIndex = i
            break

    if highpassIndex == -1:
        raise RuntimeError('Frequency vector doesn\'t span high enough')

    # Sum up spectrogram values for frequiences above highpassWc for each time slice of STFT
    freqMagSums = np.asarray([np.sum(spectrogram[highpassIndex:, i]) for i in range(0, spectrogram.shape[1])])
    freqMagSums[freqMagSums == -np.inf] = 0
    
    # Continuous Wavelet Transform to find peaks for time axis
    windowTime = [1]
    timePeaks = signal.find_peaks_cwt(freqMagSums, windowTime)

    # Continuous Wavelet Transform to find frequency peaks for each time peak
    freqPeaks = []
    windowFreq = [10]

    badTimePeaks = []

    for i, peakIndex in enumerate(timePeaks):
        freqsAtTime = spectrogram[highpassIndex:,peakIndex]
        freqPeaksAtTime = signal.find_peaks_cwt(freqsAtTime, windowFreq)

        if freqPeaksAtTime.size != 0:
            freqPeaks.append(freqPeaksAtTime)
        else:
            badTimePeaks.append(i)

    timePeaks = np.delete(timePeaks, badTimePeaks)
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
    MAX_HASH_TIME_DELTA = 5
    FAN_VALUE = 50

    print(len(peakFreqs))

    #quit()

    for i in range(len(peakFreqs)):
        for j in range(1, FAN_VALUE):

            if i + j < len(peakFreqs):
                f1 = peakFreqs[i]
                f2 = peakFreqs[i + j]
                t1 = peakTDeltas[i]
                t2 = peakTDeltas[i + j]
                timeDelta = t2 - t1

                if timeDelta >= MIN_HASH_TIME_DELTA and timeDelta <= MAX_HASH_TIME_DELTA:
                    freqHash = hashlib.sha1(f"{str(f1).replace(' ','')}|{str(f2).replace(' ','')}|{timeDelta}".encode()).hexdigest()
                    yield (freqHash[0:20], t1)

def FindMatches(hashes, knownSong):
    """
    Detects matches from sample hashes with hashes in known song(s)

    Args:
        hashes: sequence of tuples containing a hash and it's offset
        knownSong: dictionary contating song information

    Returns:
        True if match is found, False if not
    """
    mapper = {}
    for hash, offset in hashes:
        mapper[hash] = offset
    
    songHashes = [hash[0] for hash in knownSong['hashes']]

    matches = []
    for hash in mapper.keys():
        if hash in songHashes:
            matches.append((knownSong['id'], knownSong['offset'] - mapper[hash]))

    print(matches)
