#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import MySQLdb
import cgi


MEAL_SERVO_CONTROL = 14
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
    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarning(False)
    GPIO.setup(MEAL_SERVO_CONTROL, GPIO.OUT)

    pwm = GPIO.PWM(MEAL_SERVO_CONTROL, SERVO_FREQUENCY)

    # Start the SERVO moving forward
    pwm.start(10)

    # Because SERVO is not powerfull enough to make a full rotation (snacks are to heavy), we only make 1/3 rotation forward
    time.sleep(0.33)

    # And now 1/2 roration backward so we come at initial position
    pwm.start(5)
    time.sleep(0.5)

    # Clean everything
    pwm.stop()
    GPIO.cleanup()

    # Register meal in DB
    form = cgi.FieldStorage()
    db = MySQLdb.connect("localhost", "mochi", "M0ch1Datab4se", "mochi")
    username = "Raspberry Pi" if "username" not in form else  form["username"].value
    with db:
        curs=db.cursor()
        curs.execute ("""INSERT INTO meals(feeder, date) values(%s, NOW());""", username)
    db.close()

    result = 'true'
except:
    result = 'false'

# Return result
print 'Content-type: text/html\n\n'
print result
