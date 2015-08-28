#!/usr/bin/env python 

import json, sys, socket

PORT = 50001
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#while True:
	# listen for button change
    # s.sendto(<light change on sys arg index>, ('<broadcast>', PORT))
