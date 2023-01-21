import pika

from models import Contact
import connect_to_db.connect

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
chanel = connection.channel()

chanel.queue_declare(queue="send_email_queue", durable=True)


def send_email(contact_id):
    contacts = Contact.objects(id=contact_id)
    contact = contacts[0]
    print(f"Send something on {contact.email}")
    contact.send_message = True
    contact.save()


def callback_result(ch, method, properties, body):
    print(f"Received message: {body} from producer")
    contact_id = body.decode()
    send_email(contact_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    chanel.basic_qos(prefetch_count=1)
    chanel.basic_consume(queue="send_email_queue", on_message_callback=callback_result)
    chanel.start_consuming()


if __name__ == "__main__":
    main()
