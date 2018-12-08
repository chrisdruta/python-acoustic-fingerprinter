#!/bin/python
import sys

import numpy as np
from scipy.io import wavfile

import sounddevice as sd
sd.default.device = 7

import fingerprint as fp

# Reading in files
print('Reading In Files... ', end='')
sys.stdout.flush()

fs, song1 = wavfile.read('sounds/spacejam.wav')
song2 = wavfile.read('sounds/ghostslammers.wav')[1]
noise = wavfile.read('sounds/noise.wav')[1]

# Clips recorded from phone
recording1 = wavfile.read('sounds/recording1.wav')[1]
recording2 = wavfile.read('sounds/recording2.wav')[1]

print('Done')

# Generating clips used for testing
print('Generating Clips... ', end='')
sys.stdout.flush()

clipDuration = 5
clipMultiplier = 0.3
noiseMultiplier = 10
recordingMultiplier = 6

clip1 = song1[int(len(song1)/2) - fs * clipDuration:int(len(song1)/2)]
clip2 = song1[int(len(song1)/8): int(len(song1)/8) + fs * clipDuration]
clip3 = song2[int(len(song2)/2) - fs * clipDuration:int(len(song2)/2)]
clip4 = song2[int(len(song2)/4): int(len(song2)/4) + fs * clipDuration]

noiseClip1 = noise[int(len(noise)/2): int(len(noise)/2) + clipDuration * fs]
noiseClip2 = noise[int(len(noise)/2) - clipDuration * fs: int(len(noise)/2)]

addNoise = lambda c, n: np.asarray(c * clipMultiplier + n * noiseMultiplier).astype(np.int16)

clip1 = addNoise(clip1, noiseClip1)
clip2 = addNoise(clip2, noiseClip2)
clip3 = addNoise(clip3, noiseClip2)
clip4 = addNoise(clip4, noiseClip1)

recording1 = recording1 * recordingMultiplier
recording2 = recording2 * recordingMultiplier

# Toggle playing a clip back
if 0:
    sd.play(recording1, fs)

print('Done')

print('Finger Printing Samples... ', end='')
sys.stdout.flush()

# Library of songs to search through when matching
songList = [
    {
        'songId': 1,
        'title': 'Space Jam',
        'hashes': fp.Fingerprint(song1, fs, graph=False)
    },
    {
        'songId': 2,
        'title': 'Ghost Slammers',
        'hashes': fp.Fingerprint(song2, fs, graph=False)
    }
]

# Fingerprinting clips
fp1 = fp.Fingerprint(clip1, fs, graph=False)
fp2 = fp.Fingerprint(clip2, fs)
fp3 = fp.Fingerprint(clip3, fs)
fp4 = fp.Fingerprint(clip4, fs)
fp5 = fp.Fingerprint(recording1, fs)
fp6 = fp.Fingerprint(recording2, fs)

print('Done\n')

def test(clip, name, songList):
    print(f"Matching {name}..")
    result = fp.FindMatches(clip, songList)
    print(f"Matched with {songList[result - 1]['title']}\n" if result != -1 else 'Failed to match\n')

# Toggle tests
if 1:
    print('Starting Tests\n')
    test(fp1, 'clip1', songList)
    test(fp2, 'clip2', songList)
    test(fp3, 'clip3', songList)
    test(fp4, 'clip4', songList)
    test(fp5, 'recording1', songList)
    test(fp6, 'recording2', songList)
