# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

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
    showUnfilter = False

    # TODO
    # assos = getUserAssos()
    assos = [("etuville", "Étuville"), ("simde", "SiMDE"), ("bde", "BDE")]

    # TODO: test if user has right to add a key
    if request.method == 'POST':
        form = GingerKeyForm(tuple(assos), request.POST)

        if form.is_valid():
            if request.POST.get("edit-id", "").isdigit():
                # Actually editing an item
                keyId = int(request.POST.get("edit-id", ""))

                # TODO tester que la clé existe et que l'utilisateur a les droits

                # Update key values
                response = ginger.editKey(keyId, form.cleaned_data)

                # TODO gérer erreurs
                # print(response)
                messages.success(request, 'Clé d\'API correctement mise à jour pour %s'%(request.POST.get("login", "")))
            else:
                # Creating a new key
                response = ginger.addKey(form.cleaned_data)

                if response is True:
                    messages.success(request, 'Clé d\'API correctement créée pour %s: %s'%(request.POST.get("login", ""), response["key"]))
                else:
                    messages.error(request, 'Édition refusée par Ginger : %s (%s)'%(response["message"], response["name"]))

            return HttpResponseRedirect(reverse('ginger:api'))
        else:
            showForm = True

    else:
        form = GingerKeyForm(tuple(assos))

    keys = ginger.getKeys()
    keys.sort()

    # If a search has been made
    if request.method == "GET" and "s" in request.GET:
        search = request.GET["s"]
        keys = [key for key in keys if search in key["login"]+key["key"]+key["description"]]
        showUnfilter = search

    # Generate key edit form
    for i in range(0, len(keys)):
        keys[i]["form"] = GingerKeyForm(tuple(assos), keys[i]).as_materialize

    assosAutocomplete = {}
    for assoLogin, assoName in assos:
        assosAutocomplete[assoLogin] = None
    assosAutocomplete = json.dumps(assosAutocomplete)

    # TODO: put clean name instead of app_name
    context = {
        'app_name': "ginger",
        'view_name' : "api",
        'autocomplete': assosAutocomplete,
        'show_unfilter': showUnfilter,
        'keys': keys,
        'form': form,
        'show_form': showForm
    }

    # If no form is given or their is an error in the form
    return render(request, 'ginger/api.html', context)

@login_required
def delete_key(request, key):
    response = ginger.deleteKey(key)
    if response is True:
        messages.success(request, 'Clé d\'API correctement supprimée')
    else:
        messages.error(request, 'Suppression refusée par Ginger : %s (%s)'%(response["message"], response["name"]))

    return HttpResponseRedirect(reverse('ginger:api'))

@login_required
def renew_key(request, key):
    response = ginger.renewKey(key)
    if response is True:
        messages.success(request, 'Clé d\'API correctement regénérée')
    else:
        messages.error(request, 'Regénération refusée par Ginger : %s (%s)'%(response["message"], response["name"]))

    return HttpResponseRedirect(reverse('ginger:api'))


# @login_required
# def api_add(request):