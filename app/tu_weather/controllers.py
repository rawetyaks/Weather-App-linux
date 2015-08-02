# -*- coding: utf-8 -*-

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import module models (i.e. User)
# from app.tu_weather.models import User
# from app.tu_weather.models import User

# Import the verious activities that need to happen.
import scripts

from codecs import encode, decode


# Define the blueprint: 'tu_w', it is the basic point of access for the site.
tu_weather = Blueprint('tu_w', __name__, url_prefix='/')

# Set the route and accepted methods
@tu_weather.route('/', methods=['GET'])
def tu_weather_main():
    all_data = scripts.fetch_all_city_data("5110629")
    del all_data['id']
    del all_data[u'coord']
    del all_data[u'base']
    del all_data['cod']
    del all_data['wind']
    del all_data['visibility']
    del all_data['sys']
    del all_data['clouds']

    all_data_translated = scripts.translate(all_data, "tus", "eng")

    city_name = decode(all_data_translated["city_name"], "utf-8")

    mmddyy_numeric = all_data_translated["mmddyy"]
    spelled_out_mmddyy = decode(all_data_translated["spelled_out_mmddyy"], "utf-8")

    weather_desc = all_data_translated["weather_desc"]

    temp_min = all_data_translated["temp_min"]
    temp_cur = all_data_translated["temp_cur"]
    temp_max = all_data_translated["temp_max"]

    temp = scripts.fetch_entry("Buffalo, NY","temp")[0:2]

    del all_data['eng_time_data']
    del all_data[u'name']
    del all_data[u'main']
    del all_data[u'weather']
    return render_template("base.html   ", all_data=all_data,
                           city_name=city_name,
                            spelled_out_mmddyy=spelled_out_mmddyy,
                            mmddyy_numeric=mmddyy_numeric,
                            weather_desc=weather_desc,
                            temp_min=temp_min,
                            temp_cur=temp_cur,
                            temp_max=temp_max,
                            temp=temp)