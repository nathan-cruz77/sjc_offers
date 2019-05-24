# sjc_offers
Crawler for public offers made by the São José dos Campos city hall.

## Project setup
Install [`docker-compose`](https://docs.docker.com/compose/), if you don't have already, and run:
```shell
./run.sh
```

## Project setup (no docker)
Install python 3.7.

Install the project dependencies with:
```shell
pip install -r requirements.txt
```

If you are using [`pipenv`](https://pipenv.readthedocs.io/en/latest/):
```shell
pipenv install
```

To run the crawler use:
```shell
scrapy crawl offers
```

### Database
By default data will be inserted on a remote mongodb instance in
[atlas](https://www.mongodb.com/cloud) in the `offers` collection of the
`app` database.

If you prefer to have a local copy of the data, you may use the mongo instance
created by docker-compose. For this change the `MONGO_URI` setting on `settings.py`
to:
```python
MONGO_URI = 'mongodb://mongo'
```

The database will be available at `localhost:27017`. You may access it (with the
project running) using:
```shell
docker exec -it mongo mongo
```

Data is store in the local folder `mongo_data`.

In either setup multiple runs **do not** duplicate items.

Note: No mongo instance will be created if you are running the project
outside of docker-compose. In that case, if you intend to use a local database,
it should be setup prior to running the project.

### Tests
Run tests with:
```shell
./test.sh
```

Or, if you are not using docker:
```shell
scrapy check
```
