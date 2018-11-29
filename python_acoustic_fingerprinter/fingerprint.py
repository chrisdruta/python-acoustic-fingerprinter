from scipy import signal
from scipy.io import wavfile

import hashlib

def _binaryEncode(string):
    binary = ' '.join(map(bin, bytearray(string, encoding='utf-8')))

def FindPeaks(samples):
    pass

def GenerateHash(peakFreqs, peakTDeltas):
    toHash = f"{peakFreqs}{peakTDeltas}"

    fingerprintHash = hashlib.sha1(_binaryEncode(toHash)).hexdigest()
    fingerprintHash = fingerprintHash[0:len(fingerprintHash)/2]

    return fingerprintHash

def GetSpectogram(data, fs):
    pass
