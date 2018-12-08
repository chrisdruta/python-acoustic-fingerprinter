#!/bin/python
import numpy as np

from scipy.io import wavfile

import sounddevice as sd
sd.default.device = 7

import fingerprint as fp

# Reading in files
fs, song1 = wavfile.read('sounds/spacejam.wav')

song1 = song1[:, 0] # Left channel to make mono
song2 = wavfile.read('sounds/ghostslammers.wav')[1] # Already mono
noise = wavfile.read('sounds/noise.wav')[1] # Already mono

# Generating clips to try to match (test)
clipDuration = 5
clipMultiplier = 0.5
noiseMultiplier = 10

clip1 = song1[int(len(song1)/2) - fs * clipDuration:int(len(song1)/2)]
clip2 = song1[int(len(song1)/4): int(len(song1)/4) + fs * clipDuration]
clip3 = song2[int(len(song2)/2) - fs * clipDuration:int(len(song2)/2)]
clip4 = song2[int(len(song2)/4): int(len(song2)/4) + fs * clipDuration]

noiseClip1 = noise[int(len(noise)/2): int(len(noise)/2) + clipDuration * fs]
noiseClip2 = noise[int(len(noise)/2) - clipDuration * fs: int(len(noise)/2)]

addNoise = lambda c, n: np.asarray(c * clipMultiplier + n * noiseMultiplier).astype(np.int16)

clip1 = addNoise(clip1, noiseClip1)
clip2 = addNoise(clip2, noiseClip2)
clip3 = addNoise(clip3, noiseClip2)
clip4 = addNoise(clip4, noiseClip1)

# Toggle playing a clip back
if 0:
    sd.play(clip1, fs)

songList = [
    {
        'songId': 1,
        'title': 'Space Jam',
        'offset': 0,
        'hashes': fp.Fingerprint(song1, fs, True)
    },
    {
        'songId': 2,
        'title': 'Ghost Slammers',
        'offset': 0,
        'hashes': fp.Fingerprint(song2, fs, True)
    }
]

# Fingerprinting clips
fp1 = fp.Fingerprint(clip1, fs)
fp2 = fp.Fingerprint(clip2, fs)
fp3 = fp.Fingerprint(clip3, fs)
fp4 = fp.Fingerprint(clip4, fs)

def test(clip, name, songList):
    print(f"Matching {name}....")
    result = fp.FindMatches(clip, songList)
    print(f"Matched with {songList[result - 1]['title']}" if result != -1 else 'Failed to match')

# Toggle tests
if 1:
    test(fp1, 'clip1', songList)
    test(fp2, 'clip2', songList)
    test(fp3, 'clip3', songList)
    test(fp4, 'clip4', songList)
