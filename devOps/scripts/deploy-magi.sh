#!/bin/bash
set -e

echo $1

if [ -z $1 ] || [[ $1 != "prod" && $1 != "dev" ]] ; then
    echo 'You need to define version: prod | dev'
    exit 0
else 
    echo "You are going to deploy magi_$1"
fi

echo 'If you are ready for the deploy, please trigger Enter'
read MYSQL_PRESENT

echo 'devOps absolute path parent folder:'
read DOCKER_DIRECTORY

echo "Deploying $1"

if [ ! -d "${DOCKER_DIRECTORY}/cd" ]; then
        echo "${DOCKER_DIRECTORY}  does not exists or does not contains docker-compose folder"
        exit 1
fi

cd $DOCKER_DIRECTORY/cd && docker-compose pull magi_$1 && docker-compose up -d --force-recreate --no-deps --build magi_$1