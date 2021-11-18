# tts-portal

## Development Environment Setup

- [Install Docker](https://docs.docker.com/get-docker/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

## Architecture

Docker compose is used to build and launch the required Docker containers, networks, and storage volumes.

### Docker Configuration

These files determine how to build and configure each container.

| Container | Dockerfile     |
| --------- | -------------- |
| web       | Dockerfile.web |
| db        | Dockerfile.db  |

### Networking

Docker compose builds the private network **tts-net** that facilitates communication between the Python application and the database.

Port 80 of the web container is also redirected to port 8000 on the docker host.

After bringing up the containers, the development URL is available at:

http://localhost:8000/

### Containers

#### MySQL

The MySQL container uses a docker volume **tts-db** to cache MySQL table data. This storage
persists between a stop and start of a container, put is purged when an image is rebuilt.

#### Python Flask Webserver

The directory docroot/ is mounted inside the **db** container which is then served by the Flask UWSGI server.

## Operational Commands

To start up the Docker stack

```
docker-compose up
```

To shutdown the Docker stack

```
docker-compose down
```

To force a rebuild of existing containers from a down state

```
docker-compose build --force-rm
```

To launch an interactive session into the web server

```
docker exec -it web bash
```

To launch an interactive session into the database

```
docker exec -it db bash
mysql -u root -p beastm0de
```

When Python code is updated inside the docroot/ folder, the following command will instruct the running web container to reload the new code.

```
touch docroot/uwsgi.ini
```

When the database is configured with persistent mode, SQL data will live in the docker volume and not be reset when the MySQL container stops and starts. If a clean run is necessary the volume must be removed when the container is down:

```
docker volume ls
```

```
docker volume rm tts-portal_tts-db
```
