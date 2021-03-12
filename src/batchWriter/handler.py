import json
import base64
import datetime
import boto3
def handler(event, context):
    print(json.dumps(event))
    return {
        'statusCode': 200,
        'body': json.dumps("Hello World from batch writer !!!")
    }
