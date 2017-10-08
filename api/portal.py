
from django.conf import settings
from urllib import urlopen, urlencode
from urlparse import urljoin
import json

def get_roles(user):
    url = urljoin(settings.PORTAL_SERVER_URL, "profile/" + str(user) + "/json")
    response = urlopen(url).read()
    json_data = json.loads(response.decode())

    semester_ids = json_data['semestres'].keys()
    semester_ids.sort(key=int)
    last_semester_id = semester_ids[-1]

    # print(json_data['semestres'][last_semester_id])

    # Check it is current semester # TODO: make the portal API do this check on its own
    current_semester = "A17"

    if "groups" in json_data:
        groups_return = json_data["groups"]
    else:
        groups_return = False

    superadmin_return = "superadmin" in json_data and json_data["superadmin"]

    if current_semester == json_data['semestres'][last_semester_id]["semestre"]:
        current_semester_id = last_semester_id
        roles_return = json_data['semestres'][current_semester_id]["roles"]
    else:
        roles_return = False

    return superadmin_return, groups_return, roles_return