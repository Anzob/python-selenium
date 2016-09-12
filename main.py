#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, locale, _thread
from selenium import webdriver
from xvfbwrapper import Xvfb

class PageWrapper():

	def get_pageContentFunc(self, th_name, url, filename):
		print("Thread %s start" % th_name)
		
		self.xvfb = Xvfb(width=1280, height=780, colordepth=16)
		self.xvfb.start()
		
		print("xvfb_cmd %s" % self.xvfb.xvfb_cmd)
		driver = webdriver.Chrome()
		driver.get(url)

		fh = open(filename, "wb+")
		lst = list(driver.find_elements_by_xpath("//a[@class='link link_outer_yes path__item']"))
		for ii in lst:
			fh.write((ii.get_attribute('innerHTML') + "\n\n").encode())
		fh.close()
		driver.close()
		
		self.xvfb.stop()
		#print("Xvfb end")
		#pass
		print("Thread %s end" % th_name)

obj1 = PageWrapper()
obj2 = PageWrapper()

#func1 = obj1.get_pageContentFunc(th_name = 'r1', url = 'https://yandex.ru/search/?text=грпш', filename = '/home/alex/py/result.txt')
func1 = obj1.get_pageContentFunc
func2 = obj2.get_pageContentFunc
#func1(th_name = 'r1', url = 'https://yandex.ru/search/?text=грпш', filename = '/home/alex/py/result.txt')

#func2 = obj2.get_pageContentFunc('r1', 'https://yandex.ru/search/?text=грпш', '/home/alex/py/result.txt')

"""
try:
   _thread.start_new_thread( func1, ("r1", "https://yandex.ru/search/?text=грпш", "/home/alex/py/result.txt") )
   _thread.start_new_thread( func2, ('r2', 'https://yandex.ru/search/?text=рвс', '/home/alex/py/result2.txt') )
except:
   print ("Error: unable to start thread")

while 1:
   pass"""
#get_pageContentFunc('r1', 'https://yandex.ru/search/?text=грпш', '/home/alex/py/result.txt')

