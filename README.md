# 1.1 Software Title
Data Visualization of CTDD IT Server Data Flask App

# 1.1 Purpose
The purpose of the Data Visualization of CTDD IT Server Data Flask App is to display metadata associated with CTDD IT data transfers, making monitoring of these transfers easier.  

## Technical Overview

### Technical Specifications
+ Containerization Platform: Docker for containerizing the application and managing deployment
+ Programming Languages: Python for backend, HTML, CSS, and JavaScript for frontend
+ Important Python Packages: flask and pandas
+ Web Servers: Gunicorn to run Flask app, Nginx to handle HTTP requests and serve static CSS files
+ Operating System: Ubuntu 22.04

### Functionality
The Flask app builds a pandas DataFrame using the previous 30 days worth of CSV files from the data directory. This pandas DataFrame contains metadata associated with all CTDD IT data transfers over the past 30 days. Using this data, the Flask app builds a new pandas DataFrame that represents whether a study's data transfer was successful, unsuccessful, or not run on a given date. This new pandas DataFrame gets displayed as an HTML table by the Flask app, allowing for easy visualization of CTDD IT data transfers. When a new CSV file is uploaded to the data directory the flask app rebuilds both pandas DataFrames using metadata from the current date.

#### Endpoints
+ `/`: displays the error status of all data transfers over the past month
+ `/today`: displays the error status of all data transfers today
+ `/displaySingle/<col>`: displays the error status of a given study over the past week and month

### Installation Instructions
1. **Install Docker** 
+ To run this Flask app locally, install [Docker Desktop](https://docs.docker.com/get-docker/).

2. **Clone the git repository** ***Change***
```bash
git clone https://github.com/Dlang-max/Flask_Pandas.git
```
3. **Move into the `Data Visualization Flask App` Directory**
```bash
cd "Data Visualization Flask App"/
```

4. **Open the `compose.nginx.yaml` file**
+ For real-time data: Comment out `RUNNING_WITH_DATE_STRING` and `DATE_STRING`.

```yaml
    #- RUNNING_WITH_DATE_STRING=True
    #- DATE_STRING=2024-07-07
```

+ For specific date data: Uncomment `RUNNING_WITH_DATE_STRING` and `DATE_STRING`. Ensure `DATE_STRING` is formatted as YYYY-MM-DD (`DATE_STRING` is intended to be the date associated with the most recent NRG_N_TODAY_COMP_YYYYMMDD.csv file in the data directory).

```yaml
    - RUNNING_WITH_DATE_STRING=True
    - DATE_STRING=2024-07-07 #YYYY-MM-DD
```

5. **Build and run Docker containers**
```bash
docker compose -f compose.nginx.yaml up -d --build
```

6. Navigate to [http://localhost:1337/](http://localhost:1337/) for visualization of CTDD IT server data. ***Change***


## Maintainer(s)
Daniel Lang - daniel.lang@rowswellpark.org

## License
All rights reserved by [Roswell Park Comprehensive Cancer Center](https://www.roswellpark.org) and the [Clinical Trial Development Division](https://www.ctdd.org) 