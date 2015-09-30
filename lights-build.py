#!/usr/bin/env python

import json, socket, sys, datetime, urllib2, time

light_index = int(sys.argv[1])

MailProd = "http://api.screwdriver.corp.yahoo.com:4080/badge/8507/prod/icon"
StormQA = "http://api.screwdriver.corp.yahoo.com:4080/badge/13705/qa/icon"
SearResultsQA = "http://api.screwdriver.corp.yahoo.com:4080/badge/21717/qa/icon"
MailQA = "http://api.screwdriver.corp.yahoo.com:4080/badge/8507/qa/icon"
URL = MailQA

LIGHT_PORT = 50000
light_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# light_socket.bind(('', 0))
# light_socket.bind(('en0', 0))
# light_socket.bind(('10.1.3.10', 0))
# light_socket.bind(('192.168.42.10', 0))
light_socket.bind(('192.168.0.101', 0))
light_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

dimx = 3
dimy = 2
lights = [[0 for x in range(dimx)] for y in range(dimy)]
lastFinishedBuild = 'lightgrey';

def getLights(buildColor):
    return {
        'red': [0, 0, 1],
        'purple': [0, 1, 0],
        'blue': [1, 0, 0],
        'yellow': [1, 0, 1],
        'lightgrey': [0, 0, 0],
    }.get(buildColor, [1, 1, 1])

def orLights( la1, la2 ):
	return [ la1[x] or la2[x] for x in range(dimx) ]

while True:
	result = urllib2.urlopen(URL).geturl()
	buildColor = result.split('/')[-1]
	print buildColor, lastFinishedBuild
	localLights = getLights(buildColor)
	if buildColor == 'red' or buildColor == 'blue':
		lastFinishedBuild = buildColor
	if lastFinishedBuild == 'red' or lastFinishedBuild == 'blue':
		localLights = orLights( localLights, getLights(lastFinishedBuild) )
	lights[light_index] = localLights
	light_socket.sendto(json.dumps(lights), ('<broadcast>', LIGHT_PORT))
	print lights
	time.sleep(10)
