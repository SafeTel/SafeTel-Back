# SafeTel Back

<p align="center">
    <img src="https://github.com/SafeTel/SafeTel-Back/blob/master/images/Bouclier%20Safetel.png" width="200">
</p>


This repository holds SafeTel backend's code, the server name is **Magi**.


To know how to contribute follow [this link](https://github.com/SafeTel/Contribution).


To see the documentation about the server follow [this link](https://github.com/SafeTel/SafeTel-Doc-Backend).

## How to make the project work for your environnement

To make the project work, you have several spets to complete:

Go to the good cluster:
* Go to mongodb Atlas: https://www.mongodb.com/cloud/atlas
* Sign In in MongoDb Atlas
* At the top of the page, click on the current team you're actually in, and click on the **SafeTel-EIP-team**
* Your now on the Project page. choose and click, in the project name column, on **SafeTel-Back** project


Now you are on the good Cluster for this current project. From the cluster page, follow the processus:
* Look at the left side bar. Click on **Network Access**
* Look at the right part of the page. Click on the green button name **+ADD IP ADRESS**
* Click on the button **ADD CURRENT IP ADDRESS**
* Click on the button **Confirm**

You can now run the project

## How to run the server

The server is wrapped with Docker.


Command:
```sh
$ sudo docker-compose up
```


Don't forget to prune your docker before rerunning Magi.


Command:
```sh
$ sudo docker system prune
```


If you have any weird trouble don't hesitate to prune everything.


Command:
```sh
$ sudo docker system prune -a
```

