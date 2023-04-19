# **Documentation**

This python script is to automate the results collection from <a href="fina.org">Fina website</a>.
CSVs will be downloaded and be compiled into one Excel file based on user specified parameters.

<hr>

## **Requirements (Installation)**

Change into current directory and run pip to install required packages using the following command

<pre><code>pip install requirements.txt</code></pre>
<hr>

## **API Endpoint**

API Endpoint is:

<pre><code>https://api.worldaquatics.com/fina/rankings/swimming/report/csv</code></pre>

## **Parameters**

<pre>
    <code>
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
    </code>
</pre>

### **Whereby:**

- **distance** = Distance in metres [e.g. (50, 100, 200, 400, 800, 1500)]
- **gender** = M is Men, F is Women [e.g. (M or F)]
- **stroke** = Stroke or Style <u>in CAPS</u> [e.g. (FREESTYLE, FREESTYLE_RELAY, BACKSTROKE, BUTTERFLY, MEDLEY)]
- **poolConfiguration** = Pool configuration/length [e.g. LCM or SCM (LCM is 50m, SCM is 25m)]
- **year** = Year filter (leave blank if filtering by date range)
- **startDate** = Filter by Start Date (<u>in URL encoded format</u>) [e.g. 01/01/2019 will be "01%2F01%2F2019", whereby %2F denotes a "/"]
- **endDate** = Filter by End Date (<u>in URL encoded format</u>) [e.g. 31/12/2022 will be "31%2F12%2F2022", whereby %2F denotes a "/"]
- **timesMode** = Get all timings or only best timings [e.g. (ALL_TIMES, BEST_TIMES)]
- **countryId** = ID of country (this is referenced from [countries.json](countries.json) file, id is provided by FINA website and can be found using network tab of developer console)

<br/>

### **Changing Parameters**

Edit the parameters in the following code block in [script.py](script.py) line 18

<pre>
    <code>
        # Parameters for requests
        distance = "200"  # e.g. (50, 100, 200, 400, 800, 1500) Change as appropriate
        gender = "F"  # e.g. (M or F) Change as appropriate
        stroke = "FREESTYLE_RELAY"  # e.g. (FREESTYLE, FREESTYLE_RELAY) Change as appropriate
        poolConfiguration = "LCM"
        year = ""  # year leave blank if filtering by date
        startDate = "01%2F01%2F2019"
        endDate = "12%2F31%2F2022"
        timesMode = "ALL_TIMES"
        pageSize = "200"
        countryId = ""
    </code>
</pre>

<br/>

### **Changing Countries**

Edit the countries that you would like to get results for in the following code block in [script.py](script.py) line 30. Ensure that country name is the same as that defined in fina website.

<pre>
    <code>
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
    </code>
</pre>
