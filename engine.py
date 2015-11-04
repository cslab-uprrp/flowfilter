#!/usr/bin/python
import cgi, cgitb
from silk import *
import json
import os

print """Content-Type: text/html"""
print

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

	return result

