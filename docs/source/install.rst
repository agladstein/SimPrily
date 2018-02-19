##############################
Install and Environment Set up
##############################

* Python 2.7.6, 2.7.11, or 2.7.13 is required to run the code, with the requirements installed from requirements.txt.
  *Environments for Python 3 will soon be available*.
* We highly recommend running SimPrily with the provided Docker image or virtual environment.

Docker
******
A Docker Image built with Python 2.7.13, the requirements, and the SimPrily code can be found on Docker Hub
https://hub.docker.com/r/agladstein/simprily/

cd to the directory you want to work in and then pull the Docker image.
::

 docker pull agladstein/simprily

Singularity
***********
A Singularity Image, built from the Docker Image, is used for the Open Science Grid workflow.
The Singularity Image on OSG Connect is available from ``/cvmfs/singularity.opensciencegrid.org/agladstein/simprily\:latest``.
The Singularity Image is NOT currently available through Singularity Hub.
*A Singularity Image for use outside of OSG will soon be available*.


Virtual environment
*******************

Linux OS
-----------------------------
cd to the directory you want to work in and then download the repository,
::

    git clone https://github.com/agladstein/SimPrily.git

Install the virtual environment and install the requirements.
::

    ./setup/setup_env_2.7.sh

If you get an error during ``pip-sync`` try rebooting the system.

Virtual Machine for non-Linux
-----------------------------

If you are running on a non-Linux OS, we recommend using the virtual machine, Vagrant (can be used on Mac or PC). In order to run Vagrant, you will also need VirtualBox.

Download Vagrant from https://www.vagrantup.com/downloads.html

Download VirtualBox from https://www.virtualbox.org/

cd to the directory you want to work in and then download the repository,
::

 git clone https://github.com/agladstein/SimPrily.git

Start Vagrant, ssh into Vagrant, cd to SimPrily directory.
::

    vagrant up
    vagrant ssh
    cd /vagrant

Install the virtual environment and install the requirements.
::

    ./setup/setup_env_vbox_2.7.sh

Local installation
******************
*We do not recommend this method*

cd to the directory you want to work in and then download the repository,
::

 git clone https://github.com/agladstein/SimPrily.git

If the above options do not work, the correct version of Python can also be installed locally:
::

    cd mkdir python_prebuild
    wget https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
    mkdir python
    tar -zxvf Python-2.7.6.tgz
    cd Python-2.7.6
    ./configure --prefix=$(pwd)/../python
    make
    make install
    cd ..
    export PATH=$(pwd)/python/bin:$PATH
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
    pip install -r requirements.txt
    python simprily.py --help

