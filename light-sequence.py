#!/usr/bin/env python 

import select, json, socket, sys, alsaaudio, time, audioop, math

PORT = 50000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

seq = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK,'sysdefault:CARD=1')
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)

vol = 2.0
i = 0
while True:
	time.sleep(0.01)
	l,data = inp.read()
	if l:
		vol = math.min(1.0, math.log(1.0 * audioop.max(data, 2) / 750))
	#s.sendto(json.dumps([seq[i%len(seq)],seq[i%len(seq)]]), ('<broadcast>', PORT))
	i += 1
	print vol
	#time.sleep(vol)

	