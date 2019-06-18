import re
import requests
from bs4 import BeautifulSoup
import json
import msgpack
import sys
import os
from urllib import request

## Download a HTML page file
def getURLText(_url, decode='utf-8'):

	dataFromWeb = request.urlopen(_url)

	strData = dataFromWeb.read()
	strData = strData.decode(decode)
	
	return strData

## Require a HTML page by method 'GET'
def getHTMLText(_addr, _headers="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36", params=None):
	# print(_headers)
	html = requests.get(_addr, headers={'user-agent' : _headers}, params=params)
	return html

## Translate pics to numbers via a static map
def textNumberTrans(_text, _number_map):
	for w in _number_map.keys():
		_text = _text.replace(w, _number_map[w])

	return _text