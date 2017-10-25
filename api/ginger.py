# -*- coding: utf-8 -*-

from django.conf import settings
import requests

def _urlJoin(*argv):
	strArgv = []
	for arg in argv:
		strArgv.append(str(arg))
	return settings.GINGER_SERVER_URL_V2 + "/".join(strArgv)

def _makeHeaders():
	return {
		'Authorization': 'Bearer ' + settings.GINGER_KEY_V2,
		'Content-type': "application/json"
	}

def getKeys():
	# p = {}
	h = _makeHeaders()
	# r = requests.get(_urlJoin("keys"), params = p, headers = h)
	r = requests.get(_urlJoin("keys"), headers = h)
	# r.status_code
	# TODO: handle errors !
	return r.json()

def addKey(d):
	# print(d)
	h = _makeHeaders()
	r = requests.post(_urlJoin("keys"), json = d, headers = h)
	# TODO: handle errors !
	return r.json()

def editKey(key, d):
	h = _makeHeaders()
	r = requests.patch(_urlJoin("keys", key), json = d, headers = h)
	print(r)
	return True if r.status_code == 204 else r.json()

def deleteKey(key):
	h = _makeHeaders()
	r = requests.delete(_urlJoin("keys", key), headers = h)
	return True if r.status_code == 200 else r.json()

def renewKey(key):
	h = _makeHeaders()
	r = requests.post(_urlJoin("keys", key), headers = h)
	return True if r.status_code == 200 else r.json()