##############
For Developers
##############

**********
Containers
**********

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

*************
Documentation
*************

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

