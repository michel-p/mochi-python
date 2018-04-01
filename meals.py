#!/usr/bin/env python

import MySQLdb
import json
import datetime
import requests

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

try:
    db = MySQLdb.connect("localhost", "mochi", "M0ch1Datab4se", "mochi")
    with db:
        curs=db.cursor()
        curs.execute ("SELECT * FROM meals ORDER BY id DESC")
        meals = curs.fetchall()
        mealsJson = json.dumps(meals, default=datetime_handler)
        print "Status: 200 OK"
        print "Content-Type: application/json"
        print "Length:", len(mealsJson)
        print ""
        print mealsJson
except:
    print "Status: 400 Bad Request"
    print "Content-Type: application/json"
    print ""
    print json.dumps(False)
