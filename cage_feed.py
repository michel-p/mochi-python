#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import MySQLdb


MEAL_SERVO_CONTROL = 2
SERVO_FREQUENCY = 50 # In Hertz, which means 50 pulse in 1secs (1000ms) --> 1 pulse = 20ms
FULL_SPEED_FORWARD_DC = ( 2 / 20 ) * 10
FULL_SPEED_BACKWARD_DC = ( 1 / 20 ) * 10

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(MEAL_SERVO_CONTROL, GPIO.OUT)
    pwm = GPIO.PWM(MEAL_SERVO_CONTROL, SERVO_FREQUENCY)

    # Start the SERVO moving forward
    pwm.start(10)
    time.sleep(0.5)
    pwm.start(5)
    time.sleep(0.5)

    # Clean everything
    pwm.stop()
    GPIO.cleanup()

    # Register meal in DB
    db = MySQLdb.connect("localhost", "mochi", "M0ch1Datab4se", "mochi")
    username = "Cage Direct Feed"
    with db:
        curs=db.cursor()
        curs.execute ("""INSERT INTO meals(feeder, date) values(%s, NOW());""", username)
    db.close()

except KeyboardInterrupt:
    print 'interrupted!'
    GPIO.cleanup()