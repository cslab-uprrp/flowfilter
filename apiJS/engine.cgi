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
	filteredData = data['filteredData']
	path = data['path']
	entries = int(data['entries'])
	data = data['data']
	return data, startDate, endDate, filteredData, path, entries

form = cgi.FieldStorage()

if(form.has_key("data")):
	# print "Response"
	data, startDate, endDate, useFilteredData, pathOfFilteredData, entries = receiveData(form)
	# print 'antes'
	flows, filePath = processData(data, startDate, endDate, useFilteredData, pathOfFilteredData)
	# print """<h3> Flows: """+str(len(flows))+"""</h3>"""
	# graph = TreeMap(flows)
	# graph = ForceDirected(flows)
	# print graph
	if entries == -1:
		fl = toJson(flows)
	else:
		fl = toJson(flows[0:entries])

	print json.dumps({'flows': fl, 'path': filePath, 'totalFlows': len(flows)})
	# print len(flows)

elif form.has_key("entries"):
	info = form.getvalue("entries")
	info = json.loads(info)
	first = info['first']
	last = info['last']
	path = info['path']

	newFile = open('%s'%(path), 'r')
	filteredData = json.loads(newFile.read())
	filtereDflows = filteredData['flows']

	newFile.close()
	entries = filtereDflows[first:last]
	print json.dumps({'entries': entries, 'path': path, 'totalFlows': len(filtereDflows)})

else:
	printFilterPage()
	print "There is no filter..."
