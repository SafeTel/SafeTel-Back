# SafeTel Back - Data deployement

https://pkg.go.dev/github.com/go-resty/resty#section-readme

This repository holds SafeTel backend data deployment's code, the program name is **WILLE**.

## Golang packages

You can find here the documentation of packages used for this project.

- [Resty](https://github.com/go-resty/resty)


## How to run Wille

You need to install golang:

- [Install Golang](https://go.dev/doc/install)

then, you can run the project:

Command:
```sh
$ make          - Compile the project and generate a binary
```

Other rules:
```sh
$ make clean    - remove objects files and cached files
$ make fclean   - Perform a 'make clean' & remove binary
$ make re       - Perform 'make fclean' & 'make'
```

In case of a specific architecture, you have to possibility to compile the golang using different OS and Architecture:

Darwin :
```sh
$ make build-darwin-arch
$ make clean-darwin-arch
```

Linux:
```sh
$ make build-linux-arch
$ make clean-linux-arch
```

Windows:
```sh
$ make build-windows-arch
$ make clean-windows-arch
```