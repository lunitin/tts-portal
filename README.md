# tts-portal

## Development Environment Setup

- [Install Docker](https://docs.docker.com/get-docker/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)
- [Install Watchman](https://facebook.github.io/watchman/docs/install.html) (optional)

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

Port 80 of the web container is also redirected to port 8080 on the docker host.

After bringing up the containers, the development URL is available at:

http://localhost:8080/

This port can be customized in config.py

### Containers

#### MySQL

The MySQL container uses a docker volume **tts-db** to cache MySQL table data. This storage
persists between a stop and start of a container, put is purged when an image is rebuilt.

#### Python Flask Webserver

The directory docroot/ is mounted inside the **db** container which is then served by the Flask UWSGI server.

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

## Performance Enhancements

#### `WORKERS_PER_CORE`

This image will check how many CPU cores are available in the current server running your container.

It will set the number of workers to the number of CPU cores multiplied by this value.

By default:

- `2`

You can set it in docker-compose.yaml

```bash
WORKERS_PER_CORE: 4
```

If you used the value `3` in a server with 2 CPU cores, it would run 6 worker processes.

You can use floating point values too.

So, for example, if you have a big server (let's say, with 8 CPU cores) running several applications, and you have an ASGI application that you know won't need high performance. And you don't want to waste server resources. You could make it use `0.5` workers per CPU core.

In a server with 8 CPU cores, this would make it start only 4 worker processes.

#### `WEB_CONCURRENCY`

Override the automatic definition of number of workers.

By default:

- Set to the number of CPU cores in the current server multiplied by the environment variable `WORKERS_PER_CORE`. So, in a server with 2 cores, by default it will be set to `4`.

You can set it in docker-compose.yaml

```bash
WEB_CONCURRENCY: 2
```

For more options see: https://github.com/tiangolo/meinheld-gunicorn-flask-docker

## Watchman

Watchman is a helper application that will watch files in the project for changes and trigger a reload of the Flask app when changes have been detected.

To simplify things, the docker-compose and watchman commands are wrapped in a makefile.

Bring up the Docker stack

```
make up
```

Stop the Docker stack

```
make down
```

Rebuild all Docker containers

```
make clean
```
