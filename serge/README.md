## Running Serge w/ Docker
Serge is currently setup to run in a Debian:stretch Docker container.
Follow the steps below to get this up and running

### Pre-requisites
- Docker Desktop (https://www.docker.com/get-started)

1. Open/Run Docker Desktop
2. Build the docker image locally
```
cd ~/tms/serge
docker build --no-cache -t serge -f Dockerfile .
```
3. Verify that the image was built successfully. The following command will list all the images.
```
docker images
```
You should notice something like this:
```
REPOSITORY                                                                    TAG                       IMAGE ID            CREATED             SIZE
serge                                                                         latest                    643a21fee17e        20 minutes ago      349MB
```
4. Now you're ready to spin up the container. For this you will need two terminal windows/tabs. You can do this in one if you prefer.
```
docker-compose up

or if you don't want to open a new terminal tab

docker-compose up -d 
```
5. You will notice something that looks like the below:
```
Starting serge_serge_1 ... done
Attaching to serge_serge_1

```
6. Open a new Terminal window and run the following command to open a Shell session inside your container.
```
docker-compose exec serge bash
```
7. Navigate into the Serge configs directory
```
cd /var/serge/data/configs
```
8. At this point you can change the `sampleconfigs.serge` file and run it as needed.
All the commands below will work except for `push-ts` and `pull-ts` without any additional work.
Feel free to create new configuration files in the `/tms/serge/data/configs` directory and test them inside the container by running the commands below. You can change/edit these files in your local filesystem since the directory is mounted in the container.
```
# Command to initialize and setup the sqlite3 database and pull the repository for the first time.
serge pull sampleconfigs.serge --initialize

# Command to localize and generate the .po files.
serge localize sampleconfigs.serge

# Command to pull from translation service
serge pull-ts sampleconfigs.serge

# Command to push back to translation service
serge push-ts sampleconfigs.serge

# Command to push back to the original source repository
serge push sampleconfigs.serge
```


Intended Developer flow to develop using Serge
```
- Get the Docker setup running
- Configure your local machine (not Docker) python code to look for .po files in `/tms/serge/data/ts` directory.
- Update/Create a new config file in your local machine in `/tms/serge/data/configs` directory. This file will immediately show up inside Docker, but you can edit it locally without having to mess with Docker.
- Now you follow the instructions to run `serge pull /var/serge/data/configs/yourconfig.serge` inside the Docker container.
- You should see that your local machine's `/tms/serge/data/vcs` folder has some new files added to it (assuming things inside the yourconfig.serge file is correct).
- Again within Docker you run `serge localize /var/serge/data/configs/yourconfig.serge` which will populate your local machine's `/tms/serge/data/ts` directory with the appropriate .po files.
- At this point you are back in your local machine where you run your python code or any code really since the files are accessible in your machine. Your python code in your machine will be able to see all the .po files inside /tms/serge/data/ts directory.
- Your python code will be responsible to update the `/tms/serge/data/ts` directory in your local machine with the updated .po files which will immediately be reflected inside the docker container as well.
- At this point you can go back into Docker and run `serege localize /var/serge/data/configs/yourconfig.serge` which _should_ be able to recognize that the .po file has translations and update the local machine's `tms/serge/data/vcs/` directory with new translated json files.
The above setup should not require you to change anything about docker or your local setup (except for pointing your local setup to look at .po files in `/tms/serge/data/ts` directory). You would just leverage it to run `serge localize` or `serge sync` etc. And your python code will be running as it was before in your local system directly.
Eventually (hopefully this weekend) we will bring the Python code and its dependencies into Docker as well either within the same container or a separate container that runs a stand-alone Python app that shares a filesystem with the Serge Docker Container, but at the moment its not setup to do that which is why we have to run code partially on the local system and partially within the Serge Docker container.
```

9. To tear down just run `exit` inside of the shell session. And you can ctrl+c to stop the container from running.

