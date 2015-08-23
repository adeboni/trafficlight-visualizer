#!/usr/bin/env python 

import select, json, socket, sys
import wiringpi2 as wiringpi

PORT = 50000
BUFFER = 128
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', PORT))
s.setblocking(0)

wiringpi.wiringPiSetup()
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(16, 1)
wiringpi.pinMode(20, 1)
wiringpi.pinMode(21, 1)

while True:
	result = select.select([s],[],[])
	matrix = json.loads(result[0][0].recv(BUFFER))
	wiringpi.digitalWrite(16, matrix[int(sys.argv[1])][0])
	wiringpi.digitalWrite(20, matrix[int(sys.argv[1])][1])
	wiringpi.digitalWrite(21, matrix[int(sys.argv[1])][2])