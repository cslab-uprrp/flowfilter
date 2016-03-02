#!/usr/bin/python
import cgi, cgitb
from silk import *
import json
import os
from webflow import *
from ian import *
from TreeMap import *

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
	# print "Response"
	data, startDate, endDate = receiveData(form)
	# print 'antes'
	flows = processData(data, startDate, endDate)
	# print 'dsps'
	# print """<h3> Flows: """+str(len(flows))+"""</h3>"""
	# graph = TreeMap(flows)
	# graph = ForceDirected(flows)
	# print graph
	print toJson(flows)
	# print len(flows)

else:
	printFilterPage()
	print "There is no filter..."
