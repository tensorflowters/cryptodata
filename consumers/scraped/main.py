import json
import os

from kafka import KafkaConsumer
from sqlalchemy import MetaData, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

# Connect to the database
db_name = os.getenv("POSTGRES_DB")
db_pwd = os.getenv("POSTGRES_PASSWORD")
db_u = os.getenv("POSTGRES_USER")

engine = create_engine(f"postgresql://{db_u}:{db_pwd}@client_db/{db_name}")
metadata = MetaData()
metadata.reflect(bind=engine)
scraped_websites_table = metadata.tables["scraped_websites"]

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def consume_messages():
    consumer = KafkaConsumer(
        "scraped_news",
        bootstrap_servers=["kafka:9092"],
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        auto_offset_reset="earliest",
    )
    print("connected to consumer")
    print(consumer)

    for message in consumer:
        print(f"Received: {message.value}")
        try:
            # Insert data
            currencies = message.value.get("currencies", None)
            hashed_url = message.value.get("hashed_url", None)
            link_page = message.value.get("link_page", None)
            published_at = message.value.get("published_at", None)
            published_at_timestamp = message.value.get("published_at_timestamp", None)
            publish_from_when_scraped = message.value.get(
                "publish_from_when_scraped", None
            )
            source_domain = message.value.get("source_domain", None)
            title = message.value.get("title", None)

            insert_data = scraped_websites_table.insert().values(
                currencies=currencies,
                hashed_url=hashed_url,
                link_page=link_page,
                published_at=published_at,
                published_at_timestamp=published_at_timestamp,
                publish_from_when_scraped=publish_from_when_scraped,
                source_domain=source_domain,
                title=title,
            )
            session.execute(insert_data)

            # Commit the transaction
            session.commit()
        except IntegrityError:
            # Handle exceptions
            pass
        except Exception as exc:
            session.rollback()
            raise exc
        finally:
            # Close the session
            session.close()


print("Hello from container")
consume_messages()
