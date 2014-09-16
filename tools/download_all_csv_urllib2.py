#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys 
import urllib2

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from model.system import ASharesCode

res = ASharesCode.mgr().get_all_codes()

#http://table.finance.yahoo.com/table.csv?s=000001.sz

for i in res:
	if int(i.code) <= 512120:
		continue
	if i.exchange != 'sh':
		continue
	else:
		i.exchange = 'ss'
	url = "http://table.finance.yahoo.com/table.csv?s=%s.%s" % (str(i.code),str(i.exchange))
	try:	
		print "downloading... %s" % url
		f = urllib2.urlopen(url,timeout=5) 
		data = f.read()
		filename = "/home/appleface/ashare/tools/data/table%s.%s" % (str(i.code),str(i.exchange))
		with open(filename,'wb') as res:
			res.write(data)

	except Exception, e:
		print "error",url
		print e



