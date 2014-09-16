#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os  
import sys 
import datetime

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0])) 

from model.stock_data import StockData
from model.system import ASharesCodeReal

def get_all_files_name(f_dir):
    res = []
    fs = os.listdir(f_dir)
    for f in fs: 
        if 'table' not in f:
            continue
        else:
            res.append(f)
    return res 

def init_data2db(fns, f_dir, start):
	#fns = ['table002367.sz','table200016.sz']
	filenum = 0
	num = 0
	all_file_num = ASharesCodeReal.mgr().get_len_codes()
	for f in fns:
		filenum += 1
		print f,"......   ","%0.02f"%(100*float(filenum)/float(all_file_num)),"%","......running time:",datetime.datetime.now()-start
		if len(f) == 21: #wget下载的文件 (table.csv?s=000002.sz)
			code = f.strip()[12:18]
			exch = f.strip()[19:]    
		elif len(f) == 14: #urllib2下载的文件 (table600602.ss)
			code = f.strip()[5:11]
			exch = f.strip()[12:]
		else:
			print "ERROR filename doesn't match!"
			continue    
		
		of = open('%s%s'%(f_dir,f),'r')
		for i in of.readlines():				#文件行循环
			#if 'Open' not in i:				#去掉文件内容第一行
			if 'Open' in i:
				continue
			else:
				try:
					data = i.strip().split(',')
					s = StockData.new()
					s.code = str(code)
					s.exchange = str(exch)
					s.Date = data[0]
					s.Open = float(data[1])
					s.High = float(data[2])
					s.Low = float(data[3])
					s.Close = float(data[4])
					s.Volume = long(data[5])
					s.AdjClose = float(data[6])
					#print s
					s.save()
					num += 1
				except Exception,e:
					print f
					print s
					print e
	return num

if __name__ == '__main__':
	print "start importing..."
	f_dir = '/home/appleface/ashare/tools/alldata/'
	fns = get_all_files_name(f_dir)
	start = datetime.datetime.now()
	num = init_data2db(fns, f_dir, start)
	print "imported %s data"%num
	print "used time:",datetime.datetime.now()-start








