#!/usr/bin/python
import cgi, cgitb
from silk import *
import json
import os
import time
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
	data = data['data']

	return data, startDate, endDate, filteredData, path

form = cgi.FieldStorage()

# f = open("temp.txt", "wb")

if(form.has_key("data")):
	printFilterPage()

	# print """<script> $('#pleaseWaitDialog').modal('show'); </script>"""
	
	data, startDate, endDate, useFilteredData, pathOfFilteredData = receiveData(form)

	flows, filePath = processData(data, startDate, endDate, useFilteredData, pathOfFilteredData)

	print """<h3> Flows: """+str(len(flows))+"""</h3>"""

	# graph = TreeMap(flows)
	# graph = ForceDirected(flows)

	# print len(flows)

	pages = len(flows)/50
	pagesRem = int(50*(len(flows)/50.0 - pages))


	print """ <ul class="pagination"> """

	for i in range(pages):
		print """ <li><a href="#">%d</a></li> """%(i+1)

	if pagesRem:
		print """ <li><a href="#">%d</a></li> """%(pages + 1)
	# for j in range()

	print """ </ul> """
	# print """
	# 	  <ul class="pagination">
	# 	    <li><a href="#">1</a></li>
	# 	    <li><a href="#">2</a></li>
	# 	    <li><a href="#">3</a></li>
	# 	    <li><a href="#">4</a></li>
	# 	    <li><a href="#">5</a></li>
	# 	  </ul>
	# """

	# print '<br/>'
	for fl in flows:
		print '<br/>'
		print fl.sip
		print fl.sport

	# print 'blaba'
	# time.sleep(3)
	# print """<script> $('#pleaseWaitDialog').modal('hide'); </script>"""

else:
	printFilterPage()
	print "There is no filter..."
