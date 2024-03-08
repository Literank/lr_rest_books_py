# lr_rest_books_py

Example project: RESTful API implemented with Flask in Python.

See [project tutorial](https://www.literank.com/project/16/intro) here.

This project provides a comprehensive guide on building a RESTful API using the Flask web framework in Python.

In the introduction step, you are guided on setting up the development environment and defining the objectives of the project.

The development step is broken down into various sub-sections, covering the creation of an initial version of the API, implementation of health endpoints, defining data models, setting up routes, implementing a 4-layer architecture, configuring databases such as MySQL and MongoDB, incorporating caching using Redis, implementing pagination and search functionality, and finally adding authentication mechanisms.

Finally, the deployment step covers various deployment options, including running with a WSGI server: Gunicorn, setting up a reverse proxy with Nginx, and deploying the application using Docker and Docker Compose.

Overall, this project tutorial offers a structured approach to building a robust RESTful API using Flask, covering essential aspects from development to deployment.

## Run with `flask`

```bash
flask --app main run --debug
```

## Run with Gunicorn

```bash
gunicorn -w 4 -b :5000 --log-level debug  main:app
```

## Run in Docker Compose

Create `compose/.env` file:

```bash
REDIS_PASSWORD=your_pass
MYSQL_PASSWORD=your_pass
MYSQL_ROOT_PASSWORD=your_root_pass
```

Run it:

```bash
cd compose
docker compose up
```

See [project tutorial](https://www.literank.com/project/16/intro) here.
