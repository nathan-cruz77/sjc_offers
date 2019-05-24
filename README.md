# sjc_offers
Crawler for public offers made by the São José dos Campos city hall.

## Project setup
Simply run:
```shell
./run.sh
```

This requires [`docker-compose`](https://docs.docker.com/compose/) make sure you
have it instaled.

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

### Tests
Run tests with:
```shell
./test.sh
```
