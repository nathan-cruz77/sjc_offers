# sjc_offers
Crawler for public offers made by the São José dos Campos city hall.

## Project setup
Build the project image:
```shell
docker build -t sjc_offers .
```

Run it with `docker-compose`:
```shell
docker-compose up
```

### Database
The database will be available at `localhost:27017`. You may access it (with the
project running) using:
```shell
docker exec -it mongo mongo
```

Crawled items can be found in the collection `offers` in the database `app`.

Data is store in the local folder `mongo_data` and multiple runs
**do not** duplicate items.

### Tests
Run tests with:
```shell
./test.sh
```
