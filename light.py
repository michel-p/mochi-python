#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os

LIGHT_OUTPUT = 24
LIGHT_BTN_INPUT = 10

CAMERA_BTN_LED_OUTPUT = 23
CAMERA_BTN_INPUT = 9

FEED_BTN_LED_OUTPUT= 22
FEED_BTN_INPUT = 25



try:
    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarning(False)
    GPIO.setup(LIGHT_BTN_INPUT, GPIO.IN)
    GPIO.setup(CAMERA_BTN_INPUT, GPIO.IN)
    GPIO.setup(FEED_BTN_INPUT, GPIO.IN)

    GPIO.setup(LIGHT_OUTPUT, GPIO.OUT)
    GPIO.setup(CAMERA_BTN_LED_OUTPUT, GPIO.OUT)
    GPIO.setup(FEED_BTN_LED_OUTPUT, GPIO.OUT)

    while True:
        # Handling the LIGHT toggle
        if GPIO.input(LIGHT_BTN_INPUT) == False:
            print("LIGHT Pressed")
            GPIO.output(LIGHT_OUTPUT, GPIO.HIGH)
        else:
            GPIO.output(LIGHT_OUTPUT, GPIO.LOW)

        # Handle the CAMERA toggle
        if GPIO.input(CAMERA_BTN_INPUT) == False:
            print("CAMERA Pressed")
            GPIO.output(CAMERA_BTN_LED_OUTPUT, GPIO.HIGH)
            command = 'sudo service motion start'
            p = os.system(command)
        else:
            GPIO.output(CAMERA_BTN_LED_OUTPUT, GPIO.LOW)
            command = 'sudo service motion stop'
            p = os.system(command)

        # Handle the FEED System Momentary
        if GPIO.input(FEED_BTN_INPUT) == False:
            print("FEED Pressed")
            GPIO.output(FEED_BTN_LED_OUTPUT, GPIO.HIGH)
        else:
            GPIO.output(FEED_BTN_LED_OUTPUT, GPIO.LOW)


except KeyboardInterrupt:
    print 'interrupted!'

# Clean everything
# pwm.stop()
GPIO.cleanup()
