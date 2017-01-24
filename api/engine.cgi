#!/usr/bin/python
import cgi, cgitb
from silk import *
import json
import os
import time
from webflow import *
sys.path.append("Visualizations")
from ian import * #ForceDirected
from TreeMap import *
from GeoIP2 import *
import tableView
from pieces import *

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
	vis = int(data['vis'])
	data = data['data']

	return data, startDate, endDate, filteredData, path, entries, vis

form = cgi.FieldStorage()

if(form.has_key("data")):
	#descomentar
	printFilterPage()
	# /descomentar

	# print """<script> $('#pleaseWaitDialog').modal('show'); </script>"""
	
	data, startDate, endDate, useFilteredData, pathOfFilteredData, entries, vis = receiveData(form)

	flows, filePath = processData(data, startDate, endDate, useFilteredData, pathOfFilteredData)
	if entries == -1:
		fl = toJson(flows)
		entries = len(flows)
		fl1 = flows
	else:
		fl = toJson(flows[0:entries])
		fl1 = flows[0:entries]


	#descomentar
	print """<div class="container">
				<h3> Flows: """+str(len(flows))+"""</h3>
			 </div>
			 <script>
			 	console.log('data');
			 </script>
	"""

	print """<script> 
	   		 	var element = document.getElementById('selectVis');
    		 	element.value = %d;
    		 </script>
    """%(vis)

    # /descomentar

	if len(flows) != 0:

		if vis == 1:
				print tableView.setTableValues%(1, entries, str(fl), len(flows))
				print tableView.sectionTableTag
				print tableView.initTableScript

		elif vis == 2:
			print ForceDirected(fl1)

		elif vis == 3:
			print TreeMap(fl1)
		
		elif vis == 4:
			print GeoIPVis(fl1)
		
		elif vis == 5:
			print fl

		
		if vis != 1:
			setPieces(1, entries, str(fl), len(flows))
	else:
		zeroFlows()

elif form.has_key("entries"):
	info = form.getvalue("entries")
	info = json.loads(info)
	first = info['first']
	last = info['last']
	path = info['path']
	vis = int(info['vis'])

	current_page = int(info['currentPage'])
	
	newFile = open('%s'%(path), 'r')
	filteredData = json.loads(newFile.read())
	filtereDflows = filteredData['flows']

	newFile.close()

	fl = json.dumps({'flows': filtereDflows[first:last]})

	#descomentar
	printFilterPage()
	# /descomentar

	fl1 = filtereDflows[first:last]

	if vis == 1:
			print tableView.setFilePath%(path)
			print tableView.setTableValues%(current_page, (last - first), str(fl), len(filtereDflows))
			print tableView.sectionTableTag
			print tableView.initTableScript

	elif vis == 2:
		print ForceDirected(fl1)

	elif vis == 3:
		print TreeMap(fl1)
	
	elif vis == 4:
		print GeoIPVis(fl1)

	elif vis == 5:
		print fl

	
	if vis != 1:
		print setFilePath%(path)
		setPieces(current_page, (last - first), str(fl), len(filtereDflows))

	# descomentar
	print """<div class="container"> 
				<h3> Flows: """+str(len(filtereDflows))+"""</h3> 
			 </div>
			 <script>
			 	console.log('entries');
			 </script>
	"""

	print """<script> 
	   		 	var element = document.getElementById('selectVis');
    		 	element.value = %d;
    		 </script>
    """%(vis)

    # /descomentar

	# print tableView.setFilePath%(path)
	# print tableView.setTableValues%(current_page, (last - first), str(fl), len(filtereDflows))
	# print tableView.sectionTableTag
	# print tableView.initTableScript

	#descomentar
	hideLoading()
	#/descomentar
	showViz()

else:
	printFilterPage()
	print "There is no filter..."
