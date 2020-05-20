# Pyazo

Pyazo is a self-hosted screenshot and image upload utility. It allows you to take a screenshot of a part of your screen and automatically upload it to your own server. You can also directly upload an image from your computer.

It is comprised of a cross-platform client written in Python which defers the actual taking of the screenshot to the built-in OS tools (macOS and Windows) or common utilities (Linux distributions). The server is written as a RESTful FastAPI app with support for basic user accounts and image sharing options.

## Compatibility

### Server

* Python >= 3.7 (check with `python --version`)

## Installation

The only official supported way to run the server is through docker-compose. First make a copy of the `.env-example` file, name it `.env` and change the settings inside accordingly.

| Key              | Default                    | Description                                                  |
|------------------|----------------------------|--------------------------------------------------------------|
| ENV              | production                 | FastAPI environment. Set to development to enable debugging  |
| POSTGRES_USER    | pyazo                      | Username of the postgres user                                |
| POSTGRES_PASSWORD| ' '                        | Password of the postgres user                                |
| POSTGRES_DB      | pyazo                      | Database name                                                |
| JWT_SECRET       | ' '                        | JWT secret                                                   |
| BLOCK_REGISTER   | 'False'                    | Blocks registration if true                                  |
| HOST_PUBLIC_MEDIA| /srv/http/pyazo            | Nginx public media path                                      |
| PUBLIC_PATH      | ./media/public/            | Public media storage path                                    |
| PRIVATE_PATH     | ./media/private/           | Private media storage path                                   |

Make a copy of the `docker-compose-prod.yml` file, name it `docker-compose.yml` and change the settings inside if needed.

Build the container using:

```shell
docker-compose build
```

Then run it using:

```shell
docker-compose up -d
```

## Documentation
https://pyazo.com/docs

## License and Credits

BSD 3-Clause

[Python]: <https://www.python.org/downloads/>
[Docker]: <https://docs.docker.com/>
[Docker Compose]: <https://docs.docker.com/compose/>

