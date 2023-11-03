from scrapy import Spider, Request
from pathlib import Path


class SpiderCryptoScrap(Spider):
    name = "cryptopanic"

    def start_requests(self):
        urls = ["https://cryptopanic.com/news/rss/"]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = "scrapped_results/cryptopanic/cryptopanic-news-rss.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
