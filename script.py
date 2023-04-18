"""
# This script is to automate downloads of csv data files of swimming results from fina.org website
# API Url is as follow:
#   https://api.worldaquatics.com/fina/rankings/swimming/report/csv
# Parameters are as follows:
#   gender=F&distance=50&stroke=FREESTYLE&poolConfiguration=LCM&year=&startDate=01%2F01%2F2019&endDate=12%2F31%2F2022&timesMode=ALL_TIMES&regionId=&pageSize=200
"""


import requests as re
import json
import pandas as pd
import os

# API URL Endpoint
apiEndPoint = "https://api.worldaquatics.com/fina/rankings/swimming/report/csv"

# Parameters for requests
distance = "200"  # e.g. (50, 100, 200, 400, 800, 1500) Change as appropriate
gender = "F"  # e.g. (M or F) Change as appropriate
stroke = "FREESTYLE"  # e.g. (FREESTYLE, FREESTYLE_RELAY) Change as appropriate
poolConfiguration = "LCM"
year = ""  # year leave blank if filtering by date
startDate = "01%2F01%2F2019"
endDate = "05%2F05%2F2023"
timesMode = "ALL_TIMES"
pageSize = "200"
countryId = ""

# Define Countries to get results from
countries_list = [
    "Singapore",
    "Philippines",
    "Malaysia",
    "Vietnam",
    "Indonesia",
    "Thailand",
    "Myanmar"
]

# Declaration of Variables for looping
countryId_list = []
csv = []
gender_full = ""
excelFileName = " ".join([gender, distance, stroke]) + ".xlsx"

# Read Countries.json File to obtain country ID
def getCountryID():
    with open("countries.json") as countries_json:
        file_contents = countries_json.read()

    parsed_json = json.loads(file_contents)

    for i in range(len(countries_list)):
        for j in range(len(parsed_json)):
            if parsed_json[j]["Name"] == countries_list[i]:
                countryId_list.append(parsed_json[j]["Id"])


# Loop through each country and call API with params
def callAPI():
    for i in range(len(countryId_list)):
        countryId = countryId_list[i]
        r = re.get(
            apiEndPoint,
            params={
                "distance": distance,
                "gender": gender,
                "stroke": stroke,
                "poolConfiguration": poolConfiguration,
                "year": year,
                "startDate": startDate,
                "endDate": endDate,
                "timesMode": timesMode,
                "pageSize": pageSize,
                "countryId": countryId,
            },
            allow_redirects=True,
        )
        if countries_list[i] == "Democratic Republic of Timor - Leste":
            filename = "East Timor"
        elif countries_list[i] == "Lao People's Democratic Republic":
            filename = "Laos"
        elif countries_list[i] == "Brunei Darussalam":
            filename = "Brunei"
        else:
            filename = countries_list[i]
        csv.append(filename + ".csv")
        open(filename + ".csv", "wb").write(r.content)


# Compile CSV into one excel file
def compileCSV():
    writer = pd.ExcelWriter(excelFileName)
    df = pd.DataFrame()
    for i in range(len(csv)):
        df_csv = pd.read_csv(csv[i])
        df = pd.concat([df, df_csv], axis=0)
    df.drop(df[df['meet_name'] == "meet_name"].index, inplace=True)
    df.to_excel(writer,sheet_name="RAW", index=False)
    writer.save()


# Delete CSVs after Compilation
def deleteCSVs():
    for i in range(len(csv)):
        os.remove(csv[i])


# Filter RAW Data by Athlete Name defined in namelist.csv
def filterNames():
    writer = pd.ExcelWriter(excelFileName)
    df = pd.read_excel(excelFileName)
    df_namelist = pd.read_csv('namelist.csv',header=None)
    df_filtered = pd.DataFrame()
    for i in range(df_namelist.shape[0]):
        for j in range(df_namelist.shape[1]):
            df_filtered = pd.concat([df_filtered, df[df['full_name_computed'] == df_namelist.at[i, j]]])
    df.to_excel(writer,sheet_name="Competitors 2019-2023", index=False)
    writer.save()


def main():
    '''
    print(" ".join(["Getting results for:", gender, distance, stroke]))
    print("Countries: " + ", ".join(countries_list))
    getCountryID()
    callAPI()
    compileCSV()
    deleteCSVs()
    print("Results downloaded and compiled succesfully!")
    '''
    filterNames()

main()
