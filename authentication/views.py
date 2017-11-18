# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import loader
from django.http import HttpResponse

def info(request):
	template = loader.get_template('authentication/info.html')
	context = {
		'app_name': "authentication",
		'view_name' : "infos",
	}
	return HttpResponse(template.render(context, request))