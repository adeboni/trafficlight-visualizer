#!/usr/bin/env python

import json, socket, sys, datetime, urllib2, time

light_index = int(sys.argv[1])

MailProd = "http://api.screwdriver.corp.yahoo.com:4080/badge/8507/prod/icon"
StormQA = "http://api.screwdriver.corp.yahoo.com:4080/badge/13705/qa/icon"
SearResultsQA = "http://api.screwdriver.corp.yahoo.com:4080/badge/21717/qa/icon"
URL = MailProd

LIGHT_PORT = 50000
light_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# light_socket.bind(('', 0))
# light_socket.bind(('10.1.3.10', 0))
light_socket.bind(('192.168.42.10', 0))
light_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

dimx = 3
dimy = 2
lights = [[0 for x in range(dimx)] for y in range(dimy)]

def getLights(buildColor):
    return {
        'red': [1, 0, 0],
        'purple': [0, 1, 0],
        'blue': [0, 1, 1],
        'lightgrey': [0, 0, 0],
    }.get(buildColor, [1, 1, 1])

while True:
	result = urllib2.urlopen(URL).geturl()
	buildColor = result.split('/')[-1]
	print buildColor
	localLights = getLights(buildColor)
	lights[light_index] = localLights
	light_socket.sendto(json.dumps(lights), ('<broadcast>', LIGHT_PORT))
	print lights
	time.sleep(10)
