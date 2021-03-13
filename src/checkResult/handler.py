import json
import base64
import datetime
import boto3
import redis
from constants import *


redis_client = redis.Redis(host=REDIS_SERVER, port=REDIS_SERVER_PORT, ssl=None)


def handler(event, context):
    print(redis_client.get('045-74-5650_3573869538621003'))
    return {
        'statusCode': 200,
        'body': json.dumps("Hello World from batch writer !!!")
    }