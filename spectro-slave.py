#!/usr/bin/env python 

import sys, select, json
from socket import *
import wiringpi2 as wiringpi

PORT = 50000
BUFFER = 128
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('<broadcast>', PORT))
s.setblocking(0)

wiringpi.wiringPiSetup()
wiringpi.wiringPiSetupGpio()

while True:
    result = select.select([s],[],[])
    matrix = json.loads(result[0][0].recv(BUFFER))
    if len(sys.argv) > 1:
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
        print height
    else:
        print matrix