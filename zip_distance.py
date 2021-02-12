"""Project: echo-distance-calculator
Developed for Echo Church
https://echo.church/
Author: Anthony Lozano
Email: alozano805@gmail.com
Date: 01/18/2021
Version 0.3
Desc: This tool takes in a list of address as a text file and calculates
the longitude and latitude between the two distances"""
import json
import re
import sys
import argparse

import pandas as pd
from numpy import random

# TODO: Replace key below with proper key from Google API. This is a randomly generated filler key
APIKEY = "BVeRvyYl9Yecr8Oe1tZZrOrQg0Gn15zrKxGa2vl"
distance_dict = {}
zips_seen = []
df_zips_seen = pd.read_csv('datasets/input_zip_dist.csv', index_col=["Zip"])
df_input_address = pd.read_csv('echo/newaddresssince1232021.csv', index_col=["Email"])


def check_if_california(zip_code):
    """Checks if the zip code is in California or not.
    California zip codes are between 90000 and 96100

    Args:
        zip_code (): [description]

    Returns:
        boolian: if the zip code is in california or not
    """
    zip_three_digits = ((zip_code[0:3]))
    zip_three_digits = int(zip_three_digits)
    if 899 < zip_three_digits < 962:
        print(f"{zip_code} IS in California")
        return True
    else:
        print(f"{zip_code} is NOT in California")
        return False


def check_address(members_address, campus):
    import requests

    r = requests.get(f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"
                     f"&origins={members_address}"
                     f"&destinations={campus}"
                     f"&key={APIKEY}")
    if r.status_code != 200:
        print(f"HTTP status code {r.status_code} received, program terminated.")
        sys.exit()
    else:
        try:
            json_data = r.json()

            if json_data.get("status") == "REQUEST_DENIED":
                print("API Key is broken or google can't find the address, please fix it")
                sys.exit()
            else:
                print(json_data.get("rows"))

        except ValueError as e:
            print('Error while parsing JSON response, program terminated.')
            print(e)
            sys.exit()
    return json.dumps(json_data)
 
def search_new_zip(searching_zip_code, campus_array):
    zip_code = {}
    smallest_distance = 10000000
    in_california = check_if_california(searching_zip_code)
    
    campus_dict =  {"NSJ": "1180 Murphy Ave San Jose, CA 95131",
                    "SSJ": "100 Skyway Dr, San Jose, CA 95111",
                    "SUN": "1145 E. Arques Ave Sunnyvale, CA 94085",
                    "FRE": "48989 Milmont Dr, Fremont, CA 94538"}

    if in_california is True:
        for single_campus in campus_array: 

            campus = campus_dict.get(single_campus, "NSJ")
            json_api_resp = check_address(searching_zip_code, campus)
            api_data = json.loads(json_api_resp)
            current_distance = api_data['rows'][0]['elements'][0]['distance']['value']
            current_duration = api_data['rows'][0]['elements'][0]['duration']['value']

            # current_distance = (random.randint(90,100))
            # current_duration = 100

            zip_code[f"{single_campus}_DIST"]=current_distance
            zip_code[f"{single_campus}_TIME"]=current_duration

            if current_duration < smallest_distance:
                smallest_distance = current_duration
                closest_campus = single_campus
        zip_code["Campus"]=closest_campus

    else:
        zip_code = {"NSJ_DIST": None,
                    "NSJ_TIME": None,
                    "SSJ_DIST": None,
                    "SSJ_TIME": None,
                    "SUN_DIST": None,
                    "SUN_TIME": None,
                    "FRE_DIST": None,
                    "FRE_TIME": None,
                    "Campus":  "NSJ"}
    
    df = pd.DataFrame(zip_code, index=[searching_zip_code])
    with open('datasets/input_zip_dist.csv', 'a') as f:
        df.to_csv(f, header=False)
    return zip_code.get("Campus", "NSJ")
     

def main():
    # First step is to check how many unique zip codes are in the file
    for index in range(len(df_input_address)):
        each_line = df_input_address.T.loc["Address"][index]
        f_zip_code = re.findall(r'.*(\d{5}).*?$', each_line)
        f_zip_code = int(f_zip_code[-1])

        try:
        # Check if we've seen this zip code before in the input dataset
            proper_campus = df_zips_seen.loc[f_zip_code]['Campus']
            # proper_campus = pandas_campus.iloc[0]
            
        except KeyError:
            proper_campus = search_new_zip(str(f_zip_code), ["NSJ", "SSJ", "SUN", "FRE"])

        # Now we have updated the database with the newest info
        member_campus = df_input_address.iloc[index]["Campus"]= proper_campus
    df_input_address.to_csv("datasets/output.csv")


if __name__ == "__main__":
    main()
