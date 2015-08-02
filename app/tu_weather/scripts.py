# -*- coding: utf-8 -*-

import requests
import time
import csv
import unicodecsv
import codecs
from collections import namedtuple as nt

from models import TranslationStrings



api_key = "bfe25b83ff54b07a107118764a3919e7"

def fetch_all_city_data(city_code):
    url = "http://api.openweathermap.org/data/2.5/weather/?id=" + city_code + "&APPID=" + api_key \
          + "&units=imperial"
    req = requests.get(url)
    json_data = req.json()

    ### PARSE TIME DATA
    ### change the dt entry to a data set which is more
    ### easily transcribed/translated
    time_struct = time.localtime(json_data["dt"])
    readable_time_data = parse_time_data(time_struct)
    json_data["eng_time_data"] = readable_time_data
    del json_data["dt"]


    return(json_data)

def parse_time_data(time_struct):
    readable_time_data = dict()

    readable_time_data["day_of_week"] = time.strftime("%A", time_struct)
    readable_time_data["day_number"] = time.strftime("%d", time_struct)
    readable_time_data["month_name"] = time.strftime("%B", time_struct)
    readable_time_data["month_number"] = time.strftime("%m", time_struct)
    readable_time_data["year"] = time.strftime("%y", time_struct)

    readable_time_data["hour"] = time.strftime("%I", time_struct)
    readable_time_data["minute"] = time.strftime("%M", time_struct)

    return(readable_time_data)

def parse_temp_data_to_words(temp_number):
    temp_str = str(temp_number)

    temp_words = []

    split_temp_str = temp_str.split(".")

    if len(split_temp_str) < 3:
        num_list = list(split_temp_str[0])

        if len(num_list) == 3:
            hundreds = str(num_list[0]) * 100
            tens = str(num_list[1]) * 10
            ones = str(num_list[2])

            matching_hun = TranslationStrings.query.filter_by(eng_label=hundreds).first()
            matching_ten = TranslationStrings.query.filter_by(eng_label=tens).first()
            matching_one = TranslationStrings.query.filter_by(eng_label=ones).first()

            tus_hun = matching_hun.tus_label
            tus_ten = matching_ten.tus_label
            tus_one = matching_one.tus_label

            print(tus_hun + " " + tus_ten + " " + tus_one)

        elif len(num_list) == 2:
            tens = int(num_list[0]) * 10
            ones = num_list[1]

            matching_ten = TranslationStrings.query.filter_by(eng_label=tens).first()
            matching_one = TranslationStrings.query.filter_by(eng_label=ones).first()

            tus_ten = matching_ten.tus_label
            tus_one = matching_one.tus_label

            temp_words = tus_ten + " " + tus_one
            print(temp_words)

    return temp_words

def translate(data, to_lang, from_lang):
    translations = dict()

    city_name = ""
    kvp_city = [("eng", x, str(data[u"name"])) for x in data]
    for triplet in kvp_city:
        matching = TranslationStrings.query.filter_by(eng_label=triplet[2]).first()
        if matching:
            city_name = matching.tus_label
            translations["city_name"] = codecs.encode(city_name, "utf-8")



    kvp_time = [("eng", x, str.lower(data["eng_time_data"][x])) for x in data["eng_time_data"]]\

    numeric_date_MM_dd_yy = data["eng_time_data"]["month_number"] + "/" + data["eng_time_data"]["day_number"] \
                            + "/" + data["eng_time_data"]["year"]

    trans_month_name = ""
    trans_day_number = ""
    trans_year = ""

    for triplet in kvp_time:
        matching = TranslationStrings.query.filter_by(eng_label=triplet[2]).first()

        if matching:
            if triplet[1] == "month_name":
                trans_month_name = matching.tus_label
            elif triplet[1] == "day_number":
                trans_day_number = matching.tus_label
            elif triplet[1] == "year":
                trans_year = matching.tus_label

            translations["spelled_out_mmddyy"] =    codecs.encode(trans_month_name + " " + \
                                                            trans_day_number + ", " + \
                                                            trans_year, "utf-8")

        translations["mmddyy"] = numeric_date_MM_dd_yy

    temp_max = ""
    temp_cur = ""
    temp_min = ""

    kvp_temp = [data[u"main"][u"temp_min"], data[u"main"][u"temp"], data[u"main"][u"temp_max"]]
    trans_temps = []
    for temp in kvp_temp:
        tus_temp = parse_temp_data_to_words(temp)
        trans_temps.append(tus_temp)

    translations["temp_min"] = trans_temps[0]
    translations["temp_cur"] = trans_temps[1]
    translations["temp_max"] = trans_temps[2]

    kvp_weather = data[u"weather"][0][u'id']
    match = TranslationStrings.query.filter_by(super_id=kvp_weather).first()
    translations["weather_desc"] = match.tus_label


    return(translations)

def fetch_entry(city_name, entry_name):
    if city_name == "Buffalo, NY":
        city_code = "5110629"

    json_data = fetch_all_city_data(city_code)

    return(str(json_data["main"][entry_name]))

def load_translations_to_db(db):
    string_list = []

    with codecs.open("app\static\strings.txt", 'rb', encoding='utf-8') as f:
        data = unicode_csv_reader(f)

        for row in data:
            sid = row[0]
            eng = codecs.encode(row[1], "utf-8")
            tus = codecs.encode(row[2], "utf-8")

            temp_translation_string = TranslationStrings(sid, eng, tus)
            db.session.add(temp_translation_string)

        db.session.commit()

    return(string_list)

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data), dialect=dialect)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

