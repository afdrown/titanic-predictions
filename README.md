# Titanic Survival Prediction Dockerized Application#

Build the image using the following command

```bash
$ docker build -t titanic_predict .
```

Run the Docker container using the command shown below.

```bash
$ docker run --rm -it -p 5000:5000 -t titanic_predict
```

The application will be accessible at http://localhost:5000/api
