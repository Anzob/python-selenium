#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, locale, _thread, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

	def GetIPFromPageContent(self, href_data):
		pagecontent = self.GetPageContent(href_data)
		ippattern = re.findall(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', pagecontent)
		print(len(ippattern), type(ippattern))
		if(len(ippattern) > 0):
			for ip in ippattern:
				print(ip)
		#print(pagecontent)
		
	def GetPageContent(self, pageurl):
		driver = webdriver.Firefox()
		driver.implicitly_wait(30)
		driver.get(pageurl)
		content = driver.page_source
		#print(driver.title)
		driver.close()
		return content
		
	def GetProxyList(self):
		self.xvfb = Xvfb(width=1280, height=780, colordepth=16)
		self.xvfb.start()

		print("start parse body")
		
		driver = webdriver.Firefox()
		driver.get('https://www.google.com/?gfe_rd=cr&gws_rd=ssl,cr&fg=1#safe=off&q=proxy+list')
		print(driver.title)
		
		try:
			element = WebDriverWait(driver, 20).until(
				EC.presence_of_element_located((By.ID, "lfootercc"))
			)
			print("Wait success")
		except:
			print("Unexpected error:", sys.exc_info()[0])
			raise

		#print(element)
		print("start parsing")
		'''fh = open('/home/alex/py/google.txt', "wb+")
		fh.write((driver.page_source).encode())
		fh.close()'''
		
		fh = open('/home/alex/py/proxy_list.txt', "wb+")
		##sbody = driver.find_element_by_xpath("/*")
		
		#lst = list(driver.find_elements_by_xpath('/h3[@class="r"]'))
		#lst = driver.find_elements_by_css_selector('h3.r')
		lst = list(driver.find_elements_by_xpath("//h3[@class='r']/a"))
		#print('len ', len(lst), type(lst))
		print('len ', len(lst))
		for li in lst:
			fh.write((li.get_attribute('href') + "\n").encode())
			href_data = li.get_attribute('href')
			print(href_data)
			#print(self.page_content)
			self.GetIPFromPageContent(href_data)
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
