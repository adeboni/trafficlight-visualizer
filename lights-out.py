#!/usr/bin/env python 

import select, json, socket, sys

BUTTON_PORT = 50001
BUFFER = 128
button_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
button_socket.bind(('0.0.0.0', BUTTON_PORT))
button_socket.setblocking(0)


LIGHT_PORT = 50000
light_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
light_socket.bind(('', 0))
light_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


pattern = [[0,1,0],[1,0,1],[0,1,0]]
light_state = [[0,0,0],[0,0,0]]

def toggle(x, y):
	for i in [-1, 0, 1]:
		for j in [-1, 0, 1]:
			if x+i >= 0 and x+i < 3 and y+j >= 0 and y+j < 2:
				light_state[y+j][x+i] ^= pattern[j+1][i+1]
			
while True:
	result = select.select([button_socket],[],[])
	light_change = json.loads(result[0][0].recv(BUFFER))
	toggle(light_change[1], light_change[0])
	light_socket.sendto(json.dumps(light_state), ('<broadcast>', LIGHT_PORT))
