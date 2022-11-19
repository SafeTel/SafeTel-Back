#!/bin/bash
set -e

echo $1

if [ -z $1 ] || [[ $1 != "prod" && $1 != "dev" ]] ; then
    echo 'You need to define version: prod | dev'
    exit 0
else 
    echo "You are going to deploy magi_$1"
fi

echo "Deploying $1 with absolute path $2/cd"

if [ ! -d "$2/cd" ]; then
        echo "$2  does not exists or does not contains docker-compose folder"
        exit 1
fi

cd $2/cd && docker-compose pull magi_$1 && docker-compose up -d --force-recreate --no-deps --build magi_$1