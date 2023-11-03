from scrapy import Spider, Request
from xml.etree import ElementTree as ET
from confluent_kafka import Producer
from pathlib import Path

class SpiderCryptoScrap(Spider):
    name = "cryptopanic"

    def __init__(self, *args, **kwargs):
        super(SpiderCryptoScrap, self).__init__(*args, **kwargs)
        self.producer = Producer({'bootstrap.servers': 'localhost:9092'})

    def delivery_report(self, err, msg):
        if err is not None:
            self.log(f"Message delivery failed: {err}")
        else:
            self.log(f"Message delivered to {msg.topic()}")

    def start_requests(self):
        urls = ["https://cryptopanic.com/news/rss/"]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        root = ET.fromstring(response.body)

        for item in root.findall(".//item"):
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''

            news_data = {
                'title': title,
                'link': link
            }

            self.producer.produce('crypto-news', key='key', value=str(news_data), callback=self.delivery_report)

        filename = "scrapped_results/cryptopanic/cryptopanic-news-rss.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        self.producer.flush()  # Make sure all messages are sent
