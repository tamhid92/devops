FROM ubuntu:24.04

# Make the version configurable
# https://github.com/hashicorp/terraform/releases
ARG TERRAFORM_VERSION=1.10.4

LABEL maintainer="tamhidchowdhury@gmail.com" \
    org.label-schema.description="Jenkins Agent" \
    org.label-schema.url="https://github.com/tamhid92" 

# Install packages available through apt
RUN apt-get update && apt-get install -y \
  bash-completion \
  curl \
  git \
  unzip \
  python3 \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Terraform as root user
RUN curl -fsSL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -o /tmp/terraform.zip \
  && unzip /tmp/terraform.zip -d /tmp \
  && mv /tmp/terraform /usr/local/bin/ \
  && rm -rf /tmp/* \
  && terraform version

# Install auto-completions for non-root user
RUN terraform -install-autocomplete

ENV VAULT_ADDR=https://vault.tchowdhury.org
ENV ANSIBLE_HOST_KEY_CHECKING=false
ENV ANSIBLE_FORCE_COLOR=true

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
  apt-get install -y gnupg2 python3-pip sshpass git openssh-client curl software-properties-common && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get clean

RUN python3 -m pip config set global.break-system-packages true

RUN python3 -m pip install ansible && \
  rm -rf /root/.cache/pip


# TODO: INSTALL HVAC, VIM, RSYNC