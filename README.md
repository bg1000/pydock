# pydock

When using docker-compose using the latest tag can be convenient but sometimes problematic as it is hard to get back to the previous image after an update. Pydock creates rotating backups of your docker-compose.yml file as docker-compose.yml.1, docker-compose.yml.2 etc. The docker python sdk is used to obtain the id for each image from the docker repository. The backups use these id's rather than the original tag.  For example, mariadb:latest might become mariadb@sha256:e694a07f60a2bef2c48de9a2c852d05f8be9c76a8170b16f98809977398db07a. The backups are rotated such that docker-compose.yml.1 is always the most recent backup.  If your upgrade goes poorly getting back to the previous state can be as simple as running `docker-compose -f docker-compose.yml.1 up -d`.

There is the possibility, of course, that new versions of applications have changed the data on disk. To cover this possibility I also recommend you backup the data with a snapshot or other method prior to upgrading.

# Usage

Since you are already using docker that is the suggested deployment method.  The steps to deploy are as follows:

1. `git clone https://github.com/bg1000/pydock.git`
2. `cd pydock`
3. edit config.yaml.  There are three settings:
  - log_level - you may use any standard python logging level.
  - versions - pydock will create docker-compose.yml.1, docker-compose.yml.2, etc.  The files are rotated so docker-compose.yml.1 is always the most recent. Versions is an integer that specifies the number of versions you wish to keep.
  - compose_file - put the path to your compose file here.
 4. build the container with `docker build -t pydock .`
 5. run with `docker run -v /path/to/compose:/path/to/compose/in/config/file -v /var/run/docker.sock:/var/run/docker.sock pydock`

If you find yourself changing the configuration often it may be convenient to store config.yaml outside of the container and create an additional volume mapping for that.

 Run tests from top level (pydock) directory with `python3 -m unittest`
