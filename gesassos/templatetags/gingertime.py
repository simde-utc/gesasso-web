# -*- coding: utf-8 -*-

from django import template
from datetime import datetime
import pytz
from tzlocal import get_localzone # $ pip install tzlocal

register = template.Library()

@register.filter(name='ginger_date_to_human') 
def ginger_date_to_human(date_str):
    date = datetime.strptime(date_str[0:-5],"%Y-%m-%dT%H:%M:%S")
    # Add UTC time zone
    date = datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, date.microsecond, tzinfo=pytz.utc)
    localDate = date.astimezone(get_localzone())
    if localDate.date() == datetime.today().date():
        ret = "aujourd'hui à " + localDate.strftime("%H:%M:%S")
    else:
        ret = "le " + localDate.strftime("%d/%m/%Y à %H:%M:%S")
    return ret
