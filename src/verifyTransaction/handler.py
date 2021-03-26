import json
import redis
from constants import *

redis_client = redis.Redis(host=REDIS_SERVER, port=REDIS_SERVER_PORT, ssl=None)

def handler(event, context):
    print(event)
    user_id = event["user_id"]
    transaction_id = event["transaction_id"]
    redis_key = user_id + "_" + transaction_id
    redis_value = redis_client.get(redis_key)
    if redis_value is not None:
        redis_value = redis_value.decode("utf-8")
    print(redis_value)
    if redis_value == '1':
        statusCode = 200
        redis_client.set(redis_key, 0)
    elif redis_value == '0':
        statusCode = 208 # already reported
    elif redis_value == None:
        statusCode = 404
    else:
        statusCode = 403
    
    ret_dict = {
        200: "Your transaction is approved",
        208: "Your transaction has been approved. You don't need to approve it again",
        404: "Your transaction record is not found, please recheck your URL!",
        403: "Unknown Error, possibly forbidden"
    }
    return {
        'statusCode': statusCode,
        'body': json.dumps(ret_dict[statusCode])
    }
