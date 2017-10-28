# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader


def index(request):
    context = {
    	"app_name": "home",
        # "groups": [ g.name for g in request.user.groups.all()]
    }
    return render(request, 'gesassos/index.html', context)

def denied(request):
    context = {
    	"app_name": "denied",
    	"denied_page": request.GET.get('next',''),
    }
    return render(request, 'gesassos/denied.html', context)

# def error404(request):
# 	return render(request, 'gesassos/404.html', context, status=404)