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
	data = data['data']

	return data, startDate, endDate

form = cgi.FieldStorage()

# f = open("temp.txt", "wb")

if(form.has_key("data")):
	printFilterPage()
	# f.write("1baba")
	# print """<script> $('#pleaseWaitDialog').modal('show'); </script>"""
	data, startDate, endDate = receiveData(form)
	# print data, startDate, endDate
	flows = processData(data, startDate, endDate)
	# f.write("2baba")
	print """<h3> Flows: """+str(len(flows))+"""</h3>"""
	# print flows
	# for item in flows:
		# print item.sip
		# print "||"
	# graph = TreeMap(flows)
	# graph = ForceDirected(flows)
	# print graph
	print len(flows)
	# f.write(len(flows))
	print '<br/>'
	for fl in flows:
		print fl.sip
		# f.write(fl.dip)
	# f.write(type(flowList))
	# f.write(len(flowList))
	# f.write("3baba")
	print 'blaba'
	# f.close()
	# print flows


	# time.sleep(3)
	# print """<script> $('#pleaseWaitDialog').modal('hide'); </script>"""

else:
	printFilterPage()
	print "There is no filter..."
