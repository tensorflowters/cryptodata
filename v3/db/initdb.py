import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ARRAY, inspect

# Connect to the database
db_name = os.getenv('POSTGRES_DB')
db_pwd = os.getenv('POSTGRES_PASSWORD')
db_u = os.getenv('POSTGRES_USER')

engine = create_engine(f'postgresql://{db_u}:{db_pwd}@client_db/{db_name}')
metadata = MetaData()


if not inspect(engine).has_table("scraped_websites"):
    print("Table does not exist, creating it...")
    table = Table('scraped_websites', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('currencies', ARRAY(String)),
                  Column('hashed_url', String),
                  Column('link_page', String),
                  Column('published_at', String),
                  Column('publish_from_when_scraped', String),
                  Column('source_domain', String),
                  Column('title', String),
                  )
    table.create(engine)
else:
    print("Table already exists")