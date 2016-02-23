## Overview

This vagrant script automatically spins up 2 vms named **k2k-sp** and **k2k-idp** on an OpenStack cloud and set up devstack kilo

This recipe installs devstack kilo (master branch) with minimal configuration

## How to use?

### 1. Set up vagrant

1) Install vagrant

Go to [vagrant official site](http://www.vagrantup.com/downloads)

2) Install vagrant-hostmanager plugin to better manage /etc/hosts

`vagrant plugin install vagrant-hostmanager`

3) Install vagrant-openstack-provider

`vagrant plugin install vagrant-openstack-provider`

### 2. Configure the parameters in vagrantconfig

Please change the following parameters in `Vagrantfile` according to your OpenStack environment

**Please see the comments in vagrantconfig.yaml which explains how to set the parameters**

### 3. source your openrc file

You can download your openrc file on horizon under Access and Security -> API access -> Download OpenStack RC File

once you download your openrc file, simple source it by running:

`source name_of_your_rcfile`

on the terminal

### 4. Spin up vms, deploy devstack, and set up K2K

simply run

```
vagrant up --no-provision
vagrant provision
```


