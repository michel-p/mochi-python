#!/usr/bin/env python

import MySQLdb
import json
import datetime
import requests
import cgi

form = cgi.FieldStorage()
db = MySQLdb.connect("localhost", "mochi", "M0ch1Datab4se", "mochi")
username = form["username"].value
password = form["password"].value

with db:
    curs=db.cursor()
    curs.execute ("SELECT * FROM user WHERE username='"+username+"' AND password='"+password+"' ORDER BY id DESC")
    userAuth = curs.fetchall()
    print "Status: 200 OK" if len(userAuth) > 0 else "Status: 400 Bad Request"
    print "Content-Type: application/json"
    print ""
    print json.dumps(len(userAuth) > 0)
