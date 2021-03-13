import sagemaker
import json


def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps("Hello World from batch writer !!!")
    }