# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, Http404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from api import ginger

@login_required
def contributors(request):
    template = loader.get_template('ginger/index.html')
    
    context = {
        'app_name': "ginger",
        'view_name' : "contributors",
        'all': "all",
    }
    return HttpResponse(template.render(context, request))

@login_required
def api(request):
    context = {
        'app_name': "ginger",
        'view_name' : "api_keys",
        'keys': ginger.getKeys()
    }
    return render(request, 'ginger/api.html', context)