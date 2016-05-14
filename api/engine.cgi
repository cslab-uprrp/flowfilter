#!/usr/bin/python
import cgi, cgitb
from silk import *
import json
import os
import time
from webflow import *
from ian import *
from TreeMap import *
import tableView

print """Content-type: text/html"""
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
	printFilterPage()

	# print """<script> $('#pleaseWaitDialog').modal('show'); </script>"""
	
	data, startDate, endDate, useFilteredData, pathOfFilteredData, entries = receiveData(form)

	flows, filePath = processData(data, startDate, endDate, useFilteredData, pathOfFilteredData)

	if entries == -1:
		fl = toJson(flows)
		entries = len(flows)
	else:
		fl = toJson(flows[0:entries])

	print """<div class="container">
				<h3> Flows: """+str(len(flows))+"""</h3>
			 </div>
			 <script>
			 	console.log('data');
			 </script>
	"""
	print tableView.setTableValues%(1, entries, str(fl), len(flows))
	print tableView.sectionTableTag
	print tableView.initTableScript

elif form.has_key("entries"):
	info = form.getvalue("entries")
	info = json.loads(info)
	first = info['first']
	last = info['last']
	path = info['path']
	current_page = int(info['currentPage'])
	
	newFile = open('%s'%(path), 'r')
	filteredData = json.loads(newFile.read())
	filtereDflows = filteredData['flows']

	newFile.close()

	fl = json.dumps({'flows': filtereDflows[first:last]})
	
	printFilterPage()

	print """<div class="container"> 
				<h3> Flows: """+str(len(filtereDflows))+"""</h3> 
			 </div>
			 <script>
			 	console.log('entries');
			 </script>
	"""

	print tableView.setFilePath%(path)
	print tableView.setTableValues%(current_page, (last - first), str(fl), len(filtereDflows))
	print tableView.sectionTableTag
	print tableView.initTableScript

	hideLoading()
	showViz()

else:
	printFilterPage()
	print "There is no filter..."
