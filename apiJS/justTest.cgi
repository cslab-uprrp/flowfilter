#!/usr/bin/python
import cgi, cgitb
from silk import *
import json
import os
from engine import *
from ian import *

print """Content-Type: text/html"""
print

# print 'HElloo WOrld' * 5
# print 

form = cgi.FieldStorage()
dta = form.getvalue("dta")
# dta = json.loads(dta)
# dta = data['data']

print dta