import json
import os

from kafka import KafkaConsumer  # type: ignore
from scraper import get_binance_article_content  # type: ignore
from sqlalchemy import MetaData, create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from transformers import pipeline  # type: ignore

sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

# Connect to the database
db_name = os.getenv("POSTGRES_DB")
db_pwd = os.getenv("POSTGRES_PASSWORD")
db_u = os.getenv("POSTGRES_USER")

engine = create_engine(f"postgresql://{db_u}:{db_pwd}@client_db/{db_name}")
metadata = MetaData()
metadata.reflect(bind=engine)
currencies_prediction_table = metadata.tables["currencies_predictions"]
scraped_websites_table = metadata.tables["scraped_websites"]

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def main():
    consumer = KafkaConsumer(
        "scraped_news",
        bootstrap_servers=["kafka:9092"],
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        auto_offset_reset="earliest",
    )
    print("connected to consumer")

    for message in consumer:
        print(f"Received: {message.value}")

        article_uri = message.value.get("link_page", None)
        currencies = message.value.get("currencies", None)
        hashed_url = message.value.get("hashed_url", None)
        if (
            not currencies
            or not isinstance(currencies, list)
            or len(currencies) == 0
            or not article_uri
            or not isinstance(article_uri, str)
            or not article_uri.startswith("https://www.binance.com/en/feed")
        ):
            continue

        scraped_website = (
            session.query(scraped_websites_table)
            .filter_by(hashed_url=hashed_url)
            .first()
        )
        if not scraped_website:
            continue

        try:
            article_content = get_binance_article_content(article_uri)
        except Exception as exc:
            print(f"Error while processing uri {article_uri}")
            print(f"Error while scraping article content: {exc}")
            continue

        article_content = article_content[:512]
        result = sentiment_pipeline(article_content)
        result = result[0]

        insert_data = currencies_prediction_table.insert().values(
            currencies=currencies, label=result["label"], website_id=scraped_website.id
        )
        try:
            session.execute(insert_data)
            session.commit()
        except Exception as exc:
            print(f"Error while inserting into the database: {exc}")
            session.rollback()


main()
