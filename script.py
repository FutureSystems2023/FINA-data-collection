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
distance = "400"  # e.g. (50, 100, 200, 400, 800, 1500) Change as appropriate
gender = "F"  # e.g. (M or F) Change as appropriate
stroke = "MEDLEY"  # e.g. (FREESTYLE, FREESTYLE_RELAY) Change as appropriate
poolConfiguration = "LCM"
year = ""  # year leave blank if filtering by date
startDate = "01%2F01%2F2019"
endDate = "12%2F31%2F2022"
timesMode = "ALL_TIMES"
pageSize = "200"
countryId = ""

# Define Countries to get results from
countries_list = [
    "Philippines",
    "Singapore",
    "Malaysia",
    "Vietnam",
    "Indonesia",
    "Thailand",
    "Brunei Darussalam",
    "Myanmar",
    "Lao People's Democratic Republic",
    "Cambodia",
    "Democratic Republic of Timor - Leste",
]

# Declaration of Variables for looping
countryId_list = []
csv = []
gender_full = ""


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
    excelFileName = " ".join([gender, distance, stroke]) + ".xlsx"
    writer = pd.ExcelWriter(excelFileName)
    for i in range(len(csv)):
        df = pd.read_csv(csv[i])
        sheet_name = csv[i]
        df.to_excel(writer, sheet_name=sheet_name[0:-4], index=False)
    writer.save()


# Delete CSVs after Compilation
def deleteCSVs():
    for i in range(len(csv)):
        os.remove(csv[i])


def main():
    print(" ".join(["Getting results for:", gender, distance, stroke]))
    print("Countries: " + ", ".join(countries_list))
    getCountryID()
    callAPI()
    compileCSV()
    deleteCSVs()
    print("Results downloaded and compiled succesfully!")


main()
