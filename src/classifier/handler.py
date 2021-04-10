import json
import base64
from kafka import KafkaProducer
from constants import *
import datetime
import boto3
import redis
import random

frontend_url = "http://6895-frontend-host.s3-website-us-east-1.amazonaws.com"
redis_client = redis.Redis(host=REDIS_SERVER, port=REDIS_SERVER_PORT, ssl=None)
kafka_producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
sagemaker_client = boto3.client(service_name='sagemaker-runtime')


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


def dob_to_age(dob):
    datetime_format = '%Y-%m-%d'
    datetime_obj = datetime.strptime(dob, datetime_format)
    age = (datetime.now() - datetime_obj).days // 365
    return age


def gender_to_num(self, gender):
    if gender == 'F':
        return 0
    else:
        return 1


def handler(event, context):
    """
    right now it is a stupid classifier

    and after classification, it also need to publish to the kafka
    """
    # print(json.dumps(event))
    msgs = event['records'].values()

    # print("dealing with the kafka requests...")
    for lst in msgs:
        for record in lst:
            print(record['value'], base64.b64decode(record['value']))
            information = json.loads(
                base64.standard_b64decode(record['value']).decode('utf-8'))
            print(information)
            redis_key = '_'.join([information['ssn'], information['cc_num']])
            # # selected_features = ["gender", "street", "city", "state",
            # "zip", "lat", "long", "city_pop", "job", "dob", "trans_date",
            # "trans_time", "category", "amt", "merch_lat", "merch_long"]
            # selected_features = ["gender", "zip", "lat", "long",
            # "city_pop", "job", "dob",  "amt", "merch_lat", "merch_long"]

            # SAGEMAKER_ENDPOINT = "6895-sagemaker-scikit-learn"
            data = {'test': [[random.random() for i in range(10)]],
                    'train': [[random.random() for i in range(10)] for j in
                              range(150)]}
            ## !!!!! need to add permission for sagemaker in cloudformation!
            response = sagemaker_client.invoke_endpoint(
                EndpointName=SAGEMAKER_ENDPOINT,
                ContentType='application/json',
                Body=json.dumps(data).encode('utf-8'))
            result = response['Body'].read().decode('utf-8')
            result = json.loads(result)
            if result["result"] == 1:
                print("yes it is approved!")
                # approve transaction and put to another topic called Approve
                publish_kafka_topics(kafka_producer, APPROVE_TOPIC,
                                     json.dumps(information))
                redis_client.set(redis_key, 0)
            else:
                redis_client.set(redis_key, 1)
                print("It is likely to be fraud!")
                send_sns_correct_message(information)

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
