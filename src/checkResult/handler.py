import json
import base64
import datetime
import boto3
import redis
from constants import *


redis_client = redis.Redis(host=REDIS_SERVER, port=REDIS_SERVER_PORT, ssl=None)


def handler(event, context):
    print(event)
    user_id = event["queryStringParameters"]["user_id"]
    transaction_id = event["queryStringParameters"]["transaction_id"]
    redis_key = user_id + "_" + transaction_id
    redis_value = redis_client.get(redis_key)
    if redis_value is not None:
        redis_value = redis_value.decode("utf-8")
    print(redis_value)
    if redis_value == '0':
        # not fraud
        statusCode = 200
    elif redis_value == '1':
        # fraud
        statusCode = 403
    elif redis_value is None:
        # pending, the value is none
        statusCode = 208 # already reported
    else:
        statusCode = 404
    
    ret_dict = {
        200: "Your transaction is approved",
        208: "Your transaction is still pending",
        404: "Unkonwn error",
        403: "Your transaction is a potential fraud. Please check your message to approve your transaction!"
    }
    print(ret_dict[statusCode])
    return {
        'headers': {   
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'statusCode': statusCode,
        'body': json.dumps(ret_dict[statusCode])
    }