#!/usr/bin/python
import cgi, cgitb
from silk import *
import json
import os

print """Content-Type: text/html"""
print

operators = ['packets', 'bytes']

#Helper function to convert normal IPs to Silk format IP... IPv4Addr
def convertIP(values):
	values = values.split(',')
	for i in range(len(values)):
		val = values[i]
		values[i] = str(val)

	return values

def convertPort(values):
	values = values.split(',')
	for i in range(len(values)):
		val = values[i]
		values[i] = int(val)

	return values

def processDataRec(data, rec, firstFilter):
	query_keys = []
	keys_toRemove = []
	bool_sip = "none"
	bool_dip = "none"
	bool_sport = "none"
	bool_dport = "none"
	bool_bytes = "none"
	bool_packets = "none"
	mid_ip = 'none'
	mid_port = 'none'
	logic_ip = 'none'
	logic_port = 'none'
	logic_bytes = 'none'
	logic_packets = 'none'

	result = True


	for item in data:
		query_keys.append(item['name'])

	for item in data:
		name = item['name']
		if(name not in operators):
			if(name == 'sip'):
				sip_value = convertIP(item['value'])
				logic_ip = item['logic_filter']
				if(item['neg_filter'] == 'not'):
					# if(rec.sip != IPAddr(item['value'])):
					if(str(rec.sip) not in sip_value):
						bool_sip = True
					else:
						bool_sip = False
				else:
					# if(rec.sip == IPAddr(item['value'])):
					if(str(rec.sip) in sip_value):
						bool_sip = True	
					else:
						bool_sip = False
			
			elif(name == "dip"):
				logic_ip = item['logic_filter']
				mid_ip = item['midLogic_filter']

				dip_value = convertIP(item['value'])

				if(item['neg_filter'] == 'not'):
					# if(rec.dip != IPAddr(item['value'])):
					if(str(rec.dip) not in dip_value):
						bool_dip = True
					else:
						bool_dip = False
				else:
					# if(rec.dip == IPAddr(item['value'])):
					if(str(rec.dip) in dip_value):
						bool_dip = True	
					else:
						bool_dip = False

			elif(name == 'sport'):
				logic_port = item['logic_filter']
				# sport_value = item['value'].split(',')
				sport_value = convertPort(item['value'])

				if(item['neg_filter'] == 'not'):

					# if(rec.sport != int(item['value'])):
					if(rec.sport not in sport_value):
						bool_sport = True
					else:
						bool_sport = False
				else:
					# if(rec.sport == int(item['value'])):
					if(rec.sport in sport_value):
						bool_sport = True
					else:
						bool_sport = False	

			elif(name == "dport"):
				logic_port = item['logic_filter']
				mid_port = item['midLogic_filter']

				dport_value = convertPort(item['value'])

				if(item['neg_filter'] == 'not'):
					# if(rec.dport != int(item['value'])):
					if(rec.dport not in dport_value):
						bool_dport = True
					else:
						bool_dport = False
				else:
					# if(rec.dport == int(item['value'])):
					if(rec.dport in dport_value):
						bool_dport = True
					else:
						bool_dport = False
		else:
			try:
				if(name == "bytes"):
					logic_bytes = item['logic_filter']
					if(item['operator'] == "<"):
						if(rec.bytes < int(item['value'])):
							bool_bytes = True
						else:
							bool_bytes = False
					elif(item['operator'] == ">"):
						if(rec.bytes > int(item['value'])):
							bool_bytes = True
						else:
							bool_bytes = False
					elif(item['operator'] == "<="):
						if(rec.bytes <= int(item['value'])):
							bool_bytes = True
						else:
							bool_bytes = False
					elif(item['operator'] == ">="):
						if(rec.bytes >= int(item['value'])):
							bool_bytes = True
						else:
							bool_bytes = False
					elif(item['operator'] == "="):
						if(rec.bytes == int(item['value'])):
							bool_bytes = True
						else:
							bool_bytes = False
				
				elif(name == "packets"):
					logic_packets = item['logic_filter']
					if(item['operator'] == "<"):
						if(rec.packets < int(item['value'])):
							bool_packets = True
						else:
							bool_packets = False
					elif(item['operator'] == ">"):
						if(rec.packets > int(item['value'])):
							bool_packets = True
						else:
							bool_packets = False
					elif(item['operator'] == "<="):
						if(rec.packets <= int(item['value'])):
							bool_packets = True
						else:
							bool_packets = False
					elif(item['operator'] == ">="):
						if(rec.packets >= int(item['value'])):
							bool_packets = True
						else:
							bool_packets = False
					elif(item['operator'] == "="):
						if(rec.packets == int(item['value'])):
							bool_packets = True
						else:
							bool_packets = False
			except:
				if(name == "bytes"):
					logic_bytes = item['logic_filter']
					if(rec.bytes == int(item['value'])):
						bool_bytes = True
					else:
						bool_bytes = False
				elif(name == "packets"):
					logic_packets = item['logic_filter']
					if(rec.packets == int(item['value'])):
						bool_packets = True
					else:
						bool_packets = False

	keys_toRemove = query_keys[:]

	for item in query_keys:
		if(item == 'sip' and item in keys_toRemove):
			keys_toRemove.remove(item)
			if(firstFilter == 'sip'):
				if('dip' in keys_toRemove):
					keys_toRemove.remove('dip')
					if(mid_ip == 'and'):
						result = bool_sip and bool_dip
					elif(mid_ip == 'or'):
						result = bool_sip or bool_dip
				else:
					result = bool_sip
			else:
				if('dip' in keys_toRemove):
					keys_toRemove.remove('dip')
					if(logic_ip == 'and'):
						if(mid_ip == 'and'):
							result = result and (bool_sip and bool_dip)
						elif(mid_ip == 'or'):
							result = result and (bool_sip or bool_dip)
					elif(logic_ip == 'or'):
						if(mid_ip == 'and'):
							result = result or (bool_sip and bool_dip)
						elif(mid_ip == 'or'):
							result = result or (bool_sip or bool_dip)
				else:
					if(logic_ip == 'and'):
						result = result and bool_sip
					elif(logic_ip == 'or'):
						result = result or bool_sip

		elif(item == 'dip' and item in keys_toRemove):
			keys_toRemove.remove(item)
			if(firstFilter == 'sip'):
				if('sip' in keys_toRemove):
					keys_toRemove.remove('sip')
					if(mid_ip == 'and'):
						result = bool_sip and bool_dip
					elif(mid_ip == 'or'):
						result = bool_sip or bool_dip
				else:
					result = bool_dip
			else:
				if('sip' in keys_toRemove):
					keys_toRemove.remove('sip')
					if(logic_ip == 'and'):
						if(mid_ip == 'and'):
							result = result and (bool_sip and bool_dip)
						elif(mid_ip == 'or'):
							result = result and (bool_sip or bool_dip)
					elif(logic_ip == 'or'):
						if(mid_ip == 'and'):
							result = result or (bool_sip and bool_dip)
						elif(mid_ip == 'or'):
							result = result or (bool_sip or bool_dip)
				else:
					if(logic_ip == 'and'):
						result = result and bool_dip
					elif(logic_ip == 'or'):
						result = result or bool_dip

		elif(item == 'sport' and item in keys_toRemove):
			keys_toRemove.remove(item)
			if(firstFilter == 'sport'):
				if('dport' in keys_toRemove):
					keys_toRemove.remove('dport')
					if(mid_port == 'and'):
						result = bool_sport and bool_dport
					elif(mid_port == 'or'):
						result = bool_sport or bool_dport
				else:
					result = bool_sport
			else:
				if('dport' in keys_toRemove):
					keys_toRemove.remove('dport')
					if(logic_port == 'and'):
						if(mid_port == 'and'):
							result = result and (bool_sport and bool_dport)
						elif(mid_port == 'or'):
							result = result and (bool_sport or bool_dport)
					elif(logic_port == 'or'):
						if(mid_port == 'and'):
							result = result or (bool_sport and bool_dport)
						elif(mid_port == 'or'):
							result = result or (bool_sport or bool_dport)
				else:
					if(logic_port == 'and'):
						result = result and (bool_sport)
					elif(logic_port == 'or'):
						result = result or (bool_sport)

		elif(item == 'dport' and item in keys_toRemove):
			keys_toRemove.remove(item)
			if(firstFilter == 'sport'):
				if('sport' in keys_toRemove):
					keys_toRemove.remove('sport')
					if(mid_port == 'and'):
						result = bool_sport and bool_dport
					elif(mid_port == 'or'):
						result = bool_sport or bool_dport
				else:
					result = bool_dport
			else:
				if('sport' in keys_toRemove):
					keys_toRemove.remove('sport')
					if(logic_ip == 'and'):
						if(mid_ip == 'and'):
							result = result and (bool_sport and bool_dport)
						elif(mid_ip == 'or'):
							result = result and (bool_sport or bool_dport)
					elif(logic_ip == 'or'):
						if(mid_ip == 'and'):
							result = result or (bool_sport and bool_dport)
						elif(mid_ip == 'or'):
							result = result or (bool_sport or bool_dport)
				else:
					if(logic_port == 'and'):
						result = result and bool_dport
					elif(logic_port == 'or'):
						result = result or bool_dport

		elif(item == 'bytes' and item in keys_toRemove):
			keys_toRemove.remove(item)
			if(firstFilter == 'bytes'):
				result = bool_bytes
			else:
				if(logic_bytes == 'and'):
					result = result and (bool_bytes)
				elif(logic_bytes == 'or'):
					result = result or (bool_bytes)
		elif(item == 'packets' and item in keys_toRemove):
			keys_toRemove.remove(item)
			if(firstFilter == 'packets'):
				result = bool_packets
			else:
				if(logic_packets == 'and'):
					result = result and (bool_packets)
				elif(logic_packets == 'or'):
					result = result or (bool_packets)


	# print "sip: " + str(bool_sip)
	# print "dip: " + str(bool_dip)
	# print "sport: " + str(bool_sport)
	# print "dport: " + str(bool_dport)
	# print "bytes: " + str(bool_bytes)
	# print "packets: " + str(bool_packets)
	# print "mid_ip: " + mid_ip
	# print "mid_port: " + mid_port
	# print "result: " + str(result)
	return result

def receiveData(form):
	data = form.getvalue("data")
	firstFilter = form.getvalue("first")
	startDate = form.getvalue("start")
	endDate = form.getvalue("end")
	data = json.loads(data)
	data = data['data']

	return data, firstFilter, startDate, endDate


def processData(data, firstFilter, startDate, endDate):
	flows = []
	# start_date="2015/08/08", end_date="2015/08/08"
	for filename in FGlob(classname="all", type="all", start_date=startDate, end_date=endDate, site_config_file="/data/conf-v9/silk.conf", data_rootdir="/scratch/flow/rwflowpack"):
		for rec in silkfile_open(filename, READ): #read the flow file
			if(processDataRec(data, rec, firstFilter)):
				flows.append(rec)
	return flows

form = cgi.FieldStorage()

if(form.has_key("data")):
	print "Response"
	data, firstFilter, startDate, endDate = receiveData(form)
	flows = processData(data, firstFilter, startDate, endDate)
	print 'len Flows: ' + str(len(flows))
	for item in flows:
		print 'sip: ', item.sip, "---- dip: ", item.dip, "---- sport: ", item.sport
	print flows


else:
	print "There is no filter..."


# cmd = 'rwfilter --scidr=136.145.231.46 --sensor=S0 --type=all --protocol=1,6,17 --print-volume --threads=4 --pass-destination=stdout --site-config-file=/data/conf-v9/silk.conf | rwcut --fields=1,2,5,3 > test1.out'

# data = [{u'midLogic_filter': u'and', u'logic_filter': u'and', u'name': u'sip', u'value': u'136.145.231.9, 136.145.231.10', u'neg_filter': u''}, {u'midLogic_filter': u'and', u'logic_filter': u'and', u'name': u'dip', u'value': u'199.7.83.42', u'neg_filter': u''}, {u'midLogic_filter': u'and', u'logic_filter': u'and', u'name': u'sport', u'value': u'40790', u'neg_filter': u''}, {u'midLogic_filter': u'and', u'logic_filter': u'and', u'name': u'dport', u'value': u'53', u'neg_filter': u''}, {u'logic_filter': u'and', u'name': u'bytes', u'value': u'1'}, {u'logic_filter': u'and', u'name': u'packets', u'value': u'55'}]

# data = [{u'midLogic_filter': u'and', u'logic_filter': u'and', u'name': u'sip', u'value': u'136.145.231.9', u'neg_filter': u''}, {u'midLogic_filter': u'and', u'logic_filter': u'and', u'name': u'dip', u'value': u'136.145.180.232', u'neg_filter': u''}]

# data = [{u'midLogic_filter': u'and', u'logic_filter': u'and', u'name': u'sip', u'value': u'136.145.231.9', u'neg_filter': u''}]


# rec = {'sip': IPv4Addr('136.145.231.9'), 'protocol': 17, 'timeout_killed': False, 'dport': 53, 'output': 0, 'packets': 1L, 'bytes': 55L, 'uniform_packets': False, 'application': 0, 'sensor_id': 0, 'timeout_started': False, 'classtype_id': 1, 'nhip': IPv4Addr('136.145.195.141'), 'input': 0, 'sport': 40790, 'dip': IPv4Addr('199.7.83.42'), 'finnoack': False}


