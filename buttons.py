#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os

LIGHT_OUTPUT = 24
LIGHT_BTN_INPUT = 10

CAMERA_BTN_LED_OUTPUT = 23
CAMERA_BTN_INPUT = 9

FEED_BTN_LED_OUTPUT = 22
FEED_BTN_INPUT = 25

try:
    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)
    GPIO.setup(LIGHT_BTN_INPUT, GPIO.IN)
    GPIO.setup(CAMERA_BTN_INPUT, GPIO.IN)
    GPIO.setup(FEED_BTN_INPUT, GPIO.IN)

    GPIO.setup(LIGHT_OUTPUT, GPIO.OUT)
    GPIO.setup(CAMERA_BTN_LED_OUTPUT, GPIO.OUT)
    GPIO.setup(FEED_BTN_LED_OUTPUT, GPIO.OUT)

    while True:
        # Handling the LIGHT toggle
        if GPIO.input(LIGHT_BTN_INPUT) == False:
            #print("LIGHT Pressed")
            GPIO.output(LIGHT_OUTPUT, GPIO.HIGH)
            time.sleep(0.1)
        else:
            GPIO.output(LIGHT_OUTPUT, GPIO.LOW)
            time.sleep(0.1)

        # Handle the CAMERA toggle
        if GPIO.input(CAMERA_BTN_INPUT) == False:
            #print("CAMERA Pressed")
            GPIO.output(CAMERA_BTN_LED_OUTPUT, GPIO.HIGH)
            time.sleep(0.1)
            command = 'sudo service motion start'
            p = os.system(command)
        else:
            GPIO.output(CAMERA_BTN_LED_OUTPUT, GPIO.LOW)
            time.sleep(0.1)
            command = 'sudo service motion stop'
            p = os.system(command)

        # Handle the FEED System Momentary
        if GPIO.input(FEED_BTN_INPUT) == False:
            #print("FEED Pressed")
            GPIO.output(FEED_BTN_LED_OUTPUT, GPIO.HIGH)
            command = 'python /var/www/html/mochi/cage_feed.py'
            p = os.system(command)
            time.sleep(1)
        else:
            GPIO.output(FEED_BTN_LED_OUTPUT, GPIO.LOW)
            time.sleep(0.1)

except KeyboardInterrupt:
    print 'interrupted!'
    GPIO.cleanup()
    


# Clean everything
GPIO.cleanup()
