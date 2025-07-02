run-dev:
	@poetry run fastapi dev api/app/app.py

crawl-g1:
	@poetry run scrapy crawl g1spider

crawl-uol:
	@poetry run scrapy crawl uolspider

crawl-all: crawl-g1 crawl-uol

test:
	@pytest -s -x --cov=api --cov=core -vv

