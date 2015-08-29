#!/usr/bin/env python 

import json, sys, socket, time
import wiringpi2 as wiringpi

PORT = 50001
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

wiringpi.wiringPiSetup()
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(13, 0)
wiringpi.pullUpDnControl(13, 2)   
wiringpi.pinMode(19, 0)
wiringpi.pullUpDnControl(19, 2) 
wiringpi.pinMode(26, 0)
wiringpi.pullUpDnControl(26, 2) 

while True:
	if wiringpi.digitalRead(23):
		s.sendto(json.dumps([int(sys.argv[1]), 0]), ('<broadcast>', PORT))
		sleep(0.05)
	elif wiringpi.digitalRead(24):
		s.sendto(json.dumps([int(sys.argv[1]), 1]), ('<broadcast>', PORT))
		sleep(0.05)
	elif wiringpi.digitalRead(25):
		s.sendto(json.dumps([int(sys.argv[1]), 2]), ('<broadcast>', PORT))
		sleep(0.05)