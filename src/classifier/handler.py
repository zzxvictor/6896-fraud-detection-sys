import json
import base64
from kafka import KafkaProducer
from constants import *
from boto3.dynamodb.conditions import Key
import datetime
import boto3
import redis
import random

frontend_url = "http://6895-frontend-host.s3-website-us-east-1.amazonaws.com"
redis_client = redis.Redis(host=REDIS_SERVER, port=REDIS_SERVER_PORT, ssl=None)
kafka_producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
sagemaker_client = boto3.client(service_name='sagemaker-runtime')

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(DYNAMODB_TABLE)


def publish_kafka_topics(producer, topic_name, data):
    print('publish to {} topic'.format(topic_name))
    producer.send(topic=topic_name, value=str.encode(data))
    producer.flush()
    print("finished publishing to {} topic".format(topic_name))


def send_sns_correct_message(information):
    # note: ADD PERMISSIONS TO SNS
    print("send correction messages to client...")
    sms = boto3.client('sns')
    url = frontend_url + "/verify.html" + '?user_id={}&transaction_id={' \
                                          '}'.format(
        information["ssn"], information["cc_num"])

    loc_detail = ', '.join(
        [information["street"], information["city"], information["state"]])
    time_detail = ', '.join(
        [information["trans_date"], information["trans_time"]])
    amount = information["amt"]
    merchant = information["merchant"]
    phone_number = "+17348828920"
    message = "You made a transaction of {}".format(amount)
    merchant += " at {}".format(time_detail)
    message += " to {}.".format(merchant)
    message += "\nThe location of the transaction is {}".format(loc_detail)
    message += "\nClick the following link to verify your transaction. If it " \
               "is not you, just ignore this message."
    message += '\n {}'.format(url)
    response = sms.publish(
        PhoneNumber=str(phone_number), Message=message,
        MessageAttributes={
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Transactional'
            }
        }
    )
    print(response)


def drop_identifiers(requests,
                     drop_columns=["ssn", "cc_num", "trans_num", "is_fraud"]):
    """
    requests is in dictionary form

    return clean data dict
    """
    clean_data_dict = {}
    for key, val in requests.items():
        if key in drop_columns:
            continue
        else:
            clean_data_dict[key] = val
    return clean_data_dict


def get_train_test(dynamoDB_response, test_dict):
    """
    test_dict is given dictionary object
    test_dict is de-indentified
    return train_arr and test_arr, which are both 2d arrays
    """
    test_arr_raw = []
    for val in test_dict.values():
        test_arr_raw.append(val)
    test_arrs = [test_arr_raw]
    train_arrs = []

    for item in dynamoDB_response['Items']:
        print(item)
        train_dict = json.loads(item["raw_records"])

        print("train_items...,", train_dict)
        train_item = []
        for key in test_dict.keys():
            train_item.append(train_dict[key])
        train_arrs.append(train_item)

    print(train_arrs)
    print(test_arrs)
    return train_arrs, test_arrs


def handler(event, context):
    """
    right now it is a stupid classifier

    and after classification, it also need to publish to the kafka
    """
    drop_columns = ["ssn", "cc_num", "acct_num", "trans_num", "is_fraud"]

    print(json.dumps(event))
    msgs = event['records'].values()

    print("dealing with the kafka requests...")
    # DYNAMODB_TABLE
    for lst in msgs:
        for record in lst:
            try:
                print(record['value'], base64.b64decode(record['value']))
                raw_information = json.loads(
                    base64.standard_b64decode(record['value']).decode('utf-8'))
                print("Raw information: \n", raw_information)
                information = drop_identifiers(raw_information,
                                               drop_columns=drop_columns)

                print("Clean information: \n", information)
                redis_key = '_'.join(
                    [raw_information['ssn'], raw_information['trans_num']])
                print("Redis key: ", redis_key)

                """
                need to grab from database
                """
                response = table.query(
                    KeyConditionExpression=Key(PARTITION_KEY).eq(
                        raw_information['ssn'])
                )

                print("dynameDB result:\n", response)
                total = response['Count']

                train, test = get_train_test(response, information)

                genuine = 0
                if total < 20:
                    # too few data to classfiy, return yes
                    print("Too Few Data now, approve immediately!")
                    # approve transaction and put to another topic called
                    # Approve
                    print(raw_information)
                    publish_kafka_topics(kafka_producer, APPROVE_TOPIC,
                                         json.dumps(raw_information))
                    redis_client.set(redis_key, 0)
                    genuine = 1
                else:
                    # SAGEMAKER_ENDPOINT = "6895-sagemaker-scikit-learn"
                    data = {'test': test,
                            'train': train}
                    ## !!!!! need to add permission for sagemaker in
                    # cloudformation!
                    response = sagemaker_client.invoke_endpoint(
                        EndpointName=SAGEMAKER_ENDPOINT,
                        ContentType='application/json',
                        Body=json.dumps(data).encode('utf-8'))
                    result = response['Body'].read().decode('utf-8')
                    result = json.loads(result)
                    print("classification result:", result)

                    if result["result"] == 1:
                        print("yes it is approved!")
                        # approve transaction and put to another topic called
                        # Approve
                        print(raw_information)
                        publish_kafka_topics(kafka_producer, APPROVE_TOPIC,
                                             json.dumps(raw_information))
                        redis_client.set(redis_key, 0)
                        genuine = 1
                    else:

                        redis_client.set(redis_key, 1)
                        print("It is likely to be fraud!")

                        ## for now, not using sns for now. Uncomment after
                        # modification
                        # send_sns_correct_message(information)
                        genuine = 0
            except Exception as e:
                print(str(e))
                continue;

            # if int(information["is_fraud"]) == 0:
            #     # approve transaction and put to another topic called Approve
            #     publish_kafka_topics(kafka_producer, APPROVE_TOPIC,
            #     json.dumps(information))
            #     redis_client.set(redis_key, 0)
            # else:
            #     redis_client.set(redis_key, 1)
            #     print("It is likely to be fraud!")
            #     send_sns_correct_message(information)

            # append_transaction_details(information)
    # redis_key = '_'.join([information['ssn'], information['cc_num']])
    # redis_client.set(redis_key, 1)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Approval request')
    }
