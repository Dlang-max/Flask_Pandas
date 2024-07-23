# 1.1 Software Title
Data Visualization of CTDD IT Server Data Flask App

# 1.1 Purpose
The purpose of the Data Visualization of CTDD IT Server Data Flask App is to display metadata associated with CTDD IT data transfers, making monitoring of these transfers easier.  

## Technical Overview

### Technical Specifications
+ Programming Languages: Python for backend, HTML, CSS, and JavaScript for frontend.
+ Web Servers: Gunicorn to run Flask app, Nginx to handle requests and serve static CSS files.
+ Operating System: Ubuntu 22.04 

### Installation Instructions
1. Install Docker 
+ To run this Flask app locally install [Docker Desktop](https://docs.docker.com/get-docker/).
+ To run this Flask app on a remote server install [Docker Engine](https://docs.docker.com/engine/install/)

2. Clone the git repository
```bash
git clone __repo_url__
```
3. Move to the Data Visualization Flask App Directory
```bash
cd "Data Visualization Flask App Directory"/
```

4. Build and Spin Up Docker containers
```bash
docker compose -f compose.nginx.yaml up -d --build
```

5. Navigate to [http://localhost:1337/](http://localhost:1337/)  


## Maintainer(s)
Daniel Lang - langd052405@gmail.com

## License
All rights reserved by [Roswell Park Comprehensive Cancer Center](https://www.roswellpark.org) and the [Clinical Trial Development Division](https://www.ctdd.org) 