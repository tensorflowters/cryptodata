from kafka import KafkaConsumer
import json


def consume_messages():
    consumer = KafkaConsumer(
        'scraped_news',
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda m: json.loads(m.decode('ascii')),
        auto_offset_reset='earliest'
    )
    print("connected to consumer")
    print(consumer)

    for message in consumer:
        print(f"Received: {message.value}")


print("Hello from container")
consume_messages()
