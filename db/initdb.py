import os

from sqlalchemy import ( # type: ignore
    ARRAY,
    BigInteger,
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    inspect,
)

# Connect to the database
db_name = os.getenv("POSTGRES_DB")
db_pwd = os.getenv("POSTGRES_PASSWORD")
db_u = os.getenv("POSTGRES_USER")

engine = create_engine(f"postgresql://{db_u}:{db_pwd}@client_db/{db_name}")
metadata = MetaData()


if not inspect(engine).has_table("scraped_websites"):
    print("Table scraped_websites does not exist, creating it...")
    table = Table(
        "scraped_websites",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("currencies", ARRAY(String)),
        Column("hashed_url", String, unique=True),
        Column("link_page", String),
        Column("published_at", String),
        Column("published_at_timestamp", BigInteger),
        Column("publish_from_when_scraped", String),
        Column("source_domain", String),
        Column("title", String),
    )
    table.create(engine)
else:
    print("Table scraped_websites already exists")

if not inspect(engine).has_table("btc_prices"):
    print("Table btc_prices does not exist, creating it...")
    table = Table(
        "btc_prices",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("timestamp", BigInteger),
        Column("open", Integer),
        Column("high", Integer),
        Column("low", Integer),
        Column("close", Integer),
        Column("volume", Integer),
    )
    table.create(engine)
else:
    print("Table btc_prices already exists")

if not inspect(engine).has_table("currencies_predictions"):
    print("Table currencies_predictions does not exist, creating it...")
    table = Table(
        "currencies_predictions",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("currencies", ARRAY(String)),
        Column("label", String) # positive, negative, neutral
    )
    table.create(engine)
else:
    print("Table currencies_predictions already exists")