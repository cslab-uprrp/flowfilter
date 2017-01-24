from geoip import geolite2
from silk import *
from silk import silk
import datetime
from MapClass import Map

def GeoIPVis(data):
	# print len(data)
	dict = {}
	SrcNotInGeoIP = {}
	DstNotInGeoIP = {}
	countryCodes = {"BD": "BGD", "BE": "BEL", "BF": "BFA", "BG": "BGR", "BA": "BIH", "BB": "BRB", "WF": "WLF", "BL": "BLM", "BM": "BMU", "BN": "BRN", "BO": "BOL", "BH": "BHR", "BI": "BDI", "BJ": "BEN", "BT": "BTN", "JM": "JAM", "BV": "BVT", "BW": "BWA", "WS": "WSM", "BQ": "BES", "BR": "BRA", "BS": "BHS", "JE": "JEY", "BY": "BLR", "BZ": "BLZ", "RU": "RUS", "RW": "RWA", "RS": "SRB", "TL": "TLS", "RE": "REU", "TM": "TKM", "TJ": "TJK", "RO": "ROU", "TK": "TKL", "GW": "GNB", "GU": "GUM", "GT": "GTM", "GS": "SGS", "GR": "GRC", "GQ": "GNQ", "GP": "GLP", "JP": "JPN", "GY": "GUY", "GG": "GGY", "GF": "GUF", "GE": "GEO", "GD": "GRD", "GB": "GBR", "GA": "GAB", "SV": "SLV", "GN": "GIN", "GM": "GMB", "GL": "GRL", "GI": "GIB", "GH": "GHA", "OM": "OMN", "TN": "TUN", "JO": "JOR", "HR": "HRV", "HT": "HTI", "HU": "HUN", "HK": "HKG", "HN": "HND", "HM": "HMD", "VE": "VEN", "PR": "PRI", "PS": "PSE", "PW": "PLW", "PT": "PRT", "SJ": "SJM", "PY": "PRY", "IQ": "IRQ", "PA": "PAN", "PF": "PYF", "PG": "PNG", "PE": "PER", "PK": "PAK", "PH": "PHL", "PN": "PCN", "PL": "POL", "PM": "SPM", "ZM": "ZMB", "EH": "ESH", "EE": "EST", "EG": "EGY", "ZA": "ZAF", "EC": "ECU", "IT": "ITA", "VN": "VNM", "SB": "SLB", "ET": "ETH", "SO": "SOM", "ZW": "ZWE", "SA": "SAU", "ES": "ESP", "ER": "ERI", "ME": "MNE", "MD": "MDA", "MG": "MDG", "MF": "MAF", "MA": "MAR", "MC": "MCO", "UZ": "UZB", "MM": "MMR", "ML": "MLI", "MO": "MAC", "MN": "MNG", "MH": "MHL", "MK": "MKD", "MU": "MUS", "MT": "MLT", "MW": "MWI", "MV": "MDV", "MQ": "MTQ", "MP": "MNP", "MS": "MSR", "MR": "MRT", "IM": "IMN", "UG": "UGA", "TZ": "TZA", "MY": "MYS", "MX": "MEX", "IL": "ISR", "FR": "FRA", "IO": "IOT", "SH": "SHN", "FI": "FIN", "FJ": "FJI", "FK": "FLK", "FM": "FSM", "FO": "FRO", "NI": "NIC", "NL": "NLD", "NO": "NOR", "NA": "NAM", "VU": "VUT", "NC": "NCL", "NE": "NER", "NF": "NFK", "NG": "NGA", "NZ": "NZL", "NP": "NPL", "NR": "NRU", "NU": "NIU", "CK": "COK", "XK": "XKX", "CI": "CIV", "CH": "CHE", "CO": "COL", "CN": "CHN", "CM": "CMR", "CL": "CHL", "CC": "CCK", "CA": "CAN", "CG": "COG", "CF": "CAF", "CD": "COD", "CZ": "CZE", "CY": "CYP", "CX": "CXR", "CR": "CRI", "CW": "CUW", "CV": "CPV", "CU": "CUB", "SZ": "SWZ", "SY": "SYR", "SX": "SXM", "KG": "KGZ", "KE": "KEN", "SS": "SSD", "SR": "SUR", "KI": "KIR", "KH": "KHM", "KN": "KNA", "KM": "COM", "ST": "STP", "SK": "SVK", "KR": "KOR", "SI": "SVN", "KP": "PRK", "KW": "KWT", "SN": "SEN", "SM": "SMR", "SL": "SLE", "SC": "SYC", "KZ": "KAZ", "KY": "CYM", "SG": "SGP", "SE": "SWE", "SD": "SDN", "DO": "DOM", "DM": "DMA", "DJ": "DJI", "DK": "DNK", "VG": "VGB", "DE": "DEU", "YE": "YEM", "DZ": "DZA", "US": "USA", "UY": "URY", "YT": "MYT", "UM": "UMI", "LB": "LBN", "LC": "LCA", "LA": "LAO", "TV": "TUV", "TW": "TWN", "TT": "TTO", "TR": "TUR", "LK": "LKA", "LI": "LIE", "LV": "LVA", "TO": "TON", "LT": "LTU", "LU": "LUX", "LR": "LBR", "LS": "LSO", "TH": "THA", "TF": "ATF", "TG": "TGO", "TD": "TCD", "TC": "TCA", "LY": "LBY", "VA": "VAT", "VC": "VCT", "AE": "ARE", "AD": "AND", "AG": "ATG", "AF": "AFG", "AI": "AIA", "VI": "VIR", "IS": "ISL", "IR": "IRN", "AM": "ARM", "AL": "ALB", "AO": "AGO", "AQ": "ATA", "AS": "ASM", "AR": "ARG", "AU": "AUS", "AT": "AUT", "AW": "ABW", "IN": "IND", "AX": "ALA", "AZ": "AZE", "IE": "IRL", "ID": "IDN", "UA": "UKR", "QA": "QAT", "MZ": "MOZ"}

	for it in data:
		try:
			item = Map(it)
		except:
			item = it
		if not(dict.has_key(item.sip)):
			srcIP = geolite2.lookup(str(item.sip))
			if(srcIP is not None):
				locSIP = srcIP.location
				if(locSIP is not None):
					srcLat = locSIP[0]
					srcLon = locSIP[1]
					dstIP = geolite2.lookup(str(item.dip))
					if(dstIP is not None):
						locDIP = dstIP.location
						if(locDIP is not None):
							dstLat = locDIP[0]
							dstLon = locDIP[1]
							country  = dstIP.country
							if (countryCodes.has_key(country)):
								dict[item.sip] = {'latSIP': str(srcLat), 'lonSIP': str(srcLon), 'dip' : [item.dip], 'dipbytes': [item.bytes], 'dipCountry' : [countryCodes[country]], 'latDIP': [dstLat], 'lonDIP': [dstLon], 'bytes' : item.bytes}

			elif(srcIP is None or locSIP is None):
				if not(SrcNotInGeoIP.has_key(item.sip)):
					SrcNotInGeoIP[item.sip] = {'dip' : [item.dip], 'dipbytes' : [item.bytes]}
				else:
					if not(item.dip in SrcNotInGeoIP[item.sip]['dip']): # If not in source ip array
						SrcNotInGeoIP[item.sip]['dip'].append(item.dip)
						SrcNotInGeoIP[item.sip]['dipbytes'].append(item.bytes)
					else:
						index = SrcNotInGeoIP[item.sip]['dip'].index(item.dip)
						SrcNotInGeoIP[item.sip]['dipbytes'][index] += item.bytes
		else:
			dict[item.sip]['bytes'] += item.bytes
			if not(item.dip in dict[item.sip]['dip']):
				dstIP = geolite2.lookup(str(item.dip))
				if(dstIP is not None):
					locDIP = dstIP.location
					if(locDIP is not None):
						dstLat = locDIP[0]
						dstLon = locDIP[1]
						country  = dstIP.country
						dict[item.sip]['dip'].append(item.dip)
						dict[item.sip]['dipbytes'].append(item.bytes)
						dict[item.sip]['latDIP'].append(dstLat)
						dict[item.sip]['lonDIP'].append(dstLon)
						if (countryCodes.has_key(country)):
							dict[item.sip]['dipCountry'].append(countryCodes[country])

				elif(srcIP is None or locSIP is None or locDIP is None):
					if not(DstNotInGeoIP.has_key(item.sip)):
						DstNotInGeoIP[item.sip] = {'dip' : [item.dip], 'dipbytes' : [item.bytes]}
					else:
						if not(item.dip in DstNotInGeoIP[item.sip]['dip']):
							DstNotInGeoIP[item.sip]['dip'].append(item.dip)
							DstNotInGeoIP[item.sip]['dipbytes'].append(item.bytes)
						else:
							index = DstNotInGeoIP[item.sip]['dip'].index(item.dip)
							DstNotInGeoIP[item.sip]['dipbytes'][index] += item.bytes
	# print dict
	countryBytes = {}
	for item in dict:
		for i in range(0, len(dict[item]['dip']), 1):
			if not(countryBytes.has_key(dict[item]['dipCountry'][i])):
				countryBytes[dict[item]['dipCountry'][i]] = {'countryID': dict[item]['dipCountry'][i], 'countryBytes' : dict[item]['dipbytes'][i]}
			else:
				countryBytes[dict[item]['dipCountry'][i]]['countryBytes'] += dict[item]['dipbytes'][i]

	# print countryBytes
	graph = """<!DOCTYPE html>
<meta charset="utf-8">
<head>
	<style>
	table, th, td {
		border: 1px solid black;
		border-collapse: collapse;
	}
	h3 {text-align:center;}
	th, td {
		padding: 5px;
		text-align: left;
	}
	table#t01 tr:nth-child(even) {
    	background-color: #eee;
	}
	table#t01 tr:nth-child(odd) {
	   background-color:#fff;
	}
	table#t01 th	{
	    background-color: black;
	    color: white;
	}
	#nav {
	    width:200px;
	    float:right;	      
	}
	#section {
	    float:left;
	}

	#legendDiv{
	    right: 0%;
    	top: 40%;
    	position: absolute;
    	background-color:rgba(192, 192, 192, 0.72);
	}

	</style>
</head>
<body>
<div id = "vizDiv">
  <link type="text/css" href="Visualizations/GeoIP/colors.css" rel="stylesheet" />
  <script src="http://d3js.org/d3.v3.min.js"></script>
  <script src="http://d3js.org/topojson.v1.min.js"></script>
  <script src = "Visualizations/GeoIP/datamaps.world.min.js"></script>

  <div class="container"> 
  	<div id="container1" style="float: left; width: 100%; max-height:100%;"></div>

  </div>

  	<div id="legendDiv">
		<ul class="legend">
			<li><span class="bg11"></span> >3,000,000 bytes</li>
			<br>
			<li><span class="bg10"></span> >1,000,000 bytes</li>
			<br>
			<li><span class="bg9"></span> >500,000 bytes</li>
			<br>
			<li><span class="bg8"></span> >250,000 bytes</li>
			<br>
			<li><span class="bg7"></span> >100,000 bytes</li>
			<br>
			<li><span class="bg6"></span> >50,000 bytes</li>
			<br>
			<li><span class="bg5"></span> >25,000 bytes</li>
			<br>
			<li><span class="bg4"></span> >10,000 bytes</li>
			<br>
			<li><span class="bg3"></span> >5,000 bytes</li>
			<br>
			<li><span class="bg2"></span> >2,000 bytes</li>
			<br>
			<li><span class="bg1"></span> <2,000 bytes</li>
			<br>
			<li><span class="bg0"></span> No connection</li>
		</ul>
	</div>

	 <script>
	   //basic map config with custom fills, mercator projection
	  var map = new Datamap({
		scope: 'world',
		element: document.getElementById('container1'),
		projection: 'mercator',
		height: 700,
		fills: {
		  defaultFill: '#FFBE12',
		  bg1: '#0CFAEA',
		  bg2: '#0CFA97',
		  bg3: '#44FF03',
		  bg4: '#98FF03',
		  bg5: '#ADF70D', 
		  bg6: '#E9F70D', 
		  bg7: '#F7D00D', 
		  bg8: '#F77E0D', 
		  bg9: '#F74D0D', 
		  bg10: '#E74C12',
		  bg11: 'red'
		},
		data: {"""
	for item in countryBytes:
		graph += "'" + str(countryBytes[item]['countryID']) + "': { fillKey: '"
		if(countryBytes[item]['countryBytes'] > 3000000):
			graph += "bg11', },\n"
		elif(countryBytes[item]['countryBytes'] > 1000000):
			graph += "bg10' },\n"
		elif(countryBytes[item]['countryBytes'] > 500000):
			graph += "bg9' },\n"
		elif(countryBytes[item]['countryBytes'] > 250000):
			graph += "bg8' },\n"
		elif(countryBytes[item]['countryBytes'] > 100000):
			graph += "bg7' },\n"
		elif(countryBytes[item]['countryBytes'] > 50000):
			graph += "bg6' },\n"
		elif(countryBytes[item]['countryBytes'] > 25000):
			graph += "bg5' },\n"
		elif(countryBytes[item]['countryBytes'] > 10000):
			graph += "bg4' },\n"
		elif(countryBytes[item]['countryBytes'] > 5000):
			graph += "bg3' },\n"
		elif(countryBytes[item]['countryBytes'] > 2000):
			graph += "bg2' },\n"
		else:
			graph += "bg1' },\n"		
	graph += """
		}
	  })
	map.arc(["""		
	for item in dict:
		for i in range(0, len(dict[item]['dip']), 1):
			graph += """
	{
		origin:{	
			latitude: """
			graph += str(dict[item]['latSIP']) + ','
			graph += """
			longitude: """
			graph += str(dict[item]['lonSIP'])
			graph += """
		},
		destination:{
			latitude: """
			graph += str(dict[item]['latDIP'][i]) + ','
			graph += """
			longitude: """
			graph += str(dict[item]['lonDIP'][i])
			graph += """
		},
		
	},"""
	graph += """
	], {strokeWidth: 1, arcSharpness: 1.4});

	 </script>
	
	<div id="tableContainer" class="container">

	 """

	if bool(SrcNotInGeoIP):
		graph += """

	<H3> Source IPs not in Map </H3>

	<table style="width:100%;" id = "t01">
  <tr>
	<th>Source IP</th>
	<th>Destination IP</th>		
	<th>Bytes</th>
 </tr>"""
		for item in SrcNotInGeoIP:
			for i in range(0, len(SrcNotInGeoIP[item]['dip']), 1):
				graph += "	<tr>"
				graph += "		<td>" + str(item) + "</td>"
				graph += "		<td>" + str(SrcNotInGeoIP[item]['dip'][i]) + "</td>"	
				graph += "		<td>" + str(SrcNotInGeoIP[item]['dipbytes'][i]) + "</td>"	
				graph += "  </tr>"
		graph += """
</table>"""

	if bool(DstNotInGeoIP):
		graph += """
	<br>
	<br>

	<H3> Destination IPs not in Map </H3>

	<table style="width:100%;" id = "t01">
  <tr>
	<th>Destination IP</th>
	<th>Source IP</th>		
	<th>Bytes</th>
 </tr>"""
		for item in DstNotInGeoIP:
			for i in range(0, len(DstNotInGeoIP[item]['dip']), 1):
				graph += "	<tr>"
				graph += "		<td>" + str(DstNotInGeoIP[item]['dip'][i]) + "</td>"
				graph += "		<td>" + str(item) + "</td>"	
				graph += "		<td>" + str(DstNotInGeoIP[item]['dipbytes'][i]) + "</td>"	
				graph += "  </tr>"
		graph += """
	</table>
	"""
	graph += """
		</div>
		</div>
		</body>
	"""

	return graph