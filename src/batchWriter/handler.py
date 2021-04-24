import json
import base64
import datetime
from constants import DYNAMODB_TABLE, PARTITION_KEY, SORT_KEY
import boto3
def handler(event, context):
    print(json.dumps(event))
    msgs = event['records'].values()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)
    for lst in msgs:
        for record in lst:
            # print(record['value'], base64.b64decode(record['value']))
            information = json.loads(base64.standard_b64decode(record['value']).decode('utf-8'))
            print(information)
            item = {}
            # use SSN as user's SSN for now
            try:
                item[PARTITION_KEY] = information["ssn"]
                item[SORT_KEY] = information["trans_num"]
                item["raw_records"] = json.dumps(information)
                table.put_item(Item=item)
                print("put record to dynamoDB")
            except Exception as e:
                print(str(e))
                continue
    return {
        'statusCode': 200,
        'body': json.dumps("Hello World from batch writer !!!")
    }
