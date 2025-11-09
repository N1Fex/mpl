from confluent_kafka import Producer, admin
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

config = {
    'bootstrap.servers': f"localhost:{os.environ["KAFKA_PORT"]}",
}

producer = Producer(config)

kafka_admin = admin.AdminClient(config)
new_topic   = admin.NewTopic('events-mpl', 1, 1)
kafka_admin.create_topics([new_topic,])

def send_message(topic, message):
    try:
        producer.produce(
            topic=topic,
            value=message,
            callback=delivery_report
            )
        producer.flush()
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def delivery_report(err, msg):
    if err:
        print(f"Ошибка доставки: {err}")
    else:
        print(f"  Успешно в: {msg.topic()}")
