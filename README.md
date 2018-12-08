# python-acoustic-fingerprinter

Ece 429 DSP Independent Study Final Project

![example fingerprint](https://raw.githubusercontent.com/chrisdruta/python-acoustic-fingerprinter/master/images/example.png)

> Fingerprint Example

```
> Executing task: python main.py <
Reading In Files... Done
Generating Clips... Done
Finger Printing Samples... Done

Starting Tests

Matching clip1..
Number of matches: 2
Matched with Space Jam

Matching clip2..
Number of matches: 3
Matched with Space Jam

Matching clip3..
Number of matches: 1
Matched with Ghost Slammers

Matching clip4..
Number of matches: 1
Matched with Ghost Slammers

Matching recording1..
Number of matches: 0
Failed to match

Matching recording2..
Number of matches: 1
Matched with Space Jam
```

> Example Script Output

## Requirements

Requirements can be found in ./python_acoustic-fingerprinter/requirements.txt, but here they are as well:

* sounddevice
* matplotlib
* scipy
* numpy

## How to Use

Make sure you have above requirements set up in your python environment and then simply run main.py.

There are multiple possible configurations commented inside the code if want to play around with the figerprinting algorithm. More specific documentation is provided below

## How it works

[Final Project Report and Documentation](https://github.com/chrisdruta/python-acoustic-fingerprinter/blob/master/images/report.pdf "Project Report")

## Copyright

Copyright Disclaimer Under Section 107 of the Copyright Act 1976, allowance is made for "fair use" for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use.
