#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, locale, _thread, re
from selenium import webdriver
from xvfbwrapper import Xvfb

class SetProxy():
	def SetProxyFunc(self):
		self.xvfb = Xvfb(width=1280, height=780, colordepth=16)
		self.xvfb.start()

		driver = webdriver.Firefox()
		driver.get('http://myip.ru/')
		#print(driver.title)
		#element = driver.find_element_by_id('hostname')
		element = driver.find_element_by_xpath('//table[@class="network-info"]')
		print("old ip " + element.text)
		driver.close()
        #PROXY = "178.62.118.19:8118"
		PROXY = "111.1.23.180:80"

		webdriver.DesiredCapabilities.CHROME['proxy']={
		    "httpProxy":PROXY,
		    "ftpProxy":PROXY,
		    "sslProxy":PROXY,
		    "noProxy":None,
		    "proxyType":"MANUAL",
		    "autodetect":False
		}
		driver = webdriver.Chrome()
		driver.get('http://myip.ru/')
		#print(driver.title)
		element = driver.find_element_by_xpath('//table[@class="network-info"]')
		print("new ip " + element.text)
		driver.close()
		self.xvfb.stop()

	def GetIPFromPageContent(self, pagecontent):
		ippattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', re.IGNORECASE)
		print(ippattern.match(pagecontent))
		
	def GetPageContent(self, driver, pageurl):
		driver.get(pageurl)		
		page_source = driver.page_source
		return page_source
		
	def GetProxyList(self):
		self.xvfb = Xvfb(width=1280, height=780, colordepth=16)
		self.xvfb.start()

		print("start parse body")
		"""
		PROXY = "178.62.118.19:8118"

		webdriver.DesiredCapabilities.CHROME['proxy']={
		    "httpProxy":PROXY,
		    "ftpProxy":PROXY,
		    "sslProxy":PROXY,
		    "noProxy":None,
		    "proxyType":"MANUAL",
		    "autodetect":False
		}
		"""
		driver = webdriver.Chrome()
		driver.implicitly_wait(20)
		driver.get('https://www.google.com/?gfe_rd=cr&gws_rd=ssl,cr&fg=1#safe=off&q=proxy+list')

		fh = open('/home/alex/py/proxy_list.txt', "wb+")
		##sbody = driver.find_element_by_xpath("/*")
		#print(driver.page_source)
		"""lst = list(driver.find_elements_by_xpath('/h3[@class="r"]'))"""
		#lst = driver.find_elements_by_css_selector('h3.r')
		lst = driver.find_elements_by_xpath("//h3[@class='r']/a")
		print('len {0}', len(lst), type(lst))
		for li in lst:
			fh.write((li.get_attribute('href') + "\n").encode())
			href_data = li.get_attribute('href')
			print(href_data)
			page_content = self.GetPageContent(driver, href_data)
			#self.GetIPFromPageContent(page_content.string)
			##attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', li)
			##print(attrs)
		fh.close()

		driver.close()
		self.xvfb.stop()
		print("stop parse body")

class PageWrapper():
	def get_pageContentFunc(self, th_name, url, filename, filename2, useproxy):
		print("Thread %s start" % th_name)

		#self.xvfb = Xvfb(width=1280, height=780, colordepth=16)
		#self.xvfb.start()
		#print("xvfb_cmd %s" % self.xvfb.xvfb_cmd)

		if useproxy:
			#PROXY = "210.211.18.140:808"
			PROXY = "122.96.59.106:83"
			webdriver.DesiredCapabilities.CHROME['proxy']={
				"httpProxy":PROXY,
				"ftpProxy":PROXY,
				"sslProxy":PROXY,
				"noProxy":None,
				"proxyType":"MANUAL",
				"autodetect":False
			}

		driver = webdriver.Chrome()
		driver.get(url)

		fh = open(filename2, "wb+")
		sbody = driver.find_element_by_xpath("//body")
		fh.write((sbody.text).encode())
		fh.close()

		fh = open(filename, "wb+")
		lst = list(driver.find_elements_by_xpath("//a[@class='link link_outer_yes path__item']"))
		for ii in lst:
			fh.write((ii.get_attribute('innerHTML') + "\n\n").encode())
		fh.close()

		driver.close()

		#self.xvfb.stop()

		print("Thread %s end" % th_name)

#obj1 = PageWrapper()
#obj2 = PageWrapper()
obj3 = SetProxy()

obj3.GetProxyList()

#func1 = obj1.get_pageContentFunc
#func2 = obj2.get_pageContentFunc
"""
xvfb = Xvfb(width=1280, height=780, colordepth=16)
xvfb.start()

func1(th_name='r1', url='https://yandex.ru/search/?text=грпш%20москва', filename='/home/alex/py/result.txt', filename2='/home/alex/py/result_tech.txt', useproxy=False)
func1(th_name='r1', url='https://yandex.ru/search/?text=грпш%20москва', filename='/home/alex/py/result2.txt', filename2='/home/alex/py/result2_tech.txt', useproxy=True)

xvfb.stop()"""
"""
try:
   _thread.start_new_thread( func1, ("r1", "https://yandex.ru/search/?text=грпш", "/home/alex/py/result.txt") )
   _thread.start_new_thread( func2, ('r2', 'https://yandex.ru/search/?text=рвс', '/home/alex/py/result2.txt') )
except:
   print ("Error: unable to start thread")

while 1:
   pass"""
#get_pageContentFunc('r1', 'https://yandex.ru/search/?text=грпш', '/home/alex/py/result.txt')
