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
        Configures a user using Ginger
        :param user: The User to configure
        :return: The configurated user
        """
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

        return user
