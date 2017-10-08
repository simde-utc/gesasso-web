#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from cas.backends import CASBackend
from cas.backends import _verify
from django.contrib.auth import get_user_model
from django.conf import settings
# from urllib.parse import urlencode, urljoin
# from urllib.request import urlopen
from urllib import urlopen, urlencode
from urlparse import urljoin
import json
import datetime
from authentication.models import UserType
from django.contrib.auth.models import Group


class UpdatedCASBackend(CASBackend):
    """
    An extension of the CASBackend to make it functionnable 
    with custom user models on user creation and selection
    """

    def authenticate(self, ticket, service):
        """
        Verifies CAS ticket and gets or creates User object
        NB: Use of PT to identify proxy
        """

        UserModel = get_user_model()
        username = _verify(ticket, service)
        if not username:
            return None

        try:
            user = UserModel._default_manager.get(**{
                UserModel.USERNAME_FIELD: username
            })
            user = self.configure_user(user)
            user.save()
        except UserModel.DoesNotExist:
            # user will have an "unusable" password
            if settings.CAS_AUTO_CREATE_USER:
                user = UserModel.objects.create_user(username, '')
                user = self.configure_user(user)
                user.save()
            else:
                user = None
        return user

    def configure_user(self, user):
        """
        Configures a user in a custom manner
        :param user: the user to retrieve informations on
        :return: a configured user
        """
        return user


class GingerCASBackend(UpdatedCASBackend):
    """
    A CAS Backend implementing Ginger for User configuration
    """

    def configure_user(self, user):
        """
        Configures a user using Ginger and the student organization portal
        :param user: The User to configure
        :return: The configurated user
        """

        # GINGER
        params = {'key': settings.GINGER_KEY, }
        # url = urljoin(settings.GINGER_SERVER_URL, user.login) + \
        url = urljoin(settings.GINGER_SERVER_URL, str(user)) + \
            '?' + urlencode(params)
        page = urlopen(url)
        response = page.read()
        json_data = json.loads(response.decode())

        user.first_name = json_data.get('prenom').capitalize()
        user.last_name = json_data.get('nom').capitalize()
        user.email = json_data.get('mail')
        if json_data.get('is_adulte'):
            user.birthdate = datetime.date.min
        else:
            user.birthdate = datetime.date.today
        # print(json_data)

        try:
            UserType.objects.get(
                name=UserType.NON_COTISANT)
        except Exception as e:
            UserType.init_values()
            raise e

        if json_data.get('is_cotisant'):
            user.usertype = UserType.objects.get(
                name=UserType.COTISANT)
        else:
            user.usertype = UserType.objects.get(
                name=UserType.NON_COTISANT)

        # PORTAL RIGHTS
        url = urljoin(settings.PORTAL_SERVER_URL, "profile/" + str(user) + "/json")
        response = urlopen(url).read()
        json_data = json.loads(response.decode())

        semester_ids = json_data['semestres'].keys()
        semester_ids.sort(key=int)
        last_semester_id = semester_ids[-1]

        # print(json_data['semestres'][last_semester_id])

        # Check it is current semester # TODO: make the portal API do this check on its own
        current_semester = "A17"

        self._test_groups()
        self._reset_user_rights(user)

        # Check and save SiMDE and BDE rights (portal groups and super admin)
        if "groups" in json_data:
            for group in json_data["groups"]:
                if group == "simde":
                    self._set_user_simde(user)
                if group == "bde":
                    self._set_user_bde(user)
        if "superadmin" in json_data and json_data["superadmin"]:
            self._set_user_superadmin(user)

        # TODO remove, test only
        if user.get_username() in ["michelme", "jennypau", "snastuzz", "crichard"]:
            # self._set_user_superadmin(user)
            # self._set_user_simde(user)
            # self._set_user_bde(user)
            self._set_user_geek(user, "festupic")

        # Check and save asso rights
        if current_semester == json_data['semestres'][last_semester_id]["semestre"]:
            current_semester_id = last_semester_id
            for role in json_data['semestres'][current_semester_id]["roles"]:
                # For all role that is president, "bureau", "resp info", save them
                if role["role"]["name"] == u"Président":
                    self._set_user_president(user, role["asso"]["login"])
                if role["role"]["bureau"]:
                    self._set_user_bureau(user, role["asso"]["login"])
                if role["role"]["name"] == u"Resp Info":
                    self._set_user_geek(user, role["asso"]["login"])


        return user



    # rights getter/setters
    def _test_groups(self):
        try:
            Group.objects.get(name="simde")
            Group.objects.get(name="bde")
            Group.objects.get(name="president")
            Group.objects.get(name="bureau")
            Group.objects.get(name="geek")
        except Exception as e:
            Group.objects.get_or_create(name="simde")
            Group.objects.get_or_create(name="bde")
            Group.objects.get_or_create(name="president")
            Group.objects.get_or_create(name="bureau")
            Group.objects.get_or_create(name="geek")
            # TODO: add permissions

    def _reset_user_rights(self, user):
        user.groups.clear()
        user.is_superuser = False

    def _set_user_simde(self, user):
        print("%s is in SiMDE" % user.get_username())
        g = Group.objects.get(name="simde")
        g.user_set.add(user)

    def _set_user_bde(self, user):
        print("%s is in BDE" % user.get_username())
        g = Group.objects.get(name="bde")
        g.user_set.add(user)

    def _set_user_superadmin(self, user):
        print("%s is in superadmin" % user.get_username())
        user.is_superuser = True

    def _set_user_president(self, user, asso_name):
        print("%s is president in %s" % (user.get_username(), asso_name))
        print("ERROR: TODO set_president")
        g = Group.objects.get(name="president")
        g.user_set.add(user)
        pass

    def _set_user_bureau(self, user, asso_name):
        print("%s is bureau in %s" % (user.get_username(), asso_name))
        print("ERROR: TODO set_bureau")
        g = Group.objects.get(name="bureau")
        g.user_set.add(user)
        pass

    def _set_user_geek(self, user, asso_name):
        print("%s is geek in %s" % (user.get_username(), asso_name))
        print("ERROR: TODO set_geek")
        g = Group.objects.get(name="geek")
        g.user_set.add(user)
        pass