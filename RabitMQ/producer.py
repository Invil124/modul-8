from faker import Faker
import pika

from models import Contact
import connect_to_db.connect

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
chanel = connection.channel()

chanel.exchange_declare(exchange="send_email", exchange_type="direct")
chanel.queue_declare(queue="send_email_queue", durable=True)
chanel.queue_bind(exchange="send_email", queue="send_email_queue")


def fill_database():
    fake = Faker("uk_UA")
    for _ in range(10):
        contact = Contact()
        contact.full_name = fake.name()
        contact.email = fake.email()
        contact.date_of_registration = fake.date_between(start_date="-1y")
        contact.send_message = False
        contact.save()


def main():

    fill_database()

    contacts = Contact.objects()

    for contact in contacts:
        contact_id = f"{contact.id}"
        message = contact_id.encode()

        chanel.basic_publish(
            exchange="send_email",
            routing_key="send_email_queue",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(f"Contact id: {message}, successfully send")

    connection.close()


if __name__ == "__main__":
    main()