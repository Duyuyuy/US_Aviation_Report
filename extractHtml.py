#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

The files are in a directory "data", named after the carrier and airport:
"{}-{}.html".format(carrier, airport), for example "FL-ATL.html".

The table with flight info has a table class="dataTDRight". Your task is to
use 'process_file()' to extract the flight data from that table as a list of
dictionaries, each dictionary containing relevant data from the file and table
row.

Note - year, month, and the flight data should be integers.
You should skip the rows that contain the TOTAL data for a year.

"""
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os
import lxml
import json

datadir = "data"
expath="data/extract_data"

# def open_zip(datadir):
#     with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
#         myzip.extractall()


# def process_all(datadir):
#     files = os.listdir(datadir)
#     return files


def process_file(f):
    """

    Note - year, month, and the flight data should be integers.
    You should skip the rows that contain the TOTAL data for a year.
    """
    data = []
    info = {}
    filename=f.split(".")[0].split("\\")[1]
    name=filename.split("-")
    info["airport"] = name[1]
    info["courier"]= name[0]
    info["state"] = name[2]

    with open(f, "r") as html:
        soup = BeautifulSoup(html, 'lxml')
        # trs = soup.find('table', class_='dataTDRight').find_all('tr', class_='dataTDRight')
        # for tr in trs:
        #     tds = tr.find_all('td')
        #     if tds[1].text != 'TOTAL':
        table = soup.find('table', id="GridView1")
        rows= table.find_all('tr', class_='dataTDRight')
        if rows!=None:
          for row in rows[1:]:
                cols = row.find_all("td")
                # cols = [ele.text.strip() for ele in cols]
                if "TOTAL" in row.text:
                  continue

                year = int(cols[0].text)
                month = int(cols[1].text)
                domestic = int(cols[2].text.replace(',', ''))
                international = int(cols[3].text.replace(',', ''))
                data.append({
                    'courier': info['courier'],
                    'airport_info': {
                        'airport': info['airport'],
                        'state': info['state']},
                    'year': year,
                    'month': month,
                    'flights': {
                            'domestic': domestic,
                            'international': international}})
        return data


def test():
    data = []
    # Test will loop over three data files.
    for filename in os.listdir('data/transtats_bts_gov'):
        # Check if the file is a regular file (not a directory)
        if os.path.isfile(os.path.join('data/transtats_bts_gov', filename)):
         data = process_file(os.path.join('data/transtats_bts_gov', filename))
         export_file = filename.split(".")[0] +'.json'
       # Full path to export file
         export_path = os.path.join(expath, export_file)

       # Open export file for writing
         with open(export_path, "w", encoding="utf-8") as f:
           json.dump(data, f)

test()