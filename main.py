#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json,sys,re
from bs4 import BeautifulSoup
import webbrowser
true = True
null = None
false = False
google = 'http://173.194.72.31'

def query(Allkey):
	Allkey = Allkey.encode('utf-8')
	key = ' '.join(Allkey.split(" ")[1:])
	if not key:
		return ""
	results = []
	if not Allkey.endswith(' '):
		preKeyUrl = google+'/complete/search?client=hp&hl=zh-CN&gs_rn=49&gs_ri=hp&cp=3&gs_id=vw&xhr=t&q='+key
		html = requests(preKeyUrl)
		html = json.loads(html)
		for i in html[1]:
			res = {}
			res["Title"] = i[0]
			res["IcoPath"] = "./icon.png"
			results.append(res)
		return json.dumps(results)
	else:
		#url = google+'/#newwindow=1&q='+key
		#url = 'http://173.194.72.31/#q=123'
		#url = 'http://www.google.com/#newwindow=1&q=123'
		#html = requests('http://173.194.72.31/?_escaped_fragment_=q=123')
		url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=8&q='+key
		html = requests2(url)
		html = html.replace('<b>','')
		html = html.replace('</b>','')
		html = json.loads(html)
		for item in html['responseData']['results']:
			res = {}
			res["Title"] = item['titleNoFormatting']
			res["SubTitle"] = item['content'].replace('\n','')
			res["ActionName"] = "openUrl"
			res["IcoPath"] = "./icon.png"
			res["ActionPara"] = item['url']
			results.append(res)
		return json.dumps(results)

def requests(url,timeouts=4):
	header = {
			#'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Referer': 'http://www.google.com/',
			'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
			}	
	request = urllib2.Request(url,headers=header)
	response = urllib2.urlopen(request,timeout=timeouts)
	html = response.read()
	if html:
		return html
	return None

def requests2(url,timeouts=4):
	header = [
			#('DNT','1'),
			('Accept-Language','zh-CN,zh;q=0.8,ja;q=0.6'),
			('Host','ajax.googleapis.com'),
			('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
			#('Referer', 'http://www.google.com/'),
			('User-Agent','User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
			]		
	proxy_handler = urllib2.ProxyHandler({'https':'http://127.0.0.1:8087','http':'http://127.0.0.1:8087'})
	opener = urllib2.build_opener(proxy_handler)
	opener.addheaders = header
	response = opener.open(url)
	html = response.read()
	if html:
		return html
	return None

def openUrl(context,url):
	webbrowser.open(url)

if __name__ == '__main__':
	print query(u"google 123 ")
