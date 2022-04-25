# Infrastructure as Code Project - Backend

This is the repository for the backend of the automated infrastructure deployment project.

## Developpement environment

To start developping on this project, you must have installed :
- python3

Start by executing : `pip install -r requirements.txt`

You can then launch the server by executing the file api_run.py

The app must be run from the iac-api context folder.

## Installation via docker-compose

To install the project on a production :

```yml
version: 3
services:
    api:
        image: mahjopi.gcr.io/the_image_name:latest
        restart: always
        container_name: api
        depends_on:
             - mongo
             - traefik
             - terraform
             - ansible
        volumes:
            - /var/api/config/:/home/api/config/ # Mounts the config folder
            - /var/log/api/:/home/api/log/
        networks:
            - backend:
        tags:
            - traefik.enable=true
            - traefik.backend.entryPoints=http
            - traefik.backend.passHostHeader=true
            - traefik.http.routers.backend-http.rule=Host(`THEDOMAIN`)
    traefik:
        image: traefik
        container_name: traefik
        restart: always
        volumes:
            - /var/traefik/:/etc/traefik/
            # path to docker socket
            - /var/run/docker.sock:/var/run/docker.sock
        networks:
            - backend:

    networks:
        backend:
```

## Automated tests

This project contains a part of automated tests. To run those tests, you can use the command : `[...]`

Copyright MahjoPi, 2022
