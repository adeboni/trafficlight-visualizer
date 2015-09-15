#!/usr/bin/env python 

import select, json, socket, sys, time, os, random, math, thread


BUTTON_PORT = 50001
BUFFER = 128
button_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
button_socket.bind(('0.0.0.0', BUTTON_PORT))
button_socket.setblocking(0)


LIGHT_PORT = 50000
light_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
light_socket.bind(('', 0))
light_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


random = [[[int(math.floor(random.random()+0.5)) for x in range(3)],[int(math.floor(random.random()+0.5)) for x in range(3)]] for y in range(50)]
circle = [
	[[1,0,0],[0,0,0]],
	[[0,1,0],[0,0,0]],
	[[0,0,1],[0,0,0]],
	[[0,0,0],[0,0,1]],
	[[0,0,0],[0,1,0]],
	[[0,0,0],[1,0,0]]
]
circle2 = [
        [[1,1,0],[0,0,0]],
        [[0,1,1],[0,0,0]],
        [[0,0,1],[0,0,1]],
        [[0,0,0],[0,1,1]],
        [[0,0,0],[1,1,0]],
        [[1,0,0],[1,0,0]],
	[[0,0,0],[0,0,0]]
]
pong = [
	[[0,0,1],[0,0,0]],
	[[0,0,0],[0,0,1]],
	[[0,1,0],[0,0,0]],
	[[0,0,0],[0,1,0]],
	[[1,0,0],[0,0,0]],
	[[0,0,0],[1,0,0]],
	[[0,0,0],[0,0,0]]
]
bounce = [
	[[1,0,0],[0,0,0]],
	[[0,1,0],[0,0,0]],
	[[0,0,1],[0,0,0]],
	[[0,1,0],[0,0,0]],
	[[1,0,0],[0,0,0]],
	[[0,0,0],[1,0,0]],
	[[0,0,0],[0,1,0]],
	[[0,0,0],[0,0,1]],
	[[0,0,0],[0,1,0]],
	[[0,0,0],[1,0,0]],
	[[0,0,0],[0,0,0]]
]
onoff = [
	[[1,1,1],[1,1,1]],
        [[0,0,0],[0,0,0]]
]

def get_state(x):
	s = [[0,0,0],[0,0,0]]
	s[0][0] = int(x & 1 > 0)
	s[0][1] = int(x & 2 > 0)
        s[0][2] = int(x & 4 > 0)
        s[1][0] = int(x & 8 > 0)
        s[1][1] = int(x & 16 > 0)
        s[1][2] = int(x & 32 > 0)
	return s

count = [get_state(x) for x in range(2**6)]

seq = [count, circle, circle2, pong, onoff, bounce, random]

slbp = 0
def button_listener(x):
	global slbp
	while True:
		result = select.select([button_socket],[],[])
        	button_press = json.loads(result[0][0].recv(BUFFER))
		slbp = 0	

thread.start_new_thread(button_listener, (0, ))


seq_num = 0
while True:
	curr = seq[seq_num%len(seq)]
	seq_num += 1
	for i in range(3):
		for j in range(len(curr)):
			print json.dumps([curr[j][0],curr[j][1]])
			if slbp > 10: light_socket.sendto(json.dumps([curr[j][0],curr[j][1]]), ('<broadcast>', PORT))
			time.sleep(1)
			slbp += 1
		
