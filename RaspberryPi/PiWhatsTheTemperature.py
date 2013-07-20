#! /usr/bin/python

import time
import os
import RPi.GPIO as GPIO
import urllib
import urllib2

GPIO.setmode(GPIO.BCM)

def getSensorValue(sensorId, clockPin, mosiPin, misoPin, csPin):
	if ((sensorId < 0) or (sensorId > 7)):
		return -1
	
	GPIO.output(csPin, True)
	GPIO.output(clockPin, False)
	GPIO.output(csPin, False)

	commandOut = sensorId
	commandOut |= 0x18
	commandOut <<= 3
	for i in range(5):
		if (commandOut & 0x80):
			GPIO.output(mosiPin, True)
		else:
			GPIO.output(mosiPin, False)
		commandOut <<= 1
		GPIO.output(clockPin, True)
		GPIO.output(clockPin, False)
	
	sensorValue = 0;
	for i in range(12):
		GPIO.output(clockPin, True)
		GPIO.output(clockPin, False)
		sensorValue <<= 1
		if (GPIO.input(misoPin)):
			sensorValue |= 0x1

	GPIO.output(csPin, True)
	sensorValue >>= 1
	return sensorValue

SPICLK  = 18
SPIMISO = 23
SPIMOSI = 24
SPICS   = 25

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

url = "http://piwhatsthetemperature.appspot.com/CollectInfo"

while True:
	value = getSensorValue(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
	# print value
	voltage = value * 3.3
	voltage /= 1024.0
	# print voltage
	tempCelsius = (voltage - 0.5) * 100
	#print str(tempCelsius)+"* Celsius"
	temp = "{0:.2f}".format(tempCelsius)
	print temp+"* Celsius"
	lum = str(getSensorValue(1, SPICLK, SPIMOSI, SPIMISO, SPICS))
	print "Light value "+lum

	values = {'temperature' : temp, 'luminosity' : lum}
	data = urllib.urlencode(values)
	
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	
	html = response.read()
	
	print "Response "+html
		
	time.sleep(10.0)
	os.system("clear");
