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

while True:
	result = select.select([button_socket],[],[])
	lightChange = json.loads(result[0][0].recv(BUFFER))
	# process change
	# send lights
	# light_socket.sendto(<lights>, ('<broadcast>', LIGHT_PORT))
