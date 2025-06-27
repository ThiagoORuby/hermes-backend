run-dev:
	@poetry run fastapi dev api/app/app.py

crawl-g1:
	@scrapy crawl g1spider

crawl-uol:
	@scrapy crawl uolspider

crawl-all: crawl-g1 crawl-uol



