#!/usr/bin/env python 

import json, sys, socket, time
import wiringpi2 as wiringpi

PORT = 50001
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

wiringpi.wiringPiSetup()
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(23, 0)
wiringpi.pullUpDnControl(23, 2)   
wiringpi.pinMode(24, 0)
wiringpi.pullUpDnControl(24, 2) 
wiringpi.pinMode(25, 0)
wiringpi.pullUpDnControl(25, 2) 

while True:
	if not wiringpi.digitalRead(23):
		s.sendto(json.dumps([int(sys.argv[1]), 0]), ('<broadcast>', PORT))
		time.sleep(0.05)
	elif not wiringpi.digitalRead(24):
		s.sendto(json.dumps([int(sys.argv[1]), 1]), ('<broadcast>', PORT))
		time.sleep(0.05)
	elif not wiringpi.digitalRead(25):
		s.sendto(json.dumps([int(sys.argv[1]), 2]), ('<broadcast>', PORT))
		time.sleep(0.05)