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

def Fingerprint(samples, fs):
    """
    Fingerprint all samples at given fs

    Args:
        samples: mono channel raw wav data
        fs: sampling frequency used for data

    Returns:
        List of hashe tuples in the form (hash, offset)
    """
    fx, tx, spectrogram = GenerateSpectrogram(samples, fs)
    timePeaks, freqPeaks = FindPeaks(spectrogram, fx, tx)

    # Peaks given in indices, get the actual values for hashing
    freqPeakVals = [fx[i] for i in freqPeaks]
    timePeakVals = tx[timePeaks]

    return list(GenerateHash(freqPeakVals, timePeakVals))

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
    freqMagSums = np.asarray([np.sum(spectrogram[highpassIndex:, i]) for i in range(spectrogram.shape[1])])
    
    # Continuous Wavelet Transform to find peaks for time axis
    windowTime = [1]
    timePeaks = signal.find_peaks_cwt(freqMagSums, windowTime)

    # Continuous Wavelet Transform to find frequency peaks for each time peak
    freqPeaks = []
    badTimePeaks = []
    windowFreq = [10]

    for i, peakIndex in enumerate(timePeaks):
        freqsAtTime = spectrogram[highpassIndex:,peakIndex]
        
        freqPeaksAtTime = signal.find_peaks_cwt(freqsAtTime, windowFreq)

        # Case for no peaks found at this time peak
        if freqPeaksAtTime.size != 0:
            freqPeaks.append([freqIndex + highpassIndex for freqIndex in freqPeaksAtTime])
        else:
            badTimePeaks.append(i)

    timePeaks = np.delete(timePeaks, badTimePeaks)
    return timePeaks, freqPeaks 

def GenerateHash(peakFreqs, peakTDeltas):
    """
    Hashes data containing audio clip fingerprint

    Args:
        peakFreqs: peak frequency values for each time slice
        peakTDeltas: peak time values that frequency peaks were evaluated at
    
    Returns:
        List of hashe tuples in the form (hash, offset)
    """
    MIN_HASH_TIME_DELTA = 0
    MAX_HASH_TIME_DELTA = 5
    FAN_VALUE = 50

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

def FindMatches(hashes, knownSongList):
    """
    Detects matches from sample hashes with hashes in known song(s)

    Args:
        hashes: sequence of tuples containing a hash and it's offset
        knownSongList: list of dictionarys contating song information

    Returns:
        list of tuples containing match info such as (songId, relative offset)
    """
    inputMapper = {}
    for hash, offset in hashes:
        inputMapper[hash] = offset
    
    matches = []
    for song in knownSongList:
        songMapper = {}
        for hash, offset in song['hashes']:
            songMapper[hash] = offset

        for hash in inputMapper.keys():
            if hash in songMapper.keys():
                matches.append((song['id'], songMapper[hash] - inputMapper[hash]))

    return matches

def AlignMatches(matches):
    """
    Tallys up each dif's song id frequency and returns the song id with highest count diff

    Args:
        matches: list of tuples containing (song id, relative offset) matched from known song

    Returns:
        songId (int)
    """
    diffMap = {}
    largestCount = 0
    songId = -1
    for sid, diff in matches:
        if diff not in diffMap:
            diffMap[diff] = {}
        if sid not in diffMap[diff]:
            diffMap[diff][sid] = 0

        diffMap[diff][sid] += 1

        if diffMap[diff][sid] > largestCount:
            largestCount = diffMap[diff][sid]
            songId = sid

    return songId
