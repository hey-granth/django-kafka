# implements the consumer client

# BaseCommand is a Django class used to create custom management commands.
from django.core.management.base import BaseCommand
import requests, time

class Command(BaseCommand):
    help = 'kafka-like consumer client'

    # add_arguments method is used to define the command line arguments that the custom command can accept.
    def add_arguments(self, parser):
        parser.add_argument('group_id', type=str, help='Consumer group id')
        parser.add_argument('topic', type=str, help='Topic to consume from')
        parser.add_argument('--max-messages', type=int, help='Maximum number of messages to consume')

    # handle method is called when the custom command is executed
    def handle(self, *args, **options):
        print('Consuming messages from the Kafka topic')
        group_id = options['group_id']
        topic = options['topic']
        max_messages = options['max_messages']
        message_count = 0

        while True:
            if 0 < max_messages <= message_count:
                break
            response = requests.get('http://localhost:8000/api/messages/', params={'group_id': group_id, 'topic': topic, 'timeout': 5000})

            # status code 200 means the request was successful
            if response.status_code == 200:
                message = response.json()
                for msg in message:
                    self.process_message(msg)
                    message_count += 1
            else:
                self.stdout.write(self.style.ERROR('Error consuming messages'))
                time.sleep(5)

    def process_message(self, message):
        self.stdout.write(f'Received message: {message["partition"]}\nOffset {message["offset"]}: {message['key']} - {message["value"]}')
        # message[partition] is the partition number (number of a particular partition in the topic)
        # message[offset] is the offset number (number of messages that have been consumed from the partition)
        # message[key] is the key of the message
        # message[value] is the value of the message
