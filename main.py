"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Silvie Pelanova
email: silvie.pelanova@gmail.com
discord: silvie4181
"""

import requests
import bs4
import sys
import os
from bs4 import BeautifulSoup
import csv

if len(sys.argv) != 3:                                                                  #If not 3 arguments, tzn. script name
    print("Zadej dva argumenty (webovou adresu a nazev csv souboru)")                   #and web page and name of csv file, 
    quit()                                                                              #print message to the user and close program

url = sys.argv[1] 
print(f"Downloading data from url {url}")                                               #argument 1, web page
file_name = sys.argv[2]                                                                 #argument 2, name of csv file

directory = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')            #path tothe desktop
path_to_file = os.path.join(directory, sys.argv[2])                                     #path to the csv file on desktop

def make_soup(url):
    server_response = requests.get(url)
    soup = BeautifulSoup(server_response.text, 'html.parser')
    return soup

def save_data(complete_header_set: list, complete_data_set: list, path_to_file: str) -> str:  #save to file, write header and data
    with open(path_to_file, mode="w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(complete_header_set)
        csv_writer.writerows(complete_data_set)

def get_all_villages(all_tables: list):                                                        #get list of all cities in choosen dinstinct
    list_of_rows = []
    for table in range(len(all_tables)):
        for row in all_tables[table].findAll('tr'):
            list_of_cols = []
            link_to_sum_results = ""
            for idx, cell in enumerate(row.findAll('td')):
                if idx == 0:
                    if cell.text != "-": list_of_cols.append(cell.text)                         #only rows on index 0(city number) which are not empty
                    link_element = cell.find("a")
                    if link_element: link_to_sum_results = "https://volby.cz/pls/ps2017nss/" + link_element.get("href")
                if idx == 1:                                                                    #only rows on index 1 (city name) which are not empty
                    if cell.text != "-": list_of_cols.append(cell.text)
                if idx == 2:                                                                    #only rows on index 2 (links on tables with election data) which are not empty
                    if cell.text != "-": list_of_cols.append(link_to_sum_results)
            if len(list_of_cols) > 0: 
                list_of_rows.append(list_of_cols)
    return list_of_rows

def get_all_villages_data(all_villages: list):                                  #get data only from the first table with overall data about the precinct
    list_of_rows = []
    for village in all_villages:
        table_sum = make_soup(village[2]).find("table", class_="table", id="ps311_t1")          
        for row in table_sum.findAll('tr'):
            list_of_cols = []
            for cell in row.findAll('td'):
                header_attr = cell.get('headers', '')
                if "sa2" in header_attr:
                    list_of_cols.append(cell.text)
                elif "sa3" in header_attr:
                    list_of_cols.append(cell.text)
                elif "sa6" in header_attr:
                    list_of_cols.append(cell.text)
            if len(list_of_cols) > 0: 
                list_of_rows.append(list_of_cols)
    return list_of_rows

def get_all_villages_votes(all_villages: list):                                 #get election details from the tables with electoral parties
    list_of_rows = []
    for village in all_villages:
        tables = [table for table in make_soup(village[2]).find_all("table", class_="table") if table.get("id") != "ps311_t1"]
        list_of_cols = []
        for table in tables:
            for row in table.findAll('tr'):
                for cell in row.findAll('td'):
                    header_attr = cell.get('headers', '')                   
                    if "t1sa2" in header_attr and "t1sb3" in header_attr:
                        list_of_cols.append(cell.text)
                    elif "t2sa2" in header_attr and "t2sb3" in header_attr:
                        list_of_cols.append(cell.text)
        if len(list_of_cols) > 0: 
            list_of_rows.append(list_of_cols)
    return list_of_rows

def get_complete_header_set(all_villages: list):                               #create header using list
    table_headers = []
    table_headers.append("code")
    table_headers.append("location")
    table_headers.append("registered")
    table_headers.append("envelopes")
    table_headers.append("valid")

    tables = [table for table in make_soup(all_villages[0][2]).find_all("table", class_="table") if table.get("id") != "ps311_t1"]  #header part with names of electoral parties
    for table in tables:
        for row in table.findAll('tr'):
            for cell in row.findAll('td'):
                header_attr = cell.get('headers', '')                   
                if "t1sa1" in header_attr and "t1sb2" in header_attr:
                    if cell.text != "-": table_headers.append(cell.text)
                if "t2sa1" in header_attr and "t2sb2" in header_attr:
                    if cell.text != "-": table_headers.append(cell.text)
    return table_headers

def get_complete_data_set(all_villages: list, all_villages_data: list, all_villages_votes: list):              #content data
    complete_data_set = []
    for i in range(len(all_villages)):
        row_data_set = []
        row_data_set.append(all_villages[i][0])
        row_data_set.append(all_villages[i][1])
        row_data_set.append(all_villages_data[i][0])
        row_data_set.append(all_villages_data[i][1])
        row_data_set.append(all_villages_data[i][2])
        for j in range(len(all_villages_votes[i])):
            row_data_set.append(all_villages_votes[i][j])        
        complete_data_set.append(row_data_set)
    return complete_data_set

all_villages = get_all_villages(make_soup(url).find_all("table", {"class":"table"}))
print("..all_villiges loaded")
all_villages_data = get_all_villages_data(all_villages)
print("..all_villages_data loaded")
all_villages_votes = get_all_villages_votes(all_villages)
print("..all_villages_votes loaded")
complete_header_set = get_complete_header_set(all_villages)
print("..complete_header_set ready to be saved")
complete_data_set = get_complete_data_set(all_villages, all_villages_data, all_villages_votes)
print("..complete_data_set ready to be saved")

print(f"Saving data into file {file_name}")    
save_data(complete_header_set, complete_data_set, path_to_file)

print("Closing election sraper")
quit()
