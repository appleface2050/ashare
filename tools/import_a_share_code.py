#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from model.system import ASharesCode

def importing():
	exchange = 'sz'
	f = open('/home/appleface/ashare/%s.txt'%exchange,'r')
	for i in f.readlines():
		print str(i.strip())
		s = ASharesCode.new()
		try:
			s.code = str(i.strip())
			s.exchange = exchange
			s.save()
		except Exception,e: 
			print i
			logging.error('%s\n',str(e),exc_info=True)

if __name__ == '__main__':
	importing()


