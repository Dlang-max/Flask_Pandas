# 1.1 Software Title
Data Visualization of CTDD IT Server Data Flask App

# 1.1 Purpose
The purpose of the Data Visualization of CTDD IT Server Data Flask App is to display metadata associated with CTDD IT data transfers, making monitoring of these transfers easier.  

## Technical Overview

### Technical Specifications
+ Containerization Platform: Docker for containerizing the application and managing deployment
+ Programming Languages: Python for backend, HTML, CSS, and JavaScript for frontend.
+ Important Python Packages: flask and pandas
+ Web Servers: Gunicorn to run Flask app, Nginx to handle HTTP requests and serve static CSS files.
+ Operating System: Ubuntu 22.04

### Functionality
The Flask app builds a pandas DataFrame using the previous 30 days worth of CSV files from the data directory. This pandas DataFrame contains metadata associated with all CTDD IT data transfers over the past 30 days. Using this data, the Flask app builds a new pandas DataFrame that represents whether a study's data transfer was successful, unsuccessful, or not run on a given date. This new pandas DataFrame gets displayed as an HTML table by the Flask app, allowing for easy visualization of CTDD IT data transfers. Each day a cron job runs at 10:00 AM EST to rebuild both pandas DataFrames using metadata from the current date. 


### Installation Instructions
1. **Install Docker** 
+ To run this Flask app locally install [Docker Desktop](https://docs.docker.com/get-docker/).
+ To run this Flask app on a remote server install [Docker Engine](https://docs.docker.com/engine/install/).

2. **Clone the git repository** ***Change***
```bash
git clone https://github.com/Dlang-max/Flask_Pandas.git
```
3. **Move into the Data Visualization Flask App Directory**
```bash
cd "Data Visualization Flask App"/
```

4. **Build and run Docker containers**
```bash
docker compose -f compose.nginx.yaml up -d --build
```

5. Navigate to [http://localhost:1337/](http://localhost:1337/) for visualization of CTDD IT server data. ***Change***


## Maintainer(s)
Daniel Lang - langd052405@gmail.com

## License
All rights reserved by [Roswell Park Comprehensive Cancer Center](https://www.roswellpark.org) and the [Clinical Trial Development Division](https://www.ctdd.org) 