#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI.
# Your task is to process the HTML using BeautifulSoup, extract the hidden
# form field values for "__EVENTVALIDATION" and "__VIEWSTATE" and set the appropriate
# values in the data dictionary.
# All your changes should be in the 'extract_data' function
import lxml
import os

from bs4 import BeautifulSoup
import requests
import json
import shutil

html_page = "data/Data_Elements.html"
expath="data/transtats_bts_gov"

def extract_option(page,id):
    data = []

    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        opts = soup.find(id=id)
        for opt in opts.find_all('option'):
            if 'All' not in (opt['value']):
              data.append(opt['value'])

    return data


def return_state(page,id, airport):
    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        opts = soup.find(id=id)
        text= opts.find('option', {'value':airport}).get_text()
        state = text.split(",")[1].strip().split()[0]
        state = state[:-1]

    return state


def extract_requestform(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    with open(page, "r") as html:
        soup = BeautifulSoup(html, "html.parser")
        eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]
        viewstate = soup.find("input", {"name": "__VIEWSTATE"})["value"]
        data["eventvalidation"] = eventvalidation
        data["viewstate"] = viewstate

    return data


def make_request(data_form, airport, carrier):
    eventvalidation = data_form["eventvalidation"]
    viewstate = data_form["viewstate"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                      data={'AirportList': airport,
                            'CarrierList': carrier,
                            'Submit': 'Submit',
                            "__EVENTTARGET": "",
                            "__EVENTARGUMENT": "",
                            "__EVENTVALIDATION": eventvalidation,
                            "__VIEWSTATE": viewstate
                            }, verify=False)

    return r.text


if __name__ == "__main__":
    airports=extract_option(html_page,'AirportList')
    carriers= extract_option(html_page,'CarrierList')
    request_form= extract_requestform(html_page)
    for a in airports:
        s = return_state(html_page, 'AirportList', a)
        for c in carriers:
            html = make_request(request_form,a,c)
            export_file="{0}-{1}-{2}.html".format(c, a, s)
            # Full path to export file
            export_path = os.path.join(expath, export_file)

            # Open export file for writing
            with open(export_path, "w") as f:
                f.write(html)


    # print(make_request(request_form,'ATL','AS'))