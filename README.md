# tts-portal

## Development Environment Setup

- [Install Docker](https://docs.docker.com/get-docker/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)


After cloning the repository create a local configuration file:

```
cp docroot/app/config.example.py docroot/app/config.py
```

Edit `docroot/app/config.py` and customize the URL, port, mail settings, and secret keys as needed.


## Architecture

Docker compose is used to build and launch the required Docker containers, networks, and storage volumes.

### Docker Configuration

These files determine how to build and configure each container.

| Container | Dockerfile     |
| --------- | -------------- |
| web       | Dockerfile.web |
| db        | Dockerfile.db  |


### Networking

Docker compose builds the private network **tts-net** that facilitates communication between the Python application and the MariaDB database.

By default, port 80 of the web container is redirected to port 8080 on the docker host.

After bringing up the containers, the development URL is available by default at:

http://localhost:8080/

This port can be customized in `docroot/app/config.py`


### Containers

#### MariaDB

The db container uses a docker volume **tts-db** to store MariaDB table data. By default, this storage persists between a stop and start of a container, but is purged when an image is rebuilt. If tmpfs is used, then the database will be reloaded
every time the container is started.

#### Python Flask Webserver

The directory `docroot/` is mounted inside the **db** container which is then served by the Flask UWSGI server.

##### Python Packages

New python packages should be added to the **_requirements.txt_** file. Upon container creation, pip will install all packages in that file.

## Docker Compose Commands

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

When the database is configured with persistent mode, SQL data will live in the docker volume and not be reset when the MySQL container stops and starts. If a clean run is necessary the volume must be removed when the container is down:

```
docker volume ls
```

```
docker volume rm tts-portal_tts-db
```

## Performance Enhancements

Edit `Dockerfile.web` and customize the NGINX and UWSGI worker processes.

For details on these options see: https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/


If running on Linux/OSX, tmpfs can be enabled to load the database into memory for faster performance.

Edit `docker-compose.yml` and uncomment the `tmpfs:` section.


## Splash Images

Login page background images are loaded randomly from `docroot/app/static/images/splash`. Simply add more images to expand the options.

**Ensure only valid image files exist in this directory.**

## API Docs

To view the API documentation, simply navigate to the BASE_URL/apidocs

Ex. http://localhost:8080/apidocs
