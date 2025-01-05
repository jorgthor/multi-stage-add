"""
Pulls a list of numbers from RabbitMQ and adds them.
Returns the sum of the numbers to RabbitMQ.
"""
from src.rabbitmq import RabbitMQ
import json


def is_number(a):
    """
    Check if 'a' is a number
    :param a: Should be int or float
    :return: True if 'a' is a number, False otherwise
    """
    try:
        float(a)
    except ValueError:
        return False
    return True

def add(*args):
    """
    Add numbers
    :param args: number or list of numbers
    :return: sum of numbers
    """
    for a in args:
        if not is_number(a):
            return "Error: arguments must be numbers"
    return sum(map(float, args))

def callback(ch, method, properties, body):
    """
    Callback function
    :param ch: channel
    :param method: method
    :param properties: properties
    :param body: message
    """
    print(f'Received message: {body}')

def main():
    """
    Main function
    Constantly listens for messages from RabbitMQ,
    converts them to JSON, checks if they are numbers,
    adds them and sends the result back to RabbitMQ
    """
    rabbitmq = RabbitMQ()
    try:
        raw_data = rabbitmq.consume('add', callback)
        json_data = json.loads(raw_data)
        if json_data['num1'] and json_data['num2']:
            result = add(json_data['num1'], json_data['num2'])
            json_to_send = json.dumps({'service': 'add', 'result': result})
            rabbitmq.publish('add', json_to_send)
    except Exception as e:
        print(f'Error: {e}')
        json_to_send = json.dumps({'service': 'add', 'result': e})
        rabbitmq.publish('add', json_to_send)
    finally:
        rabbitmq.close()



if __name__ == '__main__':
    main()
