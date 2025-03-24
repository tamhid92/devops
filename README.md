# DevOps Projects Repository

## Overview
This repository is a collection of various scripts and projects that I am currently working on. These projects are developed and tested in my home-lab environment, which consists of a mix of Raspberry Pi and desktop PC hardware. The infrastructure is designed to support a multi-environment DevOps workflow, incorporating CI/CD pipelines, automation, containerization, and infrastructure as code (IaC).

## Home Lab Infrastructure
### Hardware:
- **Raspberry Pi** (Hosts key services and automation tools)
- **Desktop PC** (Running both Windows and WSL for multi-environment support)

### Raspberry Pi:
- **Jenkins Server**
  - Configured with two worker nodes:
    - **Windows Node:** Desktop PC running Windows
    - **Linux Node:** Desktop PC running WSL (Windows Subsystem for Linux), enabling Ansible execution
- **HashiCorp Vault Server** (Running as a Docker container)
  - Set up to be accessible from any device within my network for centralized secrets management

### Desktop PC:
- Configured with both Windows and WSL environments to facilitate hybrid workflows
- **Port forwarding** is enabled to allow SSH access to WSL from external devices
- **Virtualization Support:**
  - Runs **VMWare Workstation Pro** and **VirtualBox** to create and manage virtual machines on demand
- **Essential DevOps utilities installed**, such as **PGAdmin** for PostgreSQL database management

## Jenkins CI/CD Pipeline
The Jenkins pipeline is set up to run in a multinode configuration and performs the following tasks:

1. **Windows Node:**
   - Starts the **VMWare Workstation Pro REST API**
   - Executes a Python script to generate an **Ansible host file**, which:
     - Retrieves the VM's IP address using the VMWare REST API
     - Fetches necessary passwords and credentials from **HashiCorp Vault**

2. **WSL Node:**
   - Runs Ansible playbooks to configure VMs on **VMWare**
     - Installs essential software (Docker, MicroK8s, and other dependencies)
     - Copies necessary configuration files and certificates from **HashiCorp Vault**
     - Deploys Kubernetes workloads, including:
       - **PostgreSQL database** (containerized)
       - **Resume React app** (containerized)
       - **ManUtd Flask application** (containerized)

## Ansible Automation
The Ansible playbooks automate infrastructure provisioning and application deployment with the following key features:
- **Custom Role for Docker Installation**
- **MicroK8s Deployment**
- **Kubernetes-based application deployment:**
  - Deploys a pod for the ManUtd Flask app
  - Deploys the resume React app as a Docker container
  - Deploys PostgreSQL as a Kubernetes pod

## ManUtd Flask Application
A Flask-based web application that provides information on **Manchester United fixtures**. The application:
- Downloads a **calendar file** containing match schedules
- Scrapes and processes the fixture data
- Stores parsed data in a **PostgreSQL database**
- Exposes an API to retrieve:
  - Upcoming matches
  - Complete fixture list
- Both the Flask app and PostgreSQL database are containerized using **Docker**

## Resume React Application
- A React-based web application that hosts my resume
- Packaged as a Docker container for easy deployment and scalability

## VirtualBox Automation
- `template-powershell.py`: A Python script that generates a **PowerShell script** to deploy a VM in **VirtualBox** using the `VBoxManage` CLI tool

## Linux From Scratch (LFS) Project
I have completed a project where I built a Linux distribution from scratch. One of the most tedious and repetitive parts of this process involves manually installing all the necessary packages. To streamline this, I automated the installation by:
- Extracting a list of all required packages
- Scraping the necessary commands from the LFS website
- Compiling them into a comprehensive Bash script to automate the installation process - **`LFS/scrapeLFS.py`**

## Directory Structure
- **`lib/`** - Contains utility libraries for interacting with **HashiCorp Vault** and **VMWare APIs**
- **`templates/`** - Stores template files for:
  - Generating **Ansible inventory files**
  - Creating **PowerShell scripts** for VirtualBox VM deployment

## Conclusion
This repository serves as an evolving collection of my DevOps projects, demonstrating my ability to build, automate, and manage infrastructure using industry-standard tools such as **Jenkins, Ansible, Kubernetes, Docker, and HashiCorp Vault**. My home lab environment allows me to experiment with real-world DevOps scenarios, bridging Windows and Linux ecosystems for a comprehensive infrastructure setup.

Feel free to explore and contribute!
