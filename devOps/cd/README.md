# Continuous deployment of Safetel


This repository holds SafeTel backend's files for continuous deployment.

To see the documentation about the continuous deployment, follow [this link](https://github.com/SafeTel/SafeTel-Doc-Backend).

## How the Continuous Deployment work

The CD of the server works using Docker


### Docker-Compose

This file is used by github action for the automatic deployment of the backend.

You can find inside the docker-compose the two services:
- **magi_dev**
- **magi_prod**

These services are automatically called at each push on the branch DEV and Master

To run the **prod** version of magi:
Command:
```sh
$ docker-compose up -d --force-recreate --no-deps --build magi_prod
```


To run the **dev** version of magi:
Command:
```sh
$ docker-compose up -d --force-recreate --no-deps --build magi_dev
```


If you have any weird trouble don't hesitate to prune everything.
Command:
```sh
$ sudo docker system prune -a
```
