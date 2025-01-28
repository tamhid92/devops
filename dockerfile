FROM ubuntu

#install and source ansible
RUN apt-get update && apt-get install -y \
    git \
    python-yaml \
    python-jinja2 \
    python-pycurl

RUN git clone https://github.com/ansible/ansible.git
WORKDIR ansible/hacking
RUN chmod +x env-setup; sync \
    && ./env-setup
