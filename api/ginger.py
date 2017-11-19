# -*- coding: utf-8 -*-

from django.conf import settings
import requests
from requestCommons import RequestResult

def _urlJoin(*argv):
	strArgv = []
	for arg in argv:
		strArgv.append(str(arg))
	fullUrl = settings.GINGER_SERVER_URL_V2 + "/".join(strArgv)
	print(fullUrl)
	return fullUrl

def _makeHeaders():
	return {
		'Authorization': 'Bearer ' + settings.GINGER_KEY_V2,
		'Content-type': "application/json"
	}

def _makeRequest(method, url, httpSuccessCode, jsonData = {}):
	h = _makeHeaders()
	result = RequestResult(False)
	try:
		r = method(url, headers = h, json = jsonData)
		if r.status_code == httpSuccessCode:
			content = None
			try:
				content = r.json()
			except ValueError as e:
				pass
			result = RequestResult(True, content=content, raw = r)
		else:
			try:
				error = r.json()
			except ValueError as e:
				error = {
					"name": "Erreur lors de la lecture de l'erreur",
					"message": unicode(r)
				}
			
			if "message" in error:
				errorMessage = error["message"]
			elif "errors" in error and len(error)>0:
				errorMessage = error["errors"][0]["message"] + "(%d erreurs en tout)"%len(error)
			else:
				errorMessage = "Pas de description à afficher..."
			result = RequestResult(False, raw = r, errorName = error["name"], errorMessage = errorMessage + " (erreur Ginger)")
	except requests.ConnectionError as e:
		result = RequestResult(False, errorName="ConnectionError", errorMessage="Impossible de se connecter à Ginger.")
	return result

def getKeys(assosLogin = []):
	result = _makeRequest(requests.get, _urlJoin("keys"), 200)
	if result.success:
		if assosLogin:
			result.content = [key for key in result.content if key["login"] in assosLogin]
		result.content.sort()
	return result

def addKey(d):
	return _makeRequest(requests.post, _urlJoin("keys"), 201, jsonData=d)

def editKey(key, d):
	return _makeRequest(requests.patch, _urlJoin("keys", key), 204, jsonData=d)

def deleteKey(key):
	return _makeRequest(requests.delete, _urlJoin("keys", key), 200)

def renewKey(key):
	return _makeRequest(requests.post, _urlJoin("keys", key), 200)

def searchUsers(search):
	return _makeRequest(requests.get, _urlJoin("users", "search", "?q="+search), requests.codes.ok) # TODO: make requests.codes.ok for all