# IP Blocklist Service

## Description

Microservice that manages a list of IPs aimed at preventing abuse by
banning IPs that are known to be used for malicious purposes.

Assignment statement:
[gist](https://gist.github.com/champo/d369a4fc61a3acdaa39e335d973cfb10)

This project took approximately 16 hours to complete.

## Getting Started

### Prerequisites

- Redis
- Python 3.10.4
- Pyenv
- A [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

### Installing

- [Redis installation instructions](https://redis.io/docs/install/install-redis/)

#### Production build

    make install

## Deployment

    make run

### Usage

    curl localhost:8000/api/ips/<ipv4>

#### Example

    curl localhost:8000/api/ips/0.0.0.0    
    {"is_in_blocklist":true}


## Running the tests

    pyenv exec poetry run pytest tests/

Reminder: An active Redis is needed for this to work

### Sample Test

The following test's goal is to check that if an IP was added
to the redis service, then it should return `true`

    def test_blocklisted_ip(client):
        redis_test_instance.sadd(BLOCKLIST_NAME, '103.251.167.20')
        response = client.get("/api/ips/103.251.167.20")
        assert response.data == b'{"is_in_blocklist":true}\n'
        assert response.status_code == 200

### Interactive documentation

    curl localhost:8000/api/docs/

## Dependencies

  - [Redis](https://redis.io/) - Memory management
  - [Poetry](https://python-poetry.org/) - Dependency management
  - [Flask](https://flask.palletsprojects.com/) - Web application framework
  - [Docker](https://www.docker.com/) - Container platform
  - [Swagger](https://swagger.io/) - Interactive documentation
  - [Gunicorn](https://gunicorn.org/) - HTTP web server
  - [Pytest](https://pytest.org/) - Testing framework

## Functional requirements

The service has a single endpoint (`/api/ips/`) that takes 
an IP v4 encoded as a string (e.g. "127.0.0.1"), and return 
"true" if the IP is part of the blacklist, and "false" otherwise.

This is an example of how calling the microservice looks like

`curl http://blocklist/api/ips/127.0.0.1
{"is_in_blocklist":false}`

### Data source

The microservice does a periodical sync with [this public list](https://github.com/stamparm/ipsum).
It is currently configured to run every one hour.

#### Future improvements on list sync

Depending on how much the public list is trusted to update exactly
every 24 hours, many improvements can be made:
- After a successful update wait until 24 hours have passed 
since the time of the last commit
- In case the last commit was delayed, check the public list 
at the most frequent update hour of the day instead of waiting 24 hours
- If the public list is down when trying to update, 
an escalating backoff factor can be implemented, 
so that it progressively increases the delay between retries 
until the request is successful

## Non functional requirements

### High availability

To avoid downtime while updating the blocklist,
the blocklist is updated through a parallel worker
that updates the Redis service.

### Operation under heavy load

A load balancer can be added alongside cloud infrastructure
that allows the service to run in several copies that consume
the same Redis service to ensure consistency. 
This was not implemented due to time constraints.

### Low latency

In order to reduce the time taken by the service to check if
an ip is in the blocklist, a Redis service was implemented which
replaces the internal memory with a faster one.

### Efficient usage of resources

To avoid downloading entire lists and comparing them 
to the previously stored ones, the commit hashes are compared instead.


## Technical decisions

### Data source

Inside the repository several ip lists can be found.
One contains the list of all blocklisted ips alongside
their number of blocklisted appearances named 'ipsum.txt',
and 8 other files inside the 'levels' directory named 'n.txt', 
where n is a number in the range 1-8, each containing 
the list of blocklisted ips with n or more occurrences. 
In particular the file '1.txt' contains all blocklisted ips 
with 1 or more occurrences, which is what we need. 
This file does not contain the number of occurrences for each ip, 
which makes it lighter than the main file containing all blocklisted ips.

### Blocklist update frequency

The Job Manager checks for list updates every one hour. This means that in the worst case scenario 
that the list is updated one minute after the Job Manager checked, the service would be desynced for 59 minutes.
If the blocklist is believed to update exactly at the same time each day without fail and never at another time,
the job can be scheduled to run every 24 hours one second after the time the list updates. In this case, if the
source list update was delayed for a minute, then the service would be desynced for almost 24 hours.
A possible solution to this scenario is to check if there was a commit at the expected time, and if there wasn't,
check for updates in a few minutes, or implement an escalating backoff factor.
However, these solutions don't contemplate a possible update at an irregular time, which is why the hourly check
was chosen. Reducing the wait times between checks will eventually lead to Git blocking the requests. 
A further improvement is tu find the minimum time allowed by Git between checks.

#### Git Authentication token requirement

Checking commit hashes requires a Git Authentication token.
If the target user does not have a Git token the slower approach 
which avoids checking commit hashes should be followed instead.

### flask (vs FastAPI)
FastAPI is asynchronous which makes it more complex to
deploy and implement.
Flask is the most widely used web service microframework
