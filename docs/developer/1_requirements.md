\newpage

# Requirements

Below are the requirements for the system.

1. Python 2.7+
1. Amazon Web Services Account
1. CentOS Linux
1. Ansible
1. Packer
1. Boto
1. NPM
1. AWS Cli
1. Git

## Recommended Requirements

Below are some optional but recommended requirements.

1. Jenkins
1. Virtualenv

\newpage

# Installation of Requirements

## Python 2.7

Development requires Python 2.7.x to be installed most Unix like systems have Python installed or can be installed via the package management provided. If you wish to do development to build RPM artefacts you'll need a system that can install RPMBuild. It is recommended that you use CentOS. You will also require PIP which is a simple Python package management program.

## AWS Account
You can [create an Amazon Web Services](https://aws.amazon.com/) (AWS) Account please follow the instructions provided. 

### Users

TODO Ensure this is filled out.
You will need to create an (Identity and Access Management) IAM User so you are not creating resources as the Root account. Ensure that this user is part of the Administrative group for ease of use.

You should also create a user for Jenkins if you want to do Continuous Integration.

### Roles

You can apply roles to EC2 Instances so they have access 

#### Create Cloud

## CentOS

CentOS is the Linux distribution used to install all the packages on. It is the recommended distribution to build RPMs from. You can use the hermes_linux as the base AMI (Amazon Image)

## Ansible

Ansible is used as the provisioner of the system. It installs all the packages and configuration on the system. You can use PIP to install Ansible.

```
pip install ansible
```

## Packer
You can download packer from [https://www.packer.io](https://www.packer.io) 

## Boto
Hermes CMS is built on top of the Amazon Web Services (AWS) platform and built with Python. Boto is a python package which interfaces with the AWS API and makes interacting with AWS easy. Boto can be easily installed using PIP.

```
pip install boto
```

## NPM

NPM (Node Package Management) is required to run tests as well as build the UI package. It is recommended to this [guide on install NPM]() on to your system.

## AWS Cli
Amazon provides a command line tool which sits on top of AWS API for easy use. It is a python program sitting on top of botocore. As its a python it can be install via PIP.

```
pip install awscli
```

You will need to create a profile so you do not continuously need set environment variables. Its recommended to [follow this guide](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) on how to do it.

## Git

All development on the main Hermes CMS application is done in Git on Github. The Github repository can be found here [github.com/pmcilwaine/hermes](https://github.com/pmcilwaine/hermes)

## Jenkins

Please see [deployment](deployment.html) on how to setup Jenkins for running Continuous Integration on the system.

## Virtualenv

Virtualenv is a Python virtual environment to install packages so there are no version conflicts with the main python installation. This is easy to install using PIP.

```
pip install virtualenv
```

We should create a virtualenv folder which can be done like below:

```
$ virtualenv -p [/path/to/python.27] [DIRECTORY]
```

You can then ensure you are using this environment by doing the below:

```
$ source [DIRECTORY]/bin/activate
```

# Installation

Please see the above [Installation of Requirements](Installation of Requirements) before proceeding.


