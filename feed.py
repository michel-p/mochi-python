#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import MySQLdb
import cgi
from datetime import datetime, timedelta
import subprocess
import os
import json


MEAL_SERVO_CONTROL = 2
FEED_BTN_LED_OUTPUT = 22

SERVO_FREQUENCY = 50 # In Hertz, which means 50 pulse in 1secs (1000ms) --> 1 pulse = 20ms

'''
STOP --> Position "90" (1.5ms pulse)
FULL SPEED FORWARD --> Position "180" (2ms pulse)
FULL SPEED BACKWARD -->  "0" (1ms pulse)

Pulses are too long (20ms when we require 2ms max)
So we manage this using a low purcentage of duty-cycle on our GPIO PWM
We use the following calculation : DCPurcentage = ( ms_required / 20 ) * 10 (to have a % between 0 and 100)
'''

FULL_SPEED_FORWARD_DC = ( 2 / 20 ) * 10
FULL_SPEED_BACKWARD_DC = ( 1 / 20 ) * 10

try:

    db = MySQLdb.connect("localhost", "mochi", "M0ch1Datab4se", "mochi")
    form = cgi.FieldStorage()
    username = "Raspberry Pi" if "username" not in form else form["username"].value
    fedLastThreeHours = False
    with db:
        curs=db.cursor()
        curs.execute ("SELECT * FROM meals ORDER BY id DESC LIMIT 0, 1")
        lastMeal = curs.fetchone()
        lastMealDate = lastMeal[2]
        now = datetime.now()
        if (now - lastMealDate) < timedelta(hours = 3):
            fedLastThreeHours = True

    if not fedLastThreeHours or username in ['Michel', 'Raspberry Pi']:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(MEAL_SERVO_CONTROL, GPIO.OUT)
        GPIO.setup(FEED_BTN_LED_OUTPUT, GPIO.OUT)
        pwm = GPIO.PWM(MEAL_SERVO_CONTROL, SERVO_FREQUENCY)

        FNULL = open(os.devnull, 'w')

        # Stop the button daemon to light the LED
        # www-data able to stop the daemon thanks to sudo visudo rules
        subprocess.Popen(['sudo /etc/init.d/mochibuttons stop'], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
        time.sleep(0.5)

        #Light the LED enough time to see it on camera
        GPIO.output(FEED_BTN_LED_OUTPUT, GPIO.HIGH)
        time.sleep(0.5)

        # Start the SERVO moving forward
        pwm.start(10)

        # Because SERVO is not powerfull enough to make a full rotation (snacks are to heavy), we only make 1/3 rotation forward
        time.sleep(0.33)

        # And now 1/2 roration backward so we come at initial position
        pwm.start(5)
        time.sleep(0.66)

        # Clean everything
        pwm.stop()
        time.sleep(0.5)
        GPIO.output(FEED_BTN_LED_OUTPUT, GPIO.LOW)
        GPIO.cleanup()

        time.sleep(0.5)
        # Restart deamons for buttons
        subprocess.Popen(['sudo /etc/init.d/mochibuttons start'], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

        # Register meal in DB
        with db:
            curs=db.cursor()
            curs.execute ("""INSERT INTO meals(feeder, date) values(%s, NOW());""", username)
        db.close()
        result = True
    else:
        result = False
except:
    result = False

# Return result
print "Status: 200 OK" if result else "Status: 400 Bad Request"
print "Content-Type: application/json"
print ""
print json.dumps(result)
