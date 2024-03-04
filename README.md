# IP Blocklist Service

Microservice that manages a list of IPs aimed at preventing abuse by
banning IPs that are known to be used for malicious purposes.

Assignment statement:
[gist](https://gist.github.com/champo/d369a4fc61a3acdaa39e335d973cfb10)

## Getting Started

Install python 3.10.4 and pyenv 3.10.4.
These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Prerequisites

- This project uses Redis service. Without it, the project won't work.
- python 3.10.4
- pyenv/conda or similar

Requirements for the software and other tools to build, test and push 
- [Example 1](https://www.example.com)
- [Example 2](https://www.example.com)

### Installing

- redis

#### Production build

    make install

### Usage

    curl localhost:8000/api/ips/<ipv4>


## Running the tests

	pyenv exec poetry run pytest tests/

Reminder: An active Redis is needed for this to work

### Sample Tests

Explain what these tests test and why

    Give an example


## Deployment

    make run

Add additional notes to deploy this on a live system

## Dependencies

  - [Redis](https://redis.io/) - Memory management
  - [Poetry](https://python-poetry.org/) - Dependency management
  - [Flask](https://flask.palletsprojects.com/) - Web application framework
  - [Docker](https://www.docker.com/) - Container platform
  - [Swagger](https://swagger.io/) - Interactive documentation
  - [Gunicorn](https://gunicorn.org/) - HTTP web server
  - [Pytest](https://pytest.org/) - Testing framework
  

## Technical decisions
Inside the repository several ip lists can be found.
One contains the list of all blocklisted ips alongside
their number of blocklisted appearances named 'ipsum.txt',
and 8 other files inside the 'levels' directory named 'n.txt', 
where n is a number in the range 1-8, each containing 
the list of blocklisted ips with n or more occurences. 
In particular the file '1.txt' contains all blocklisted ips 
with 1 or more occurences, which is what we need. 
This file does not contain the number of occurences for each ip, 
which makes it lighter than the main file containing all blocklisted ips.

### Why Redis
In a high availability environment we need 
consistency in the data between separate instances.
Redis replaces the internal memory cache to avoid
these inconsistencies.
Redis also provides a low latency option for
storing data.


### flask (vs FastAPI)
FastAPI is asynchronous which makes it more complex to
deploy and implement.
Flask is the most widely used web service microframework

### Python injector (Not currently used)
Simplifies importing services and methods across files
which makes them easier to test
and provides inversion of control

## TODO
### JobManager is a monster, refactor
### (move download, save and d&s somewhere else)
### There are 2 dockerfiles, maybe refactor into only 1
### One dockerfile in /jobs and the other in the root dir
### So that we can rename the JobManagerDockerfile to just 'Dockerfile'
