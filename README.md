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

The database will be available at `localhost:27017`. You may access it (with the
project running) using:
```shell
docker exec -it mongo mongo
```
