# devops

This is just a collection of random scripts/projects that I'm working on.

Infrastructure:

Everything is developed in my home-lab environment with the following hardware:
 - Raspberry PI
 - Desktop PC (Running Windows and WSL)

Raspberry PI:
    - Hosts the Jenkins server
        - This has 2 worker nodes set.
            - Desktop PC (Windows Environment)
            - Desktop PC (WSL - Set up as a seperate Linux node, so that I can run Ansible)
    - Hosts the HashiCorp Vault Server as a docker container
        - I set it up on my Raspberry PI, so that I can access it from any device on my network

Desktop PC:
    - This is set up to have two different environments. Windows and WSL for Linux jobs.
        - Set up a port forwarding rule to allow access to the WSL via SSH
    - The Windows environment hosts VMWare and VirtualBox that allows me to spin up VMs when needed for a job.
    - Necessary Utility programs installed such as PGAdmin to access DB

JENKINS CI/CD Pipeline:
    The Jenkinsfile runs as on a multinode setup to do the following:
        - Connects to the Windows Node:
            - Starts the VMWare Workstation Pro REST API.
            - Runs a python script to template the host file needed for Ansible (gets the VM IP address using the REST API and passwords from the vault)
        - Connects to WSL:
            - Runs Ansible Playbooks which connects to VMWare VMs.
                - Configures the VM. (Installs docker, MicroK8s, and copies over necessary files and certs from HasiCorp Vault)
                - Runs K8s deployment files, deploys Postgres, my resume as a react app and the ManUtd Flask application.

Ansible:
    - Created a custom role to install docker
    - Installs MicroK8s
    - Deploys a K8 pod for the manutd_flask app
    - Deploys resume-react app as a Docker container

ManUtd_Flask:
    - This is a flask application that pulls the fixture list for Manchester Uniter.
        - Downloads a calendar file with all the games.
        - Scrapes the file to get all the game information.
        - Stores all the data in a Postgres DB.
        - Flask sets up the API service, pulling data from the DB to display next game as well as all the remaining games.
        - Both of those are containerized in Docker.

resume_react:
    - This is the source folder that contains the dockerized react app that deploys my resume.

VBOX:
    - template-powershell.py This templates a Powershell script to deploy a VM in VirtualBox using the VBoxManage CLI tool.
lib:
    - Contains the library files required for Vault and VMWare apis.
templates:
    - Contains the template files to create the ansible host file as well as powershell script to deploy VirtualBox VMs.