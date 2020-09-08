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
cd /var/configs
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
9. To tear down just run `exit` inside of the shell session. And you can ctrl+c to stop the container from running.


