#!/usr/bin/env python 

import alsaaudio as aa
import numpy as np
from fft import calculate_levels
import sys
import wiringpi2 as wiringpi

wiringpi.wiringPiSetup()
wiringpi.wiringPiSetupGpio()

# Initialize the FFT matrix
matrix    = [0, 0, 0, 0, 0, 0, 0, 0]
weighting = [512, 256, 1024, 1024, 2048, 4096, 4096, 4096]
weighting = np.true_divide(weighting, 1000000)
np.set_printoptions(suppress=True)

# Set up audio
rate = 44100
chunk = 1024
inp = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, 'sysdefault:CARD=1')
inp.setchannels(2)
inp.setrate(rate)
inp.setformat(aa.PCM_FORMAT_S16_LE)
inp.setperiodsize(chunk)

# Process audio file
count = 0
while True:
    count += 1
    l, data = inp.read()
    matrix = np.floor(calculate_levels(matrix, weighting, data, chunk, rate))
    if len(sys.argv) > 1:
        if count % 5 == 0:
            height = int(matrix[int(sys.argv[1])]*7/4095)
            r = 1
            y = 1
            g = 1
            if height > 0: g = 0
            if height > 2: y = 0
            if height > 4: r = 0
            wiringpi.digitalWrite(16, g)
            wiringpi.digitalWrite(20, y)
            wiringpi.digitalWrite(21, r)
    else:
        print matrix