#!/usr/bin/python
import cgi, cgitb
from silk import *
import json
import os
from webflow import *
sys.path.append("Visualizations")
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
	
	ipversion = int(data['ipversion'])
	
	startTime = str(data['starttime'])
	endTime = str(data['endtime'])

	vis = int(data['vis'])
	data = data['data']

	return data, startDate, startTime, endDate, endTime, filteredData, path, entries, vis, ipversion
	

form = cgi.FieldStorage()

if(form.has_key("data")):
	# print "Response"
	data, startDate, startTime, endDate, endTime, useFilteredData, pathOfFilteredData, entries, vis, ipversion = receiveData(form)

	flows, filePath = processData(data, startDate, endDate, startTime, endTime, useFilteredData, pathOfFilteredData)
	# print """<h3> Flows: """+str(len(flows))+"""</h3>"""
	graph = TreeMap(flows)
	# graph = ForceDirected(flows)
	# print graph
	# if entries == -1:
	# 	fl = toJson(flows)
	# else:
	# 	fl = toJson(flows[0:entries])

	if entries == -1:
		if ipversion == 4:
			fl = toJsonInt4(flows)
		elif ipversion == 6:
			fl = toJsonInt6(flows)
		elif ipversion == 2: #Both --> IPv4 and IPv6
			fl = toJson(flows)

		entries = len(flows)
		fl1 = flows
	else:
		if ipversion == 4:
			fl = toJsonInt4(flows[0:entries])
		elif ipversion == 6:
			fl = toJsonInt6(flows[0:entries])
		elif ipversion == 2: #Both --> IPv4 and IPv6
			fl = toJson(flows[0:entries])

		fl1 = flows[0:entries]

	print json.dumps({'flows': fl, 'path': filePath, 'totalFlows': len(flows)})
	# print fl1

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
