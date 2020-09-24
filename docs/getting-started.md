# Running Serge w/ Docker
Serge is currently setup to run in a Docker container that is also setup to run any Python 3.8.5 applications. Its based on the Debian:buster image.
Follow the steps below to get this up and running

# Running Translation Service w/ Docker
The Docker image is setup to run the Translation service Python application. The current image is setup to use Python 3.8.5 and will install any dependencies specified in `/translation_service/requirements.txt` during the build process.
Follow the same steps as outlined below.

# Running Ingestion Service w/ Docker
The Docker image is setup to run the Ingestion service Python application. The current image is setup to use Python 3.8.5 and will install any dependencies specified in `/ingestion/requirements.txt` during the build process.
Follow the same steps as outlined below.


## Docker Setup Overview
At a high-level you need to get familiarized with two docker functions-
1. `docker build`
This "builds" your Docker image by downloading and installing all the packages required as defined by either your Python code or the code defined in Serge.

You will not be running this very often. Typically you'll be building a new image only if something changed with your application infrastructure. Either a new service was added or a new python dependency was added in `requirements.txt`, etc. Or if there were improvements or changes made to the `Dockerfile`.

2. `docker-compose`
This command is responsible to "spin-up" the container that is defined in `docker-compose.yml`. This file essentially tells Docker to run an instance of the image that was previously built. At this step, we will specify the environment-specific configurations as well as "mount" volumes that are shared by both your local machine as well as the docker container. This is useful because you may want to change some code in your local machine and quickly test those changes inside the docker container to see if it had the intended effect.


### Pre-requisites
- Docker Desktop (https://www.docker.com/get-started)
- Copy over `.env.template` into `.env` with any other environment variables the application needs access to.
- Setup Secrets by looking at the following templates and re-creating them:
	- `git_key.template` -> `git_key`
	- `IngestionGoogleKey.json.template` -> `IngestionGoogleKey.json`
	- `TranslationGoogleKey.json.template` -> `TranslationGoogleKey.json`
Your google keys may be the same as the existing ones, but your git_key will certainly need to be created.

## Build Process
1. Open/Run Docker Desktop
2. Build the docker image locally
```
cd ~/tms
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

## Container Up/Down
1. Now that the image exists and is built-- you're ready to spin up the container. For this you will need two terminal windows/tabs. You can do this in one if you prefer.
```
docker-compose up

or if you don't want to open a new terminal tab

docker-compose up -d 
```
2. You will notice something that looks like the below:
```
Starting serge_serge_1 ... done
Attaching to serge_serge_1

```
3. Open a new Terminal window and run the following command to open a Shell session inside your container.
```
docker-compose exec serge bash
```
4. Run the `ls` command and verify that you are seeing roughly the following directories. You want to make sure that the application directories defined in the top-level of the project exist. 
```
bin   common  etc   ingestion  lib64  mnt  proc  run   serge-1.4	 srv  testing  translation_service  var
boot  dev     home  lib        media  opt  root  sbin  shared_directory  sys  tmp      usr
```

## App-specific development
1. Navigate into the directory of the application you would like to develop.
```
# For serge
cd /var/tms/serge/configs

# For translation servie
cd /var/tms/translation_service

# For ingestion service
cd /var/tms/ingestion
```
2. (A) FOR SERGE ONLY: At this point you can change the `sampleconfigs.serge` file and run it as needed.
All the commands below will work except for `push-ts` and `pull-ts` without any additional work.
Feel free to create new configuration files in the `/var/tms/serge/configs` directory and test them inside the container by running the commands below. You can change/edit these files in your local filesystem since the directory is mounted in the container.
```

# Command to initialize and setup the sqlite3 database and pull the repository for the first time.
serge pull sampleconfigs.serge --initialize

# Command that does everything for a Serge cycle. You need to run it at least twice to complete a full translation cycle.
serge sync sampleconfig.serge

Alternatively you can use the following commands for parts of the process:

# Command to localize and generate the .po files.
serge localize sampleconfigs.serge

# Command to pull from translation service
serge pull-ts sampleconfigs.serge

# Command to push back to translation service
serge push-ts sampleconfigs.serge

# Command to push back to the original source repository
serge push sampleconfigs.serge
```
2. (B) FOR PYTHON APPS: Just run `python your_py_file.py` to execute any code you would like to run.

3. Remember you can change any code you would like locally in your machine (not inside Docker) and it will take effect within Docker. Use this step to make some changes to your code. Navigate into your application directory within the Docker container and verify that the changes appear correctly.

4. To tear down just run `exit` inside of the shell session. And you can ctrl+c to stop the container from running.


### Troubleshooting

#### Directory Permissions issue. It may look like the following:
```
Deleting directory '/var/serge/vcs/'
Creating directory '/var/serge/vcs/'
fatal: Could not get current working directory: No such file or directory
Exception occurred while processing configuration file:
Exit code: -128; last error: No such file or directory
```
The fix for this is to run your command with `sudo`.
`sudo serge pull sampleconfig.serge --initialize` which will give your environment the right privileges to create/destroy directories.

