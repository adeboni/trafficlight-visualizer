#!/usr/bin/env python 

import json, sys, socket, time
import wiringpi2 as wiringpi

PORT = 50001
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind(('', 0))
# s.bind(('10.1.3.1', 0))
s.bind(('192.168.42.1', 0))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

wiringpi.wiringPiSetup()
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(13, 0)
wiringpi.pullUpDnControl(13, 2)   
wiringpi.pinMode(19, 0)
wiringpi.pullUpDnControl(19, 2) 
wiringpi.pinMode(26, 0)
wiringpi.pullUpDnControl(26, 2) 

light_index = int(sys.argv[1])
light_color = int(sys.argv[2])
button_pin = int(sys.argv[3])
state = 0

while True:
	if wiringpi.digitalRead(button_pin):
		state = 0
		time.sleep(0.1)
	elif not wiringpi.digitalRead(button_pin):
		state += 1
		if state == 3:
			s.sendto(json.dumps([light_index, light_color]), ('<broadcast>', PORT))
			print 'button pressed: ' + json.dumps([light_index, light_color, button_pin])
		time.sleep(0.05)
