"""
Class to handle RabbitMQ connection and message sending
"""
import os
import pika

class RabbitMQ:
    """
    Class to handle RabbitMQ connection and message sending
    """
    def __init__(self):
        """
        Initialize RabbitMQ connection
        """
        self.user = os.getenv('RABBITMQ_USER', 'user')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'password')
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = os.getenv('RABBITMQ_PORT', 5672)
        self.connection = None
        self.channel = None
        self.connect()


    def connect(self):
        """
        Connect to RabbitMQ
        """
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()


    def close(self):
        """
        Close RabbitMQ connection
        """
        if self.connection and not self.connection.is_closed:
            self.connection.close()


    def consume(self, queue_name, callback):
        """
        Consume messages from the queue
        :param queue_name:  name
        :param callback: Function to call when a message is received
        """
        if not self.channel:
            raise Exception('Channel is not initialized')
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()


    def publish(self, queue_name, message):
        """
        Publish a message to the queue
        :param queue_name: name
        :param message: message
        """
        if not self.channel:
            raise Exception('Channel is not initialized')
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2  # make message persistent
                                   ))
        print(f'Sendt message to {queue_name}: {message}')
