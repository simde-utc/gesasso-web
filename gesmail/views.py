# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

# @login_required
def index(request):
    template = loader.get_template('gesmail/index.html')
    
    context = {
        'app_name': "gesmail",
        'all': "all",
    }
    return HttpResponse(template.render(context, request))

def detail(request, all):
    context = {
        'app_name': "gesmail",
        'all': all == "all",
    }
    if all == "prout":
    	raise Http404("Mauvaise réponse !")
    return render(request, 'gesmail/index.html', context)