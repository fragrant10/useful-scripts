#!/bin/bash
docker stop $(docker ps -aq) -f
docker rm $(docker ps -aq) -f
docker rmi $(docker images -aq) -f
