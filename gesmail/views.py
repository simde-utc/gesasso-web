# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

def index(request):
    template = loader.get_template('gesmail/index.html')
    context = {
        'all': "all",
    }
    return HttpResponse(template.render(context, request))

def detail(request, all):
    context = {
        'all': all == "all",
    }
    if all == "prout":
    	raise Http404("Mauvaise réponse !")
    return render(request, 'gesmail/index.html', context)