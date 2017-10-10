# -*- coding: utf-8 -*-

from django import template
from datetime import datetime

register = template.Library() 

@register.filter(name='ginger_date_to_human') 
def ginger_date_to_human(date_str):
    date = datetime.strptime(date_str[0:-5],"%Y-%m-%dT%H:%M:%S")
    if date.date() == datetime.today().date():
        ret = "aujourd'hui à " + date.strftime("%H:%M:%S")
    else:
        ret = "le " + date.strftime("%d/%m/%Y à %H:%M:%S")
    return ret
