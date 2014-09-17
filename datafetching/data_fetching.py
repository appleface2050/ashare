#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys 
import urllib2
import time
import getopt
import logging
import datetime

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from model.system import ASharesCodeReal
from model.stock_data import StockData
from conf.settings import TIMEOUT_FETCH_DAILY,TIMEOUT_REFETCH_DAILY

class DataFetching(object):
	def generate_g(self, period):
		assert period in ('day','week','month') 	
		if period == 'day':
			g = 'd'
		elif period == 'week':
			g = 'w'
		elif period == 'month':
			g = 'm'
		return g		
	
	def split_code(self, code):
			return str(code['code']),str(code['exchange'])

	def progress_bar(self, code, maxnum, nownum, start_time):
		'''
		print f,"......   ","%0.02f"%(100*float(filenum)/float(all_file_num)),"%","......running time:",datetime.datetime.now()-start
		'''
		cod, exch = self.split_code(code)
		coe = "%0.02f"%(100*float(nownum)/float(maxnum)) + "%"
		rt = datetime.datetime.now()-start_time
		return str(cod)+'.'+str(exch)+'......'+str(coe)+'...running time:'+str(rt)

	def generate_url(self, code, start, end, period):
		'''
		url = 'http://ichart.yahoo.com/table.csv?s=600000.SS&a=08&b=15&c=2014&d=08&e=15&f=2014&g=d'
		'''
		url = ''
		#cn = str(code['code'])
		#exch = str(code['exchange'])
		cn,exch = self.split_code(code)
		a = str(start.month - 1) # yahoo's api , month-1 
		b = str(start.day)
		c = str(start.year)
		d = str(end.month - 1)
		e = str(end.day)
		f = str(end.year)
		g = self.generate_g(period)
		url = "http://ichart.yahoo.com/table.csv?s=%s.%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=%s" % (cn,exch,a,b,c,d,e,f,g)
		return url
		
	def fetch_data(self, url):
		if not url:
			return False
		else:
			f = urllib2.urlopen(url,timeout=TIMEOUT_FETCH_DAILY) 
			data = f.readlines() 
			return data
		
	def save_data(self, code, data):
		import_num = 0
		cod, exch = self.split_code(code)
		for i in data:
			if 'Open' in i:
				continue
			else:
				try:
					da = i.strip().split(',')
					if len(da) != 7:
						print "the number of this line's data is wrong ",da
						continue
					else:
						s = StockData.new()
						s.code,s.exchange = cod, exch
						s.Date = str(da[0])
						s.Open = float(da[1])
						s.High = float(da[2])
						s.Low = float(da[3])
						s.Close = float(da[4])
						s.Volume = float(da[5])
						s.AdjClose = float(da[6])
						#print s
						s.save()
						import_num += 1
				except Exception,e:
					print e,code,data
		return import_num

	def start_fetching(self, start, end, period, pro_start_time):
		code_num = 0
		data = ''
		code_list = ASharesCodeReal.mgr().get_all_codes()
		num_all = len(code_list)
		for code in code_list:
			url = self.generate_url(code,start,end,period)				
			try:
				data = self.fetch_data(url)
			except Exception, e:
				print code,e				
			if data:
				import_num = self.save_data(code,data)
				print self.progress_bar(code,len(code_list),code_num,pro_start_time)
				code_num += 1
		return import_num

	def start_deleting(self, start, end, period):
		print "delete function not ready yet"
		return True

	def start_updating(self, start, end, period):
		print "update function not ready yet"
		return True

	def start_importing(self, mode, start, end, period,pro_start_time):
		import_num = 0
		if mode == 'fetch':	
			import_num = self.start_fetching(start,end,period,pro_start_time)
		elif mode == 'delete':
			import_num = self.start_deleting(start,end,period)
		elif mode == 'update':
			import_num = self.start_updating(start,end,period)
		print "import num: ",import_num
		return True

if __name__ == '__main__':
##	f = urllib2.urlopen(url,timeout=10)
#	data = f.readlines()
#	print data[1].strip()
	s = DataFetching()
	try:
		opts,args = getopt.getopt(sys.argv[1:],'',['mode=','start=','end=','period='])
	except getopt.GetoptError,e:
		logging.error('%s\n',str(e),exc_info=True)
		sys.exit(2)
	mode,start,end,period = 'fetch',None,None,'day'
	for o, a in opts:
		if o == '--mode':
			mode = a 
		if o == '--start':
			start = datetime.datetime.strptime(a,'%Y-%m-%d').date()
		if o == '--end':
			end = datetime.datetime.strptime(a,'%Y-%m-%d').date()
		if o == '--period':
			period = a
	assert mode in ('fetch','update','delete')
	assert period in ('day','week','month')

	now = datetime.datetime.now()
	yest = datetime.date.today() - datetime.timedelta(days=1)
	if not start:
		start = yest
	if not end:
		end = yest	
	if start > end:
		print "start time or end time error"
		sys.exit(2)
 	
	print 'start...',mode,start,'-->',end 
	s.start_importing(mode,start,end,period,now)
	print 'processed...',mode,start,'-->',end
	print 'time used:  ',mode,datetime.datetime.now()-now



