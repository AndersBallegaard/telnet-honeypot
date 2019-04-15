# Telnet honeypot 
A telnet honeypot running in docker.

## Getting started
### prerequisite
Make sure your system have Docker Docker-compose or Docker swarm, Git(optional) installed

### Install
```bash
# Download telnet-honeypot
git clone https://github.com/AndersBallegaard/telnet-honeypot.git

# Go to directory
cd telnet-honeypot

# Deployment option 1 (docker-compose)
docker-compose up -d

# Deployment option 2 (docker swarm)
# Note for this option you will have to build the image youself, change the compose file
docker stack deploy --compose-file docker-compose.yml TELNET-HONEYPOT 
``` 

## TODO
* Read the RFC for telnet (RFC854)
* Follow the RFC
* Improve compatibility with swarm and k8s
* Create a dashboard for the information