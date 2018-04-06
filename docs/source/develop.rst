##############
For Developers
##############

##############################
Install and Environment Set up
##############################

* Python 2.7.6, 2.7.11, or 2.7.13 is required to run the code, with the requirements installed from requirements.txt.
  *Environments for Python 3 will soon be available*.
* We highly recommend running SimPrily with the provided Docker, Singularity, or virtual environment.

Container
*********

Docker
------
A Docker Image built with Python 2.7.13, the requirements, and the SimPrily code can be found on Docker Hub
https://hub.docker.com/r/agladstein/simprily/

cd to the directory you want to work in and then pull the Docker image.
To pull the Docker container:
::

 docker pull agladstein/simprily


How to run SimPrily with the Docker container
::

    docker run -t -i --mount type=bind,src="$(pwd)",dst=/app agladstein/simprily python /app/simprily.py [-h] -p PARAM -m MODEL -i ID -o OUT [-g MAP] [-a ARRAY] [-v] [--profile]




Singularity
-----------
The Docker image can be pulled as a Singularity container.

To pull the Singularity container:
::

    singularity pull docker://agladstein/simprily


How to run SimPrily with the Singularity container
::

    singularity exec simprily.simg python /app/simprily.py [-h] -p PARAM -m MODEL -i ID -o OUT [-g MAP] [-a ARRAY] [-v] [--profile]


Open Science Grid Connect
=========================

A prebuilt Singularity Image from the Docker Image is used for the Open Science Grid workflow.
The Singularity Image on OSG Connect is available from ``/cvmfs/singularity.opensciencegrid.org/agladstein/simprily\:latest``.

Virtual environment
*******************

Linux OS
--------
cd to the directory you want to work in and then download the repository,
::

    git clone https://github.com/agladstein/SimPrily.git

Install the virtual environment and install the requirements.
::

    ./setup/setup_env_2.7.sh

If you get an error during ``pip-sync`` try rebooting the system.

How to run SimPrily with a virtual environment:
``simprily.py`` takes 4 required arguments and 2 optional arguments, and help, verbose, and profile options.

::

    python simprily.py [-h] -p PARAM -m MODEL -i ID -o OUT [-g MAP] [-a ARRAY] [-v] [--profile]


For quick help:
::

    python simprily.py --help

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

How to run SimPrily with a virtual environment in Vagrant:
``simprily.py`` takes 4 required arguments and 2 optional arguments, and help, verbose, and profile options.

::

    python simprily.py [-h] -p PARAM -m MODEL -i ID -o OUT [-g MAP] [-a ARRAY] [-v] [--profile]


For quick help:
::

    python simprily.py --help

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


How to run SimPrily locally
``simprily.py`` takes 4 required arguments and 2 optional arguments, and help, verbose, and profile options.

::

    python simprily.py [-h] -p PARAM -m MODEL -i ID -o OUT [-g MAP] [-a ARRAY] [-v] [--profile]


For quick help:
::

    python simprily.py --help


************************************
Additional Information on Containers
************************************

Docker
------
Notes on installing Docker, creating a Docker image, and running a Docker container.
*The following instructions for Docker require sudo privaliges.
Check the Docker documentation for what to do if you do not have sudo.*

**Installing Docker**
^^^^^^^^^^^^^^^^^^^^^

Check that Docker is installed:
::

    sudo docker run hello-world

Quick and easy install script provided by Docker:
::

    curl -sSL https://get.docker.com/ | sh

OR

If not on Linux, you can use Vagrant.
::

    vagrant up
    vagrant ssh

Then, continue with Linux steps.

See https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce

For Mac or Windows see Docker documentation.

**Dockerize**
^^^^^^^^^^^^^

1. Create Dockerfile
2. Build Docker image
3. Push Docker image to Docker Hub

**1. Create Dockerfile**
In the directory with the necessary code and requirements.txt

`Dockerfile <https://github.com/agladstein/SimPrily/blob/master/Dockerfile>`_
::

    # Use an official Python runtime as a parent image
    FROM python:2.7

    # Set the working directory to /app
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    ADD . /app

    # Install any needed packages specified in requirements.txt
    RUN pip install -r requirements.txt

    # Create directory for OSG
    RUN mkdir -p /cvmfs

    # Make executable
    RUN chmod +x /app/simprily.py

    # Make port 80 available to the world outside this container
    EXPOSE 80

    # Define entry point
    #ENTRYPOINT ["python", "/app/simprily.py"]

See https://docs.docker.com/engine/reference/builder/

**2. Build Docker imiage**
::

    sudo docker build -t agladstein/simprily .

**3. Push Docker image to Docker Hub**

Must first login to Docker Hub
::

    sudo docker login

::

    sudo docker push agladstein/simprily


**Run program with Docker container**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Pull image:
::

    sudo docker pull agladstein/simprily

Run program:
::

    docker run -t -i --mount type=bind,src=/home/agladstein/docker_test/SimPrily,dst=/app agladstein/simprily_autobuild:version1 python /app/simprily.py -p examples/eg1/param_file_eg1.txt -m examples/eg1/model_file_eg1.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -a array_template/ill_650_test.bed -i 1 -o output_dir -v

*try running with port ``-p``*

or Run Docker container interactively to poke around
::

    docker run --rm -it --entrypoint=/bin/bash agladstein/simprily_autobuild:version1

**Cheat sheet**
^^^^^^^^^^^^^^^
Some useful commands
::

    docker build -t friendlyname .  # Create image using this directory's Dockerfile
    docker run -p 4000:80 friendlyname  # Run "friendlyname" mapping port 4000 to 80
    docker run -d -p 4000:80 friendlyname         # Same thing, but in detached mode
    docker container ls                                # List all running containers
    docker container ls -a             # List all containers, even those not running
    docker container stop <hash>           # Gracefully stop the specified container
    docker container kill <hash>         # Force shutdown of the specified container
    docker container rm <hash>        # Remove specified container from this machine
    docker container rm $(docker container ls -a -q)         # Remove all containers
    docker image ls -a                             # List all images on this machine
    docker image rm <image id>            # Remove specified image from this machine
    docker image rm $(docker image ls -a -q)   # Remove all images from this machine
    docker rmi $(docker images -q)  # Remove all containers from this machine
    docker login             # Log in this CLI session using your Docker credentials
    docker tag <image> username/repository:tag  # Tag <image> for upload to registry
    docker push username/repository:tag            # Upload tagged image to registry
    docker run username/repository:tag                   # Run image from a registry


**Resources**
^^^^^^^^^^^^^
https://docs.docker.com/get-started/
https://github.com/wsargent/docker-cheat-sheet
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce
https://docs.docker.com/engine/reference/builder/
https://docs.docker.com/engine/reference/commandline/run/#add-bind-mounts-or-volumes-using-the-mount-flag
http://codeblog.dotsandbrackets.com/persistent-data-docker-volumes/


Singularity
-----------
*These are preliminary notes, not specific to a SimPrily Singularity container.*

**Installing Singularity**
^^^^^^^^^^^^^^^^^^^^^^^^^^

To install Singularity:
::

    git clone https://github.com/singularityware/singularity.git
    cd singularity
    sudo apt-get install libtool
    sudo apt-get install autotools-dev
    sudo apt-get install automake
    ./autogen.sh
    ./configure --prefix=/usr/local
    make
    sudo make install

**Create empty image**
^^^^^^^^^^^^^^^^^^^^^^

To create an empty Singularity image:
::

    create --size 2048 simprily-little.img

**Make or pull a container**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**1. Make container by dumping docker layers into empty image:**
::

    import simprily-little.img docker://agladstein/simprily-little

or

**2. Pull container**
::

    singularity pull docker://centos:latest

or

**3. Bootstrap**

Create Singularity specification file.

For example:
::

    Bootstrap: docker
    From: ubuntu:latest

    %runscript

        echo "I can put here whatever I want to happen when the user runs my container!"
        exec echo "Hello Monsoir Meatball" "$@" #The $@ is where arguments go

    %post

       echo "Here we are installing software and other dependencies for the container!"
       apt-get update
       apt-get install -y git

Then build image from Singularity file:
::

    sudo singularity bootstrap analysis.img Singularity

**Run container**
^^^^^^^^^^^^^^^^^

**1. from Singularity Hub**
::

    singularity run shub://vsoch/hello-world

or

**2. from local container with input arguement**
::

    singularity run analysis.img Ariella

**Shell into a container**
^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    singularity shell centos7.img

**Resources**
^^^^^^^^^^^^^
- http://singularity.lbl.gov/quickstart
- http://singularity.lbl.gov/singularity-tutorial
- https://singularity-hub.org/faq

*******
Testing
*******

The shell script ``autoTesting.sh`` is included for quick automated testing of included examples.

It is run as:
::

    ./autoTesting.sh PYTHON [EXAMPLE_INT]

| Where,
| ``PYTHON`` is the python to use
| ``EXAMPLE_INT`` is the specific example number to test (optional). If it is not specified, it will test all of the examples.

**********************
Creating Documentation
**********************

- Install Sphinx:
::

    pip install Sphinx

- To edit the Read The Docs, edit the Sphinx .rst files in ``SimPrily/docs``.
- Build the html from restructured text:
::

    ~/simprily_env/bin/sphinx-build -b html source build


Resources
---------
- http://www.sphinx-doc.org/en/stable/tutorial.html
- https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst
- https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html#headings
- http://rest-sphinx-memo.readthedocs.io/en/latest/ReST.html

***********
Other Notes
***********

- If you use import a new Python package make sure you add it to the requirements.txt file then create the requirements.in. This will insure that the package installed in the virtual environment and Docker image.

::

    pip-compile --output-file requirements.txt requirements.in

