# Asuka - SafeTel Back
---
This folder hold the save database's code, the tool name is **Asuka**.


To see the documentation about the tool follow [this link](https://github.com/SafeTel/SafeTel-Doc-Backend/wiki/Resume%3A-Tools).

## How to run the tool
---
Asuka is wrapped with Docker.

Command:
```sh
$ sudo docker-compose build && sudo docker-compose up
```

Don't forget to prune your docker before rerunning Asuka.

Command:
```sh
$ sudo docker system prune
```

If you have any weird trouble don't hesitate to prune everything.

Command:
```sh
$ sudo docker system prune -a
```

## Documentation
---
This tool save every 24h the dedicated database.

The saved files is of the following specific architecture:

```sh
- SavingFolder/DatabaseName/Collections.json
```

#### SavingFolder/

The name of the **SavingFolder/** is of the following format:

```
$MODE-$DATE-save/
```

With:
```
- $Mode: The database mode with 4 possible values: PROD/DEV/LOCAL/POSTMAN

- $Date: The date in ISO 8601 format with the specific structure:
    * %Y-%m-%d-T%H_%M_%SZ
        * %Y: Year
        * %m: month
        * %d: day
        * %H: hours
        * %M: minutes
        * %S: seconds
        * (Year)-(month)-(day)(T: time)(hours)_(minutes)_(seconds)(Z: Zone)
```