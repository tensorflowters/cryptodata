from scrapy import Spider, Request
from pathlib import Path


class SpiderCryptoScrap(Spider):
    name = "coinmarketcap"

    def start_requests(self):
        urls = ["https://coinmarketcap.com/community/articles/browse/?sort=-publishedOn"]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = "scrapped_results/coinmarketcap/coinmarketcap-news.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")