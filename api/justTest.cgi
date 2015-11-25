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
	printFilterPage()
	data, startDate, endDate = receiveData(form)
	flows = processData(data, startDate, endDate)
	print 'len Flows: ' + str(len(flows))
	graph = ForceDirected(flows)
	print graph

else:
	printFilterPage()
	print "There is no filter..."