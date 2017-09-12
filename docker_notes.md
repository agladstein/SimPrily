Notes on installing Docker, creating a Docker image, and running a Docker container.  

## Installing Docker

Check that Docker is installed:
```bash
sudo docker run hello-world
```

Quick and easy install script provided by Docker: 
```bash
curl -sSL https://get.docker.com/ | sh
```
OR  

Install by hand using steps provided by Docker:
```
sudo apt-get update
sudo apt-get install \
    linux-image-extra-$(uname -r) \
    linux-image-extra-virtual

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
    
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
   
sudo apt-get update

sudo apt-get install docker-ce
sudo docker run hello-world
```


If not on Linux, can use Vagrant.
```bash
vagrant up
vagrant ssh
```
Then, continue with Linux steps.

See https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce  


For Mac or Windows see Docker documentation.

## Dockerize

1. Create Dockerfile  
2. Build Docker image  
3. Push Docker image to Docker Hub

#### Create Dockerfile
In the directory with the necessary code and requirements.txt  

Dockerfile
```text
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

# Make port 80 available to the world outside this container
EXPOSE 80

# Run simprily.py when the container launches
CMD ["python", "simprily.py"]
```

See https://docs.docker.com/engine/reference/builder/
#### Build Docker image
```bash
sudo docker build -t agladstein/simprily .
```

#### Push Docker image to Docker Hub

Must first login to Docker Hub
```bash
sudo docker login
```
```bash
sudo docker push agladstein/simprily
```

## Run program with Docker Container

Pull image:
```bash
sudo docker pull agladstein/simprily
```

Run program:
```bash
sudo docker run -t -i --mount type=bind,src=/home/agladstein/docker_test/SimPrily,dst=/app agladstein/simprily-little python /app/simprily.py examples/eg1/param_file_eg1.txt examples/eg1/model_file_eg1.csv macs 1 array_template/ill_650_test.bed 1 False /app/out_dir
```

## Cheat sheet
```
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
docker login             # Log in this CLI session using your Docker credentials
docker tag <image> username/repository:tag  # Tag <image> for upload to registry
docker push username/repository:tag            # Upload tagged image to registry
docker run username/repository:tag                   # Run image from a registry
```

## Resources
https://docs.docker.com/get-started/  
https://github.com/wsargent/docker-cheat-sheet  

https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce    
https://docs.docker.com/engine/reference/builder/  
https://docs.docker.com/engine/reference/commandline/run/#add-bind-mounts-or-volumes-using-the-mount-flag  
http://codeblog.dotsandbrackets.com/persistent-data-docker-volumes/