
from django.conf import settings
from urllib import urlopen, urlencode
from urlparse import urljoin
import json

def get_user(user):
    params = {'key': settings.GINGER_KEY, }
    url = urljoin(settings.GINGER_SERVER_URL, user.get_username()) + \
        '?' + urlencode(params)
    page = urlopen(url)
    response = page.read()
    json_data = json.loads(response.decode())

    ret = {
        "surname": json_data.get('prenom'),
        "name": json_data.get('nom'),
        "email": json_data.get('mail'),
        "is_adult": json_data.get('is_adulte'),
        "is_contributor": json_data.get('is_cotisant'),
    }

    return ret