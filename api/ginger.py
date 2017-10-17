# -*- coding: utf-8 -*-

from django.conf import settings
import requests

def _urlJoin(*argv):
	return settings.GINGER_SERVER_URL_V2 + "/".join(argv)

def _makeHeaders():
	return {
		'Authorization': 'Bearer ' + settings.GINGER_KEY_V2,
		'Content-type': "application/json"
	}

def getKeys():
	p = {}
	h = _makeHeaders()
	r = requests.get(_urlJoin("keys"), params = p, headers = h)
	# r.status_code
	# TODO: handle errors !
	return r.json()

def addKey(login,
	description,
	users_add,
	users_delete,
	users_edit,
	users_badge,
	contributions_add,
	contributions_delete,
	contributions_read,
	stats,
	settings_read,
	keys_all):
	d = {
		"login": login,
		"description": description,
		"users_add": users_add,
		"users_delete": users_delete,
		"users_edit": users_edit,
		"users_badge": users_badge,
		"contributions_add": contributions_add,
		"contributions_delete": contributions_delete,
		"contributions_read": contributions_read,
		"stats": stats,
		"settings_read": settings_read,
		"keys_all": keys_all,
	}
	print(d)
	p = {}
	h = _makeHeaders()
	r = requests.post(_urlJoin("keys"), params = p, json = d, headers = h)
	# TODO: handle errors !
	return r.json()

def deleteKey(key):
	h = _makeHeaders()
	r = requests.delete(_urlJoin("keys", key), headers = h)
	return True if r.status_code == 200 else r.json()