# image-generator

## Installation

### Without Docker

Create a virtualenv and activate it:

```bash
python3 -m venv venv
. venv/bin/activate
```

Or windows:

```bash
py -3 -m venv venv
venv\Scripts\activate.bat
```

Install all the dependencies.

```bash
pip3 install -r requirements.txt
```

Start the API

```bash
python3 api/main.py
```

### With Docker

Build the Docker container.

```bash
docker build -t image-generator .
```

Run the docker container and map the internal port to external port

```bash
docker run -p 5001:5001/tcp image-generator
```

## Swagger

Endpoints are documented using Swagger. To access the interactive documentation got to:

`/swagger`
