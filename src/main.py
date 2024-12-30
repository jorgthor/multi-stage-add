"""
Pulls a list of numbers from Redis and adds them.
Returns the sum of the numbers to Redis.
"""
from redis import Redis

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

def main():
    """
    Main function
    Pulls a list of numbers from Redis and adds them.
    Returns the sum of the numbers to Redis.
    If the list is empty or contains non-numeric values,
        it returns an error message to Redis.
    """
    redis = Redis(
        host='redis',
        port=6379,
        db=0,
        decode_responses=True,
        charset='utf-8',
        socket_timeout=5
    )
    redis_list = redis.lrange('numbers', 0, -1)
    if not redis_list:
        redis.set('sum', 'Error: list is empty')
    sum_ = add(*redis_list)
    redis.set('sum', sum_)

if __name__ == '__main__':
    main()
