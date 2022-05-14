# SafeTel Back

<p align="center">
    <img src="https://github.com/SafeTel/SafeTel-Back/blob/master/images/Bouclier%20Safetel.png" width="200">
</p>



This repository holds SafeTel backend's code, the server name is **Magi**.


To know how to contribute follow [this link](https://github.com/SafeTel/Contribution).


To see the documentation about the server follow [this link](https://github.com/SafeTel/SafeTel-Doc-Backend).

## How to run the server

The server is wrapped with Docker.

Command:
```sh
$ sudo docker-compose build && sudo docker-compose up
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
