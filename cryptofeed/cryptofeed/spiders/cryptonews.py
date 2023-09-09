from scrapy import Spider, Request
from pathlib import Path


class SpiderCryptoScrap(Spider):
    name = "cryptonews"

    def start_requests(self):
        urls = ["https://cryptonews.com/news/"]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = "scrapped_results/cryptonews/cryptonews-news.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")