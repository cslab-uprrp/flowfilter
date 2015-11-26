#!/usr/bin/python
import cgi, cgitb
from silk import *
import json
import os
from engine import *
from ian import *

print """Content-Type: text/html"""
print

def receiveData(form):
	data = form.getvalue("data")
	data = json.loads(data)
	startDate = str(data['start'])
	endDate = str(data['end'])
	data = data['data']

	return data, startDate, endDate

form = cgi.FieldStorage()

if(form.has_key("data")):
	print "Response"
	data, startDate, endDate = receiveData(form)
	flows = processData(data, startDate, endDate)
	print data
	print 'len Flows: ' + str(len(flows))
	# for item in flows:
	# 	print 'sip: ', item.sip, "---- dip: ", item.dip, "---- sport: ", item.sport
	# print flows

	graph = ForceDirected(flows)
	print graph

else:
	printFilterPage()
	print "There is no filter..."