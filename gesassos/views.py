# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader


def index(request):
    context = {
    	"app_name": "home",
        "location?": "TODO",
    }
    return render(request, 'gesassos/index.html', context)

# def login(request):
# 	# Todo : use return URL in parameter, given by a private page redirecting here
# 	return redirect(settings.CAS_URL + 'login?service=' + request.build_absolute_uri(reverse('view_name', args=(obj.pk, ))))