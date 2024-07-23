# 1.1 Software Title
Data Visualization of CTDD IT Server Data Flask App

# 1.1 Purpose
The purpose of the Data Visualization of CTDD IT Server Data Flask App is to display metadata associated with CTDD IT data transfers, making monitoring of these transfers easier.  

## Technical Overview

access CSV files for data directory
use pandas to build a dataframe containing meta info.
display this info using a Flask app
Cron job runs every day at 10:00 AM EST to built today's dataframe.


### Technical Specifications
+ Containerization Platform: Docker for containerizing the application and managing deployment
+ Programming Languages: Python for backend, HTML, CSS, and JavaScript for frontend.
+ Important Python Packages: flask and pandas
+ Web Servers: Gunicorn to run Flask app, Nginx to handle HTTP requests and serve static CSS files.
+ Operating System: Ubuntu 22.04 

### Installation Instructions
1. **Install Docker** 
+ To run this Flask app locally install [Docker Desktop](https://docs.docker.com/get-docker/).
+ To run this Flask app on a remote server install [Docker Engine](https://docs.docker.com/engine/install/).

2. **Clone the git repository**
```bash
git clone __repo_url__
```
3. **Move into the Data Visualization Flask App Directory**
```bash
cd "Data Visualization Flask App"/
```

4. **Build and run Docker containers**
```bash
docker compose -f compose.nginx.yaml up -d --build
```

5. Navigate to [http://localhost:1337/](http://localhost:1337/) for visualization of CTDD IT server data.


## Maintainer(s)
Daniel Lang - langd052405@gmail.com

## License
All rights reserved by [Roswell Park Comprehensive Cancer Center](https://www.roswellpark.org) and the [Clinical Trial Development Division](https://www.ctdd.org) 