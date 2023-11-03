
from scrapy import Spider, Request
from pathlib import Path


class SpiderCryptoScrap(Spider):
    name = "binance"

    def start_requests(self):
        urls = ["https://www.binance.com/en-IN/feed/news"]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = "scrapped_results/binance/binance-news.json"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")