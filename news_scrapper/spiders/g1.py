import scrapy

from news_scrapper.items import PostItem


class G1Spider(scrapy.Spider):
    name = "g1spider"
    start_urls = ["https://g1.globo.com/"]

    def parse(self, response):  # pyright: ignore
        posts = response.css("*.bastian-feed-item")

        for post in posts:
            post_item = PostItem()
            post_item["image_url"] = post.css("img::attr(src)").get()

            link = post.css("a.feed-post-link::attr(href)").get()

            if link is None:
                yield None
            else:
                yield response.follow(link, self.parse_post, meta={"item": post_item})

    def parse_post(self, response):  # noqa: PLR6301
        post = response.meta["item"]

        # Ignora noticia de playlist
        if "playlist" in response.url:
            return

        # Ignora notícia em vídeo
        if response.css("div.vt").get():
            return

        post["title"] = response.css("div.title h1::text").get()
        post["url"] = response.url
        post["description"] = response.css("div.subtitle h2::text").get()
        post["date_published"] = response.css(
            "div.content-publication-data time::attr(datetime)"
        ).get()
        post["type"] = response.css("span.header-title a::text").get()
        post["source"] = "g1"

        yield post
