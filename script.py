import requests as re
import json
import pandas as pd
import datetime as dt
import os
import argparse
from openpyxl import load_workbook
from urllib.parse import unquote
import config

pd.options.mode.chained_assignment = None


class API():

    # API URL Endpoint
    f = open('api.json')
    data = json.load(f)
    apiEndPoint = data['apiEndPoint']
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.29.2',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    def __str__(self):
        return f"API Endpoint: {self.apiEndPoint}"

    def fetch_data(self, countryId):
        r = re.get(
            url=self.apiEndPoint,
            headers=self.headers,
            params={
                "distance": config.distance,
                "gender": config.gender,
                "stroke": config.stroke,
                "poolConfiguration": config.poolConfiguration,
                "year": config.year,
                "startDate": config.startDate,
                "endDate": config.endDate,
                "timesMode": config.timesMode,
                "pageSize": config.pageSize,
                "countryId": countryId,
            },
            allow_redirects=True,
        )
        return r


# Declaration of Variables for looping
countries_list = config.countries_list
countryId_list = []
csv = []
gender_full = ""
outputExcelFileName = " ".join([config.gender, config.distance, config.stroke]) + ".xlsx"


# Read Countries.json File to obtain country ID
def getCountryID():
    print("Countries: " + ", ".join(countries_list))
    with open("countries.json") as countries_json:
        file_contents = countries_json.read()

    parsed_json = json.loads(file_contents)

    for i in range(len(countries_list)):
        for j in range(len(parsed_json)):
            if parsed_json[j]["Name"] == countries_list[i]:
                countryId_list.append(parsed_json[j]["Id"])


# Loop through each country and call API with params
def callAPI():
    print("Downloading data using API...")
    for i in range(len(countryId_list)):
        r = API().fetch_data(countryId_list[i])

        if r.status_code != 200:
            print("Failed calling API!")
            print(r.text)
            exit
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
    print("Compiling data...")
    df = pd.DataFrame()
    writer = pd.ExcelWriter(outputExcelFileName, engine='openpyxl')

    for i in range(len(csv)):
        df_csv = pd.read_csv(csv[i])
        if len(df_csv) == 0:
            print("API returned no results found for", countries_list[i])
        df = pd.concat([df, df_csv], axis=0)

    df.drop(df[df['meet_name'] == "meet_name"].index, inplace=True)
    df['swim_date'] = pd.to_datetime(df['swim_date'], format='%d/%m/%Y').dt.date
    df.to_excel(writer, sheet_name="RAW", index=False)
    writer.close()


# Delete CSVs after Compilation
def deleteCSVs():
    for i in range(len(csv)):
        try:
            os.remove(csv[i])
        except Exception as e:
            print(e)


def cleanResults():
    print("Commencing data cleaning operations...")
    df = pd.read_excel(outputExcelFileName, sheet_name="RAW")
    df['swim_time'] = df['swim_time'].apply(lambda x: convertStrToSeconds(x))
    writer = pd.ExcelWriter(outputExcelFileName, mode='a', engine='openpyxl')
    df.to_excel(writer, sheet_name="CLEANED", index=False)
    writer.close()
    return


def convertStrToSeconds(x):
    # Data type is float (already in seconds, no conversion needed)
    if isinstance(x, str):
        # HH:MM:SS or HH:MM:SS.ms
        if x.count(":") == 2:
            colonIndex_1st = x.find(":")
            colonIndex_2nd = x.rfind(":")
            seconds = float(x[0:colonIndex_1st]) * 3600 + float(x[colonIndex_1st + 1:colonIndex_2nd]) * 60 + float(x[colonIndex_2nd + 1:])
        # MM:SS or MM:SS:ms
        elif x.count(":") == 1:
            colonIndex = x.find(":")
            seconds = float(x[0:colonIndex]) * 60 + float(x[colonIndex + 1:])
        else:
            seconds = float(x)
    elif isinstance(x, int) or isinstance(x, float):
        seconds = x

    return seconds


# Filter RAW Data by Athlete Name defined in namelist.csv and seprate into different sheets by year (2019-2023, 2022-2023 & 2023)
def filterNames(targetFileName=outputExcelFileName):
    print("Begin filtering data using namelist.csv...")
    df_filtered = pd.DataFrame()
    try:
        df = pd.read_excel(targetFileName, sheet_name='CLEANED')
        df_namelist = pd.read_csv('namelist.csv', header=None)
    except Exception as e:
        print(e)
        quit()
    writer = pd.ExcelWriter(outputExcelFileName, mode='a', engine='openpyxl')

    for i in range(df_namelist.shape[0]):
        for j in range(df_namelist.shape[1]):
            df_filtered = pd.concat(
                [df_filtered, df[df['full_name_computed'] == df_namelist.at[i, j]]])
    df_filtered.to_excel(writer, sheet_name="Competitors 2019-2023", index=False)

    df_filtered2022to2023 = df_filtered[
        (df_filtered['swim_date'].dt.year == 2022) | (
            df_filtered['swim_date'].dt.year == 2023)
    ]
    df_filtered2022to2023.to_excel(writer, sheet_name="Competitors 2022-2023", index=False)

    df_filtered2023 = df_filtered[df_filtered['swim_date'].dt.year == 2023]
    df_filtered2023.to_excel(writer, sheet_name="Competitors 2023", index=False)
    writer.close()


def parseScriptArguments():
    description = "This is a python script to automate data collection and cleaning of FINA's results retrieved from FINA website's backend API."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-scrapeonly", "--ScrapeOnly", action='store_true',
                        help="Passing this argument will only run scrapping but not filter scrapped and cleaned data by namelist.csv.")
    parser.add_argument("-filteronly", "--FilterOnly", action='store_true',
                        help="Passing this argument will not run scrapping but only filter existing cleaned data by namelist.csv.")
    parser.add_argument("-t", "--TargetFileName", help="Define Output file name of Scrapped Results (without '.xlsx' extension)")
    args = parser.parse_args()

    if args.ScrapeOnly:
        print(" ".join(["Getting results for:", config.gender, config.distance, config.stroke,
                        "(" + unquote(config.startDate), "to", unquote(config.endDate) + ")"]))
        getCountryID()
        callAPI()
        compileCSV()
        deleteCSVs()
        cleanResults()
        print("Script ran successfully!")
    elif args.FilterOnly:
        if args.TargetFileName:
            filterNames(args.TargetFileName)
            print("Script ran successfully!")
        else:
            print("Please provide target excel file name for filtering operations.")
    else:
        print(" ".join(["Getting results for:", config.gender, config.distance, config.stroke,
                        "(" + unquote(config.startDate), "to", unquote(config.endDate) + ")"]))
        getCountryID()
        callAPI()
        compileCSV()
        deleteCSVs()
        cleanResults()
        filterNames()
        print("Script ran successfully!")
    return


def main():
    parseScriptArguments()


if __name__ == "__main__":
    main()
