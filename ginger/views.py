# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from api import ginger

from .forms import GingerKeyForm

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
    showForm = False

    if request.method == 'POST':
        form = GingerKeyForm(request.POST)

        if form.is_valid():
            response = ginger.addKey(form.cleaned_data)

            # TODO gérer erreurs
            # print(response)
            messages.success(request, 'Clé d\'API correctement créée pour %s: %s'%(request.POST.get("login", ""), response["key"]))

            return HttpResponseRedirect(reverse('ginger:api'))
        else:
            showForm = True

    else:
        form = GingerKeyForm()

    keys = ginger.getKeys()
    keys.sort()

    # TODO: delete ginger_rights
    # TODO: put clean name instead of app_name
    context = {
        'app_name': "ginger",
        'view_name' : "api",
        'keys': keys,
        'form': form,
        'show_form': showForm,
        'assos': [
            {
                'login': "simde",
                'name': "SiMDE"
            },
            {
                'login': "etuville",
                'name': "Étuville"
            },
            {
                'login': "bde",
                'name': "BDE"
            }
        ]
    }

    # If no form is given or their is an error in the form
    return render(request, 'ginger/api.html', context)

@login_required
def delete_key(request, key):
    # TODO: properly check the response
    response = ginger.deleteKey(key)
    if response is True:
        messages.success(request, 'Clé d\'API correctement supprimée')
    else:
        print(response)
        messages.error(request, 'Suppression refusée par Ginger : %s (%s)'%(response["message"], response["name"]))

    return HttpResponseRedirect(reverse('ginger:api'))


# @login_required
# def api_add(request):