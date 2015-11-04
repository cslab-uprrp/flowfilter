#!/usr/bin/python
import cgi, cgitb
from silk import *
import os


cmd = 'rwfilter --scidr=136.145.231.46 --sensor=S0 --type=all --protocol=1,6,17 --print-volume --threads=4 --pass-destination=stdout --site-config-file=/data/conf-v9/silk.conf | rwcut --fields=1,2,5,3 > test1.out'

flows = []

print 'hola'


for filename in FGlob(classname="all", type="all", start_date="2000/01/01", end_date="2039/01/01", site_config_file="/data/conf-v9/silk.conf", data_rootdir="/scratch/flow/rwflowpack"):
        for rec in silkfile_open(filename, READ): #read the flow file
                sip = rec.sip
                dip = rec.dip
                sport = rec.sport
                dport = rec.dport
                output = rec.output
                _input = rec.input
                
		print sip
#os.system(cmd)
