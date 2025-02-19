# implements the producer client

# BaseCommand is a Django class used to create custom management commands.
from django.core.management.base import BaseCommand
import requests, time, json

class Command(BaseCommand):
    help = 'kafka-like producer client'

    def add_arguments(self, parser):
        parser.add_argument('topic', type=str, help='Topic to produce to')
        parser.add_argument('--file', type=str, help='File containing messages to produce')
        parser.add_argument('--key', type=str, help='Key for the message')
        parser.add_argument('--value', type=str, help='Value for the message')

    def handle(self, *args, **options):
        print('Producing messages to the Kafka topic')
        if options['file']:
            self.produce_from_file(options['topic'], options['file'])
        else:
            self.produce_message(options['topic'], options['key'], options['value'])

    def produce_from_file(self, topic, file):
        with open(file, 'r') as f:
            for line in f:
                key, value = line.split(',', 1)
                self.produce_message(topic, key, value)
                time.sleep(1)

    def produce_message(self, topic, key, value):
        payload = {'topic': topic, 'key': key, 'value': value}
        response = requests.post('http://localhost:8000/api/messages/', json=payload)
        self.print_response(response)

    def print_response(self, response):
        # status code 201 means the request was successful
        if response.status_code == 201:
            data = response.json()
            self.stdout.write(self.style.SUCCESS(f'Message produced: {data["partition"]}\nOffset {data["offset"]}: {data["key"]} - {data["value"]}'))
        else:
            self.stdout.write(self.style.ERROR('Error producing message'))
            self.stdout.write(response.text)