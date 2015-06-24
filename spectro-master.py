#!/usr/bin/env python 

import alsaaudio as aa
import numpy as np
from fft import calculate_levels
import json
from socket import *

PORT = 50000
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

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
    if count % 5 == 0:
        s.sendto(json.dumps(matrix.tolist()), ('<broadcast>', PORT))