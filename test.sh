function rebuild {
  docker build -t sjc_offers .
}

function check {
  docker run -it sjc_offers scrapy check
}

rebuild && check
