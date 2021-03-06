#!/usr/bin/env python 

import select, json, socket, sys, datetime

BUTTON_PORT = 50001
BUFFER = 128
button_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
button_socket.bind(('0.0.0.0', BUTTON_PORT))
button_socket.setblocking(0)


LIGHT_PORT = 50000
light_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
light_socket.bind(('', 0))
light_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def get_time():
	x = str(datetime.datetime.now()).split(' ')[1].split(':')
	return float(x[0])*3600 + float(x[1])*60 + float(x[2])


dimx = 3
dimy = 2
lights = [[0 for x in range(dimx)] for y in range(dimy)]
pattern = [[0,1,0],[1,0,1],[0,1,0]]

def toggle(x, y):
	for i in [-1, 0, 1]:
		for j in [-1, 0, 1]:
			if x+j >= 0 and x+j < dimy and y+i >=0 and y+i < dimx:
				lights[x+j][y+i] ^= pattern[j+1][i+1]

light_socket.sendto(json.dumps(lights), ('<broadcast>', LIGHT_PORT))
print lights

slbp = get_time()		
while True:
	result = select.select([button_socket],[],[])
	light_change = json.loads(result[0][0].recv(BUFFER))
	
	curr_time = get_time()
	if curr_time - slbp > 123:
		time.sleep(1)
		lights = [[0 for x in range(dimx)] for y in range(dimy)]
	else:
		toggle(light_change[0], light_change[1])
	
	light_socket.sendto(json.dumps(lights), ('<broadcast>', LIGHT_PORT))
	
	slbp = get_time()
	print lights
