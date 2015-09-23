\newpage 

# Introduction

Hermes is a Content Management System (CMS) utilising Amazon Web Services (AWS). It allows for the ability to create Pages, Files and Upload entire static websites which can be maintained with the CMS. It contains its own Analytics and can scale based on the load of the system.

## Installation

The system is installed using automated scripts. A first installation of the system will contain no documents and only 2 users which should be removed for production use. To install the system you will need an Amazon Web Services (AWS) Account. 

There are several steps to install the system from scratch however there are some requirements to install first.

### Requirements
1. Python 2.7
1. CentOS 7 - It is recommended to use the Amazon base image ami-f7740dcd
1. Packer - [http://packer.io/](http://packer.io/) 
1. Ansible - [http://www.ansible.com/home](http://www.ansible.com/home)
1. Git
1. AWS Account - Assumption that relevant keys have been created

In your CentOS machine with the checked out source code you can run the following scripts to launch a system. All shell commands assume you are in the root directory of the git repository.

#### Build RPMs

```./ci/build_rpms.sh -v 201509042058```

#### Build YUM Repo

```./ci/build_yumrepo.sh -v 201509042058```

Please read the Developer Documentation on how to set up a S3 YUM Repository

#### Bake AMI

```./ci/bake_amis.sh -v 201509042058```

#### Create Cloud

You will need to install the following packages

```sudo python hermes_aws/setup.py install```

```sudo python hermes_cloud/setup.py install```

You will need to ensure the manifest file is created. See the baking/ansible/roles/hermes_cloud/templates/main.yml

```
create_cloud -d [domain] -n [name] -m [manifest] -k [key] --region [region] --min [min] 
    --max [max]
```

    Domain: The domain you wish to namespace your stacks too. This is recommended as S3 Buckets must 
    be unique within all of AWS.

    Name: The name of the cloud. All stacks created are prefixed with this name

    Manifest: The AMI Manifest file to read to create the cloud

    Key: The AWS Key Pair used to assign to each instance for SSH login

    Region: The region to install the stacks. By default this is ap-southeast-2 (Sydney)

    Min: The minimum number of instances to have in the ASG.

    Max: The maximum number of instances to have in the ASG.

There is more explanation on the installation in the Developer Documentation.

## Access and Logging details

The Hermes CMS is available at [http://hermescms.paulmcilwaine.com/](http://hermescms.paulmcilwaine.com/). There are 2 accounts which can be used to login in.

### Login page

You can at the page [http://hermescms.paulmcilwaine.com/login](http://hermescms.paulmcilwaine.com/login), and access the admin page is accessible at [http://hermescms.paulmcilwaine.com/admin/](http://hermescms.paulmcilwaine.com/admin/)

### Administrator Account

| Field      | Value                       |
|------------|-----------------------------|
| email:     | test@example.org            |
| password:  | password                    |

### Limited Access Account

| Field      | Value                      |
|------------|----------------------------|
| email:     | testing@example.org        |
| password:  | password                   |
