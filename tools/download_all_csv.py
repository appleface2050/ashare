#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys 

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from model.system import ASharesCode

res = ASharesCode.mgr().get_all_codes()

#http://table.finance.yahoo.com/table.csv?s=000001.sz

for i in res:
	if i.exchange != 'sh':
		continue
	else:
		i.exchange = 'ss'
	url = "http://table.finance.yahoo.com/table.csv?s=%s.%s" % (str(i.code),str(i.exchange))
	os.system("wget %s"%url)



