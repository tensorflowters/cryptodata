from scrapy import Spider, Request
from pathlib import Path


class SpiderCryptoScrap(Spider):
    name = "googlenews"

    def start_requests(self):
        urls = ["https://news.google.com/search?q=cryptocurrency&hl=en-US&gl=US&ceid=US%3Aen"]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = "scrapped_results/googlenews/googlenews-news.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")