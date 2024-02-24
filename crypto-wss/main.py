import asyncio
import json
import os

import websockets
from sqlalchemy import create_engine, MetaData  # type: ignore
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

# Connect to the database
db_name = os.getenv("POSTGRES_DB")
db_pwd = os.getenv("POSTGRES_PASSWORD")
db_u = os.getenv("POSTGRES_USER")

engine = create_engine(f"postgresql://{db_u}:{db_pwd}@client_db/{db_name}")
metadata = MetaData()
metadata.reflect(bind=engine)
btc_table = metadata.tables["btc_prices"]

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


async def fill_db_from_blockhain_ws(token):
    uri = "wss://ws.blockchain.info/mercury-gateway/v1/ws"
    try:
        async with websockets.connect(
            uri, extra_headers={"Origin": "https://exchange.blockchain.com"}
        ) as websocket:
            await websocket.send(
                json.dumps({"token": token, "action": "subscribe", "channel": "auth"})
            )
            await websocket.send(
                json.dumps(
                    {
                        "token": token,
                        "action": "subscribe",
                        "channel": "prices",
                        "symbol": "BTC-USD",
                        "granularity": 60,
                    }
                )
            )
            print("Subscribed, now listening for messages...")
            while True:
                try:
                    message = await websocket.recv()
                    print(message)
                    obj = json.loads(message)
                    if "price" in obj and "seqnum" in obj:
                        [timestamp, _open, high, low, close, volume] = obj["price"]
                        print(timestamp, _open, high, low, close, volume)
                        insert_data = btc_table.insert().values(
                            id=int(obj.get("seqnum")),
                            timestamp=int(timestamp),
                            open=int(_open),
                            high=int(high),
                            low=int(low),
                            close=int(close),
                            volume=int(volume),
                        )
                        session.execute(insert_data)
                        try:
                            session.commit()
                        except IntegrityError:
                            pass
                        except Exception as exc:
                            session.rollback()
                            raise exc
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed")
                    break
                except Exception as e:
                    print(f"Error receiving message: {e}")
                    break
    except Exception as e:
        print(f"WebSocket connection failed: {e}")


token = os.getenv("BLOCKCHAIN_API_KEY")
asyncio.run(fill_db_from_blockhain_ws(token))
