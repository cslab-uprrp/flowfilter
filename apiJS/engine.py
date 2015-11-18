#!/usr/bin/python
from silk import *
import json

operators = ['packets', 'bytes']

firstDict = {
	'dip': 'sip',
	'dport': 'sport',
	'sip': 'sip',
	'sport': 'sport',
	'input': 'input',
	'output': 'input',
	'srcAS': 'srcAS',
	'dstAS': 'srcAS'
}

#This function will print out the filter selector tool
def printFilterPage():
	f = open('webpage/index.html', 'r')
	f = f.read()
	print f

#Helper function to convert each IP into a string to be compare with the Silk IP
def convertIP(values):
	values = values.split(',') #splitting the IPs because it can be a list of IPs
	for i in range(len(values)):
		val = values[i]
		values[i] = str(val)

	return values

#Helper function to convert the ports numbers to int 
def convertToInt(values):
	values = values.split(',')
	for i in range(len(values)):
		val = values[i]
		values[i] = int(val)

	return values

#This function is the one that will iterate through all the flows from startDate to endDate
def processData(data, startDate, endDate):
	flows = [] #List to save all the flows that meet the filters 
	for filename in FGlob(classname="all", type="all", start_date=startDate, end_date=endDate, site_config_file="/data/conf-v9/silk.conf", data_rootdir="/scratch/flow/rwflowpack"):
		for rec in silkfile_open(filename, READ): #reading the flow file
			if(processDataRec(data, rec)): #if the flow (rec) meet the filters then I will add it to the flows list
				flows.append(rec)
	return flows

#This function will process an specific flow to see if it meets the filters
def processDataRec(data, rec):
	#This is the first selected filter in the tool, I need to know which is the first filter 
	#because it would not need the first logic in the querry that I am going to construct
	firstFilter = data[0]['name']
	if(firstFilter in firstDict):
		firstFilter = firstDict[firstFilter]

	query_keys = [] #This list will save the filters that the user selected in the selector tool
	keys_toRemove = [] #this list is the same as query_keys but i will be removing keys from this list in a loop
	
	#The following boolean variables will say if the current flow meets each filter, None means that the filter was not selected
	#by the user
	bool_sip = "none"
	bool_dip = "none"
	bool_sport = "none"
	bool_dport = "none"
	bool_bytes = "none"
	bool_packets = "none"
	bool_input = "none"
	bool_output = "none"
	bool_sAS = "none"
	bool_dAS = "none"
	mid_ip = 'none'
	mid_port = 'none'
	mid_interface = "none"
	mid_AS = "none"
	logic_ip = 'none'
	logic_port = 'none'
	logic_bytes = 'none'
	logic_packets = 'none'
	logic_interface = "none"
	logic_AS = "none"

	result = True

	#Saving the selected name of filters in the query_keys list
	for item in data:
		query_keys.append(item['name'])

	#This for will be going through all the filters selected by the users and will check if the current flow
	#meet them or not, updating the boolean variables
	for item in data: #for each item in the data dictionary
		name = item['name'] #name of the filter
		#If the current filter is not in the list of operators ['packets', 'bytes'], they are going to be procces a bit different
		if(name not in operators): 
			#if the filter is sip (source ip), then it will get the values from the dictionary and will convert each ip to string,
			#it will set the logic of the filter, if it is and/or (this will be used later)
			if(name == 'sip'):
				sip_value = convertIP(item['value'])
				logic_ip = item['logic_filter']
				#If the filter has a negation, then it will check if the sip of the current flow is not in the list of values of the sip
				#introduced by the user.
				if(item['neg_filter'] == 'not'):
					if(str(rec.sip) not in sip_value):
						bool_sip = True
					else:
						bool_sip = False
				#else, it will check if the sip of the current flow is in the list of values
				#of the sip introduced by the user
				else:
					if(str(rec.sip) in sip_value):
						bool_sip = True	
					else:
						bool_sip = False
			
			#if the filter is dip (destination ip), then it will get the values from the dictionary and will convert each ip 
			#to string, then it will set the logic of the filter and the mid logic (the one that is between sip and dip), 
			#if it is and/or (this will be used later)
			elif(name == "dip"):
				logic_ip = item['logic_filter']
				mid_ip = item['midLogic_filter']

				dip_value = convertIP(item['value'])

				#If the filter has a negation, then it will check if the sip of the current flow is not in the list of values 
				#of the dip introduced by the user.
				if(item['neg_filter'] == 'not'):
					if(str(rec.dip) not in dip_value):
						bool_dip = True
					else:
						bool_dip = False
				#else, it will check if the sip of the current flow is in the list of values
				#of the dip introduced by the user
				else:
					if(str(rec.dip) in dip_value):
						bool_dip = True	
					else:
						bool_dip = False

			#if the filter is sport (source port), then it will get the values from the dictionary and will convert each port 
			#to int, then it will set the logic of the filter, if it is and/or (this will be used later)
			elif(name == 'sport'):
				logic_port = item['logic_filter']
				sport_value = convertToInt(item['value'])

				#If the filter has a negation, then it will check if the sport of the current flow is not in the list of values 
				#of the sport introduced by the user.
				if(item['neg_filter'] == 'not'):
					if(rec.sport not in sport_value):
						bool_sport = True
					else:
						bool_sport = False
				#else, it will check if the sip of the current flow is in the list of values
				#of the sport introduced by the user
				else:
					if(rec.sport in sport_value):
						bool_sport = True
					else:
						bool_sport = False	

			#if the filter is dport (destination port), then it will get the values from the dictionary and will convert each port 
			#to int, then it will set the logic of the filter and the mid logic (the one that is between sport and dport), 
			#if it is and/or (this will be used later)
			elif(name == "dport"):
				logic_port = item['logic_filter']
				mid_port = item['midLogic_filter']

				dport_value = convertToInt(item['value'])

				#If the filter has a negation, then it will check if the dport of the current flow is not in the list of values 
				#of the dport introduced by the user.
				if(item['neg_filter'] == 'not'):
					if(rec.dport not in dport_value):
						bool_dport = True
					else:
						bool_dport = False
				#else, it will check if the dip of the current flow is in the list of values
				#of the dport introduced by the user
				else:
					if(rec.dport in dport_value):
						bool_dport = True
					else:
						bool_dport = False

			#if the filter is input (input interface), then it will get the values from the dictionary and will convert each value 
			#to int, then it will set the logic of the filter then it will set the logic of the filter, if it is and/or 
			#(this will be used later)
			elif(name == "input"):
				logic_interface = item['logic_filter']
				input_value = convertToInt(item['value'])

				#If the filter has a negation, then it will check if the input of the current flow is not in the list of values 
				#of the input introduced by the user.
				if(item['neg_filter'] == 'not'):
					if(rec.input not in input_value):
						bool_input = True
					else:
						bool_input = False
				#else, it will check if the input of the current flow is in the list of values
				#of the input introduced by the user
				else:
					if(rec.input in input_value):
						bool_input = True
					else:
						bool_input = False	

			#if the filter is output (output interface), then it will get the values from the dictionary and will convert each 
			#output to int, then it will set the logic of the filter and the mid logic (the one that is between input and output), 
			#if it is and/or (this will be used later)
			elif(name == "output"):
				logic_interface = item['logic_filter']
				mid_interface = item['midLogic_filter']

				output_value = convertToInt(item['value'])

				#If the filter has a negation, then it will check if the output of the current flow is not in the list of values 
				#of the output introduced by the user.
				if(item['neg_filter'] == 'not'):
					if(rec.output not in output_value):
						bool_output = True
					else:
						bool_output = False
				
				#else, it will check if the output of the current flow is in the list of values
				#of the output introduced by the user
				else:
					if(rec.output in output_value):
						bool_output = True
					else:
						bool_output = False

		#else, if the filter is bytes or packets, it will check if the operator is <,>,<=,>=,=, after that it will make the
		#operation using the bytes or packets of the current flow and the bytes or packets introduced by the user
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

	#This for loop will do the query, using the different logics for each filter
	for item in query_keys:
		#If the item is sip and it has not been process then we remove the item from the list keys_toRemove, because we do not want
		#to process an item twice.
		if(item == 'sip' and item in keys_toRemove):
			keys_toRemove.remove(item)
			#If the item is the first filter, then we do not have to take in consideration the first logic
			if(firstFilter == 'sip'):
				#If the item's partner, in this case dip, is in keys_toRemove, meaning that it has not been process, then
				#we check if the middle logic is and/or an according to the result we execute the querry saving the answer,
				#true or false, in result
				if('dip' in keys_toRemove):
					keys_toRemove.remove('dip')
					if(mid_ip == 'and'):
						result = bool_sip and bool_dip
					elif(mid_ip == 'or'):
						result = bool_sip or bool_dip
				#else, the result is just that first item
				else:
					result = bool_sip
			#else, if the item is not the first filter
			else:
				#we check if the item's partner, in this case dip, is in keys_toRemove, meaning that it has not been process, 
				#then we check if the middle logic is and/or an according to the result we execute the querry with the old value
				#of result (since is not the first item, it should contain something), and/or (depending on the logic of that
				#expecific filter) the result of bool_sip and/or (the middle logic) bool_dip. We save the answer, true or false,
				#in result.
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
				#else, if the item's partner, in this case dip, is not in keys_toRemove, then the querry will be the old value of
				#result and/or (depending on the logic of that expecific filter) bool_sip
				else:
					if(logic_ip == 'and'):
						result = result and bool_sip
					elif(logic_ip == 'or'):
						result = result or bool_sip

		#If the item is dip and it has not been process then we remove the item from the list keys_toRemove, because we do not want
		#to process an item twice.
		elif(item == 'dip' and item in keys_toRemove):
			keys_toRemove.remove(item)
			#If the item is the first filter, then we do not have to take in consideration the first logic
			#Here we are checking if the sip is the first item, instead of dip, because if dip is the first in the webpage, 
			#since is a template, in the html, then we are adding sip anyways but is hidden and in the list it will be the first
			if(firstFilter == 'sip'):
				#If the item's partner, in this case sip, is in keys_toRemove, meaning that it has not been process, then
				#we check if the middle logic is and/or an according to the result we execute the querry saving the answer,
				#true or false, in result
				if('sip' in keys_toRemove):
					keys_toRemove.remove('sip')
					if(mid_ip == 'and'):
						result = bool_sip and bool_dip
					elif(mid_ip == 'or'):
						result = bool_sip or bool_dip
				#else, the result is just that first item
				else:
					result = bool_dip
			#else, if the item is not the first filter
			else:
				#we check if the item's partner, in this case sip, is in keys_toRemove, meaning that it has not been process, 
				#then we check if the middle logic is and/or an according to the result we execute the querry with the old value
				#of result (since is not the first item, it should contain something), and/or (depending on the logic of that
				#expecific filter) the result of bool_sip and/or (the middle logic) bool_dip. We save the answer, true or false,
				#in result.
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
				#else, if the item's partner, in this case sip, is not in keys_toRemove, then the querry will be the old value of
				#result and/or (depending on the logic of that expecific filter) bool_dip
				else:
					if(logic_ip == 'and'):
						result = result and bool_dip
					elif(logic_ip == 'or'):
						result = result or bool_dip

		#If the item is sport and it has not been process then we remove the item from the list keys_toRemove, because we do not want
		#to process an item twice.
		elif(item == 'sport' and item in keys_toRemove):
			keys_toRemove.remove(item)
			#If the item is the first filter, then we do not have to take in consideration the first logic
			if(firstFilter == 'sport'):
				#If the item's partner, in this case dport, is in keys_toRemove, meaning that it has not been process, then
				#we check if the middle logic is and/or an according to the result we execute the querry saving the answer,
				#true or false, in result
				if('dport' in keys_toRemove):
					keys_toRemove.remove('dport')
					if(mid_port == 'and'):
						result = bool_sport and bool_dport
					elif(mid_port == 'or'):
						result = bool_sport or bool_dport
				#else, the result is just that first item
				else:
					result = bool_sport
			#else, if the item is not the first filter
			else:
				#we check if the item's partner, in this case dport, is in keys_toRemove, meaning that it has not been process, 
				#then we check if the middle logic is and/or an according to the result we execute the querry with the old value
				#of result (since is not the first item, it should contain something), and/or (depending on the logic of that
				#expecific filter) the result of bool_sip and/or (the middle logic) bool_dip. We save the answer, true or false,
				#in result.
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
				#else, if the item's partner, in this case dport, is not in keys_toRemove, then the querry will be the old value of
				#result and/or (depending on the logic of that expecific filter) bool_sport
				else:
					if(logic_port == 'and'):
						result = result and (bool_sport)
					elif(logic_port == 'or'):
						result = result or (bool_sport)

		#If the item is dport and it has not been process then we remove the item from the list keys_toRemove, because we do not want
		#to process an item twice.
		elif(item == 'dport' and item in keys_toRemove):
			keys_toRemove.remove(item)
			#If the item is the first filter, then we do not have to take in consideration the first logic
			#Here we are checking if the sport is the first item, instead of dport, because if dport is the first in the webpage, 
			#since is a template, in the html, then we are adding sport anyways but is hidden and in the list it will be the first
			if(firstFilter == 'sport'):
				if('sport' in keys_toRemove):
					keys_toRemove.remove('sport')
					if(mid_port == 'and'):
						result = bool_sport and bool_dport
					elif(mid_port == 'or'):
						result = bool_sport or bool_dport
				#else, the result is just that first item
				else:
					result = bool_dport
			#else, if the item is not the first filter
			else:
				#we check if the item's partner, in this case sport, is in keys_toRemove, meaning that it has not been process, 
				#then we check if the middle logic is and/or an according to the result we execute the querry with the old value
				#of result (since is not the first item, it should contain something), and/or (depending on the logic of that
				#expecific filter) the result of bool_sip and/or (the middle logic) bool_dip. We save the answer, true or false,
				#in result.
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
				#else, if the item's partner, in this case sport, is not in keys_toRemove, then the querry will be the old value of
				#result and/or (depending on the logic of that expecific filter) bool_dport
				else:
					if(logic_port == 'and'):
						result = result and bool_dport
					elif(logic_port == 'or'):
						result = result or bool_dport

		#If the item is input and it has not been process then we remove the item from the list keys_toRemove, because we do not want
		#to process an item twice.
		elif(item == 'input' and item in keys_toRemove):
			keys_toRemove.remove(item)
			#If the item is the first filter, then we do not have to take in consideration the first logic
			if(firstFilter == 'input'):
				#If the item's partner, in this case output, is in keys_toRemove, meaning that it has not been process, then
				#we check if the middle logic is and/or an according to the result we execute the querry saving the answer,
				#true or false, in result
				if('output' in keys_toRemove):
					keys_toRemove.remove('output')
					if(mid_interface == 'and'):
						result = bool_input and bool_output
					elif(mid_interface == 'or'):
						result = bool_input or bool_output
				#else, the result is just that first item
				else:
					result = bool_input
			#else, if the item is not the first filter
			else:
				#we check if the item's partner, in this case output, is in keys_toRemove, meaning that it has not been process, 
				#then we check if the middle logic is and/or an according to the result we execute the querry with the old value
				#of result (since is not the first item, it should contain something), and/or (depending on the logic of that
				#expecific filter) the result of bool_input and/or (the middle logic) bool_output. We save the answer, true or false,
				#in result.
				if('output' in keys_toRemove):
					keys_toRemove.remove('output')
					if(logic_interface == 'and'):
						if(mid_interface == 'and'):
							result = result and (bool_input and bool_output)
						elif(mid_interface == 'or'):
							result = result and (bool_input or bool_output)
					elif(logic_interface == 'or'):
						if(mid_interface == 'and'):
							result = result or (bool_input and bool_output)
						elif(mid_interface == 'or'):
							result = result or (bool_input or bool_input)
				#else, if the item's partner, in this case output, is not in keys_toRemove, then the querry will be the old value of
				#result and/or (depending on the logic of that expecific filter) bool_input
				else:
					if(logic_interface == 'and'):
						result = result and bool_input
					elif(logic_interface == 'or'):
						result = result or bool_input

		#If the item is output and it has not been process then we remove the item from the list keys_toRemove, because we do not want
		#to process an item twice.
		elif(item == 'output' and item in keys_toRemove):
			keys_toRemove.remove(item)
			#If the item is the first filter, then we do not have to take in consideration the first logic
			#Here we are checking if the input is the first item, instead of output, because if output is the first in the webpage, 
			#since is a template, in the html, then we are adding input anyways but is hidden and in the list it will be the first
			if(firstFilter == 'input'):
				if('input' in keys_toRemove):
					keys_toRemove.remove('input')
					if(mid_interface == 'and'):
						result = bool_input and bool_output
					elif(mid_interface == 'or'):
						result = bool_input or bool_output
				#else, the result is just that first item
				else:
					result = bool_output
			#else, if the item is not the first filter
			else:
				#we check if the item's partner, in this case input, is in keys_toRemove, meaning that it has not been process, 
				#then we check if the middle logic is and/or an according to the result we execute the querry with the old value
				#of result (since is not the first item, it should contain something), and/or (depending on the logic of that
				#expecific filter) the result of bool_input and/or (the middle logic) bool_output. We save the answer, true or false,
				#in result.
				if('input' in keys_toRemove):
					keys_toRemove.remove('input')
					if(logic_interface == 'and'):
						if(mid_interface == 'and'):
							result = result and (bool_input and bool_output)
						elif(mid_interface == 'or'):
							result = result and (bool_input or bool_output)
					elif(logic_interface == 'or'):
						if(mid_interface == 'and'):
							result = result or (bool_input and bool_output)
						elif(mid_interface == 'or'):
							result = result or (bool_input or bool_output)
				#else, if the item's partner, in this case input, is not in keys_toRemove, then the querry will be the old value of
				#result and/or (depending on the logic of that expecific filter) bool_output
				else:
					if(logic_interface == 'and'):
						result = result and bool_output
					elif(logic_interface == 'or'):
						result = result or bool_output


		#If the item is bytes and it has not been process then we remove the item from the list keys_toRemove, because we do not want
		#to process an item twice.
		elif(item == 'bytes' and item in keys_toRemove):
			keys_toRemove.remove(item)
			#If the item is the first filter, then we do not have to take in consideration the first logic
			if(firstFilter == 'bytes'):
				result = bool_bytes
			#else, if the item is not the first filter
			else:
				#then the querry will be the old value of result and/or (depending on the logic of that expecific filter)
				#bool_bytes
				if(logic_bytes == 'and'):
					result = result and (bool_bytes)
				elif(logic_bytes == 'or'):
					result = result or (bool_bytes)

		#If the item is packets and it has not been process then we remove the item from the list keys_toRemove, because we do not want
		#to process an item twice.
		elif(item == 'packets' and item in keys_toRemove):
			keys_toRemove.remove(item)
			#If the item is the first filter, then we do not have to take in consideration the first logic
			if(firstFilter == 'packets'):
				result = bool_packets
			#else, if the item is not the first filter
			else:
				#then the querry will be the old value of result and/or (depending on the logic of that expecific filter)
				#bool_packets
				if(logic_packets == 'and'):
					result = result and (bool_packets)
				elif(logic_packets == 'or'):
					result = result or (bool_packets)

	return result

