import json
import os

import psycopg2.errors
from confluent_kafka import Consumer, KafkaException
from dotenv import load_dotenv

from Lab2.DBManager import DBManager

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

conf = {
    'bootstrap.servers': f"localhost:{os.environ["KAFKA_PORT"]}",
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'
}

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "mpl",
    "user": "postgres",
    "password": "postgres",
}

consumer = Consumer(conf)

topic = 'events-mpl'
consumer.subscribe([topic])
db_manager = DBManager(DB_CONFIG)

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            json_data = json.loads(msg.value().decode("utf-8"))
            print(f'Получено сообщение: {json_data}')
            tn = json_data["table_name"]
            try:
                db_manager.create_table(tn, json_data["columns"])
            except psycopg2.errors.DuplicateTable:
                print(f"Таблица '{tn}' уже существует")
            db_manager.add_data_to_table(json_data["table_name"], json_data["data"])

finally:
    consumer.close()
