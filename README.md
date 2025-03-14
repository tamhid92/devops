# devops

This is just a collection of random scripts/projects that I'm working on.

LFS - Linux from Scratch
- I've been building Linux from scratch. Chapter 8 is about installing all the system packages manually which is tedious and repetative.
- I wrote a python script (LFS/scrapeLFS.py) that scrapes all the necessary commands from the LFS website and creates a bash script.
- The generated bash script can now be run as just one file to install all 78 packages.

Man United games
- I built a very simple flask app, which output the next Manchester United game as well as the remaining one.
- The docker compose file builds 3 containers. The first container is the postgres DB container.
- The first python script (python/populateDB.py) populates the postgres DB.
    - The script downloads a calendar file from the SkySports website and then scrapes the data from it and  stores them in the postgres database.
- The last container deploys the flask app.

The Jenkinsfile is a left-over file from an old project. Currently not used, I'll use it to deploy VMs to VMWare Workstation Pro using Terraform 
and then Ansible to provision and set up the VM.