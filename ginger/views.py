# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from api import ginger
from authentication import userUtils, models

from .forms import GingerKeyForm

@login_required
def contributors(request):
    contributors = []
    search = ""
    
    # If a search has been made
    if request.method == "GET" and "s" in request.GET and len(request.GET["s"]) > 0:
        getSearch = request.GET["s"]

        response = ginger.searchUsers(getSearch)
        if response.success:
            contributors = response.content
        else:
            messages.error(request, 'Erreur lors de la recherche: %s (%s)'%(response.errorMessage, response.errorName))

        search = getSearch

    context = {
        'app_name': "ginger",
        'view_name' : "contributors",
        'contributors' : contributors,
        'search': search,
        'all': "all",
    }

    return render(request, 'ginger/contributors.html', context)

@login_required
def api(request):
    showForm = False
    search = False

    # TODO: get real asso names
    assos = list(set([(role.asso, role.asso) for role in models.UserRole.objects.all()]))
    assos.append(('bde', 'bde'))
    if not userUtils.has_group(request.user, "simde"):
        userAssos = list(set([role.asso for role in request.user.roles.all()]))
    else:
        userAssos = [] #nofilter
    # assos = [("etuville", "Étuville"), ("simde", "SiMDE"), ("bde", "BDE")]

    # Test if user has right to add a key
    if userUtils.has_group(request.user, "simde") and request.method == 'POST':
        form = GingerKeyForm(tuple(assos), request.POST)

        if form.is_valid():
            if request.POST.get("edit-id", "").isdigit():
                # Actually editing an item
                keyId = int(request.POST.get("edit-id", ""))

                # Update key values
                form.cleaned_data.pop("login", None)
                print form.cleaned_data
                response = ginger.editKey(keyId, form.cleaned_data)

                if response.success:
                    messages.success(request, 'Clé d\'API correctement mise à jour pour %s'%(request.POST.get("login", "")))
                else:
                    messages.error(request, 'Édition impossible : %s (%s)'%(response.errorMessage, response.errorName))
            else:
                # Creating a new key
                print form.cleaned_data
                response = ginger.addKey(form.cleaned_data)

                if response.success:
                    messages.success(request, 'Clé d\'API correctement créée pour %s: %s'%(request.POST.get("login", ""), response.content["key"]))
                else:
                    messages.error(request, 'Ajout impossible : %s (%s)'%(response.errorMessage, response.errorName))

            return HttpResponseRedirect(reverse('ginger:api'))
        else:
            showForm = True

    else:
        form = GingerKeyForm(tuple(assos))

    keysResponse = ginger.getKeys(userAssos)
    keys = []
    if keysResponse.success:
        keys = keysResponse.content

        # If a search has been made
        if request.method == "GET" and "s" in request.GET:
            getSearch = request.GET["s"]
            keys = [key for key in keys if getSearch in key["login"]+key["key"]+key["description"]]
            search = getSearch

        # Generate key edit form
        for i in range(0, len(keys)):
            keys[i]["form"] = GingerKeyForm(tuple(assos), keys[i]).as_materialize
    else:
        messages.error(request, 'Lecture des clés impossible : %s (%s)'%(keysResponse.errorMessage, keysResponse.errorName))

    assosAutocomplete = {}
    for assoLogin, assoName in assos:
        assosAutocomplete[assoLogin] = None
    assosAutocomplete = json.dumps(assosAutocomplete)

    # TODO: put clean name instead of app_name
    context = {
        'app_name': "ginger",
        'view_name' : "api",
        'autocomplete': assosAutocomplete,
        'search': search,
        'keys': keys,
        'form': form,
        'show_form': showForm
    }

    # If no form is given or their is an error in the form
    return render(request, 'ginger/api.html', context)

@login_required
def delete_key(request, key):
    response = ginger.deleteKey(key)
    if response.success:
        messages.success(request, 'Clé d\'API correctement supprimée')
    else:
        messages.error(request, 'Suppression refusée par Ginger : %s (%s)'%(response.errorMessage, response.errorName))

    return HttpResponseRedirect(reverse('ginger:api'))

@login_required
def renew_key(request, key):
    response = ginger.renewKey(key)
    if response.success:
        messages.success(request, 'Clé d\'API correctement regénérée')
    else:
        messages.error(request, 'Regénération refusée par Ginger : %s (%s)'%(response.errorMessage, response.errorName))

    return HttpResponseRedirect(reverse('ginger:api'))

@login_required
def info(request):
    context = {
        'app_name': "ginger",
        'view_name' : "infos",
        'user_info': request.user,
    }
    return render(request, 'ginger/info.html', context)

@login_required
def info(request, login = None):
    if not login:
        login = request.user.login

    response = ginger.getUser(login)
    user_info = None
    if response.success:
        user_info = response.content

        # Rename inconsistant keys
        user_info["is_contributor"] = user_info["isContributor"]
        user_info["first_name"] = user_info["firstname"]
        user_info["last_name"] = user_info["lastname"]
        user_info["user_infotype"] = {
            "name": user_info["type"]
        }
        user_info["is_active"] = request.user.is_active if login == request.user.login else None
        user_info["is_admin"] = request.user.is_admin if login == request.user.login else None
        user_info["is_adult"] = user_info["isAdult"]
        user_info["badge"] = user_info["badge"]
        user_info["updated_at"] = user_info["updatedAt"]
        user_info["groups"] = request.user.groups if login == request.user.login else None
        user_info["roles"] = request.user.roles if login == request.user.login else None

        # Get contributions
        response = ginger.getUserContributions(login)
        if response.success:
            user_info["contributions"] = response.content
            currentDate = datetime.today().date()
            user_info["contributions"][0]["begin"] = contributionBegin = datetime.strptime(user_info["contributions"][0]["begin"],"%Y-%m-%d").date()
            user_info["contributions"][0]["end"] = contributionEnd = datetime.strptime(user_info["contributions"][0]["end"],"%Y-%m-%d").date()
            if contributionBegin < currentDate and currentDate < contributionEnd:
                user_info["contributions"][0]["current"] = True
        else:
            if not response.errorName == "ContributionNotFoundError":
                messages.error(request, 'La recherche de contribution sur Ginger a échoué : %s (%s)'%(response.errorMessage, response.errorName))
            user_info["contributions"] = None
    else:
        messages.error(request, 'La recherche sur Ginger a échoué : %s (%s)'%(response.errorMessage, response.errorName))

    context = {
        'app_name': "ginger",
        'view_name' : "infos",
        'user_info': user_info,
    }
    return render(request, 'ginger/info.html', context)