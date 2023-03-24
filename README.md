# Documentation

This is script is to automate the results collection from <a href="fina.org">Fina website</a>.
CSVs will be downloaded and be compiled into one Excel file based on user specified parameters.

<hr>

## API Endpoint

API Endpoint is:

<pre><code>https://api.worldaquatics.com/fina/rankings/swimming/report/csv</code></pre>

## Parameters

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

### Whereby:

- **distance** = Distance in metres [e.g. (50, 100, 200, 400, 800, 1500)]
- **gender** = M is Men, F is Women [e.g. (M or F)]
- **stroke** = Stroke or Style <u>in CAPS</u> [e.g. (FREESTYLE, FREESTYLE_RELAY, BACKSTROKE, BUTTERFLY, MEDLEY)]
- **poolConfiguration** = Pool configuration/length [e.g. LCM or SCM (LCM is 50m, SCM is 25m)]
- **year** = Year filter (leave blank if filtering by date range)
- **startDate** = Filter by Start Date (<u>in URL encoded format</u>) [e.g. 01/01/2019 will be "01%2F01%2F2019", whereby %2F denotes a "/"]
- **endDate** = Filter by End Date (<u>in URL encoded format</u>) [e.g. 31/12/2022 will be "31%2F12%2F2022", whereby %2F denotes a "/"]
- **timesMode** = Get all timings or only best timings [e.g. (ALL_TIMES, BEST_TIMES)]
- **countryId** = ID of country (this is referenced from [countries.json](countries.json) file, id is provided by FINA website and can be found using network tab of developer console)