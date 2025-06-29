import scrapy

from news_scrapper.items import PostItem


class UOLSpider(scrapy.Spider):
    name = "uolspider"
    start_urls = ["https://uol.com.br/"]

    def parse(self, response):  # type: ignore
        posts = response.css("div.headlineSub__link")[:20]
        VALID_URLS = ["www.uol.com.br", "noticias.uol.com.br"]
        for post in posts:
            post_item = PostItem()
            post_item["image_url"] = post.css("img::attr(src)").get()

            link = post.xpath("../@href").get()

            for url in VALID_URLS:
                if url in link:
                    yield response.follow(
                        link, self.parse_post, meta={"item": post_item}
                    )

    def parse_post(self, response):  # noqa: PLR6301
        post = response.meta["item"]

        description = (
            response.css("div.jupiter-paragraph-fragment")[0]
            .xpath("./p[1]//text()")
            .getall()
        )

        if not post.get("image_url"):
            post["image_url"] = response.css(
                "figure.solar-photo-content img::attr(src)"
            ).get()
        post["title"] = response.css("h1.title::text").get()
        post["url"] = response.url
        post["description"] = "".join(description)
        post["date_published"] = response.css("time::attr(datetime)").get()
        post["type"] = response.css("span.kicker-item a::text").get()
        post["source"] = "uol"

        yield post
