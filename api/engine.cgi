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
	print form
	data = form.getvalue("data")
	data = json.loads(data)
	
	startDate = str(form.getvalue('from'))
	startTime = str(form.getvalue('starttime'))

	endDate = str(form.getvalue('to'))
	endTime = str(form.getvalue('endtime'))

	filteredData = data['filteredData']
	path 	= data['path']

	entries = form.getvalue('entries')

	if entries == "Other":
		entries = int(form.getvalue('otherEntries'))
	else:
		entries = int(entries)

	vis 	= int(form.getvalue('vis'))

	ipversion = int(form.getvalue('ipversion'))

	print ipversion

	data = data['data']


	return data, startDate, startTime, endDate, endTime, filteredData, path, entries, vis, ipversion

form = cgi.FieldStorage()

if(form.has_key("data")):
	#descomentar
	# printFilterPage()
	# /descomentar

	# print """<script> $('#pleaseWaitDialog').modal('show'); </script>"""
	
	data, startDate, startTime, endDate, endTime, useFilteredData, pathOfFilteredData, entries, vis, ipversion = receiveData(form)

	flows, filePath = processData(data, startDate, endDate, startTime, endTime, useFilteredData, pathOfFilteredData)

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
		
		elif vis == 5: #Cube
			print fl
		elif vis == 6:
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
