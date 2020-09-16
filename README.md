# pydock

pydock creates versioned backups of docker-compose.yml inserting registry id's for tags.  So mariadb:latest becomes mariadb@sha256:e694a07f60a2bef2c48de9a2c852d05f8be9c76a8170b16f98809977398db07a
allowing you to get back to the exact images you were running at a particular point in time.  The intended usage is for indivuduals who sometimes use the latest tag and want to be able to update the entire stack with a docker-compose pull docker-compose up -d and be able to go back if needed.

Usage
Since the user is already using docker that is the suggested deployment method.  The steps to deploy are as follows:
1. git clone 
