from scipy import signal
from scipy.io import wavfile

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

def FindPeaks(spectogram, fx, tx):
    """
    Finds frequncy peaks and for each significant time delta

    Args:
        spectogram: spectogram of audio data (1 channel)
        fx: a vector of frequency bins,
        tx: vector of time bins

    Returns:
        vector of binned peaks,
        vector of significant time deltas
    """
    pass

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

def GetSpectogram(data, fs):
    """
    Generate and cleanse spectogram of an audio clip.

    Args:
        data: raw audio data
        fs: sampling frequency of the data

    Returns:
        fx, a vector of frequency bins,
        tx, vector of time bins,
        2d array containing spectogram data (of 1 channel) mapped by fx & tx
    
    Raises:
        Execption for audio data of greater than 2 channels
    """
    pass
