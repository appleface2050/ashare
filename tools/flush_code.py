#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys 
import urllib2

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from model.system import ASharesCodeReal,ASharesCode

def download_data(code,exchange):
	url = "http://table.finance.yahoo.com/table.csv?s=%s.%s" % (code,exchange)
	try:
		print "downloading... %s" % url
		f = urllib2.urlopen(url,timeout=15)
		data = f.read()
		filename = "/home/appleface/ashare/tools/otherdata/table%s.%s" % (code,exchange)
		with open(filename,'wb') as res:
			res.write(data)
	except Exception, e:
		print "error",url
		print e

if __name__ == '__main__':
	q = ASharesCode.mgr().get_all_unreal_code()
	for i in q:
		if str(i['exchange']) == 'sh':
			i['exchange'] = 'ss'
		download_data(str(i['code']),str(i['exchange']))


