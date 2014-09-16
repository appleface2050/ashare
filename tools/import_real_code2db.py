#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from model.system import ASharesCodeReal

def get_all_files_name(dir):
	res = []
	fs = os.listdir(dir)
	for f in fs:
		if 'table' not in f:
			continue
		else:
			res.append(f)
	return res

def data2db(fns):
	for f in fns:
		if len(f) == 21: #wget下载的文件 (table.csv?s=000002.sz)
	 		code = f.strip()[12:18]
			exch = f.strip()[19:]		
		elif len(f) == 14: #urllib2下载的文件 (table600602.ss)
			code = f.strip()[5:11]
			exch = f.strip()[12:]
		else:
			print "ERROR filename doesn't match!"
			continue			

		s = ASharesCodeReal.new()
		try:
			s.code = str(code)
			s.exchange = str(exch)
			s.status = 'valid'
			#print s
			s.save()
		except Exception,e:
			print f
			print e
	return True

if __name__ == '__main__':
	fns = get_all_files_name('/home/appleface/ashare/tools/otherdata')
	data2db(fns)
	


