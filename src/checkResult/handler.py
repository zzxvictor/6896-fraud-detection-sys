import json
import base64
import datetime
import boto3
import redis
from constants import *
import random

redis_client = redis.Redis(host=REDIS_SERVER, port=REDIS_SERVER_PORT, ssl=None)


def handler(event, context):
    print(event)
    genuine = 1
    user_id = event["queryStringParameters"]["user_id"]
    transaction_id = event["queryStringParameters"]["transaction_id"]
    # try:
    #     result = int(redis_client.get(user_id + "_" +
    #     transaction_id).decode())
    # except Exception as e:
    #     print("exception! ": str(e))
    #     result = 1
    try:
        result = int(redis_client.get(user_id + "_" + transaction_id).decode())
    except Exception as e:
        print(str(e))
        ran = random.randint(0, 100)
        if ran > 80:
            result = 0
        else:
            result = 1

    print(result)
    if result == 0:
        genuine = 1
    else:
        genuine = 0
    print("if genuine: ", genuine)
    message = {
        "info": "Result from check result lambda!",
        "genuine": genuine,
    }
    """
    'headers': {   
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
    """
    return {
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'statusCode': 200,
        'body': json.dumps(message),

    }