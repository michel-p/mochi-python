#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os
import subprocess
import json

LIGHT_OUTPUT = 24

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(LIGHT_OUTPUT, GPIO.OUT)
    FNULL = open(os.devnull, 'w')

    # Handling the LIGHT toggle
    if GPIO.input(LIGHT_OUTPUT) == False:
        # Stop the button daemon to light the LED
        subprocess.Popen(['sudo /etc/init.d/mochibuttons stop'], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
        #time.sleep(0.2)
        GPIO.output(LIGHT_OUTPUT, GPIO.HIGH)
        light = True
        #time.sleep(10)
    else:
        GPIO.output(LIGHT_OUTPUT, GPIO.LOW)
        #time.sleep(0.2)
        # Restart deamons for buttons
        subprocess.Popen(['sudo /etc/init.d/mochibuttons start'], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
        light = False
    result = True
except:
    result = False

print "Status: 200 OK" if result else "Status: 400 Bad Request"
print "Content-Type: application/json"
print ""
print json.dumps({'result':result, 'lightOn': light})
