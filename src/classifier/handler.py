import json
import base64
from kafka import KafkaProducer
from constants import CLUSTER_ARN, APPROVE_TOPIC, ZOOKEEPER, BOOTSTRAP_SERVERS, BootstrapBrokerStringTls
import datetime
import boto3


def publish_kafka_topics(producer, topic_name, data):
    print('publish to {} topic'.format(topic_name))
    producer.send(topic=topic_name, value=str.encode(data))
    producer.flush()
    print("finished publishing to {} topic".format(topic_name))


def handler(event, context):
    """
    right now it is a stupid classifier
    
    and after classification, it also need to publish to the kafka
    """
    print(json.dumps(event))
    msgs = event['records'].values()
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    
    print("dealing with the kafka requests...")
    for lst in msgs:
        for record in lst:
            print(record['value'], base64.b64decode(record['value']))
            information = json.loads(base64.standard_b64decode(record['value']).decode('utf-8'))
            print(information)
            # this is dummy
            if int(information["is_fraud"]) == 0:
                # approve transaction and put to another topic called Approve
                publish_kafka_topics(producer, APPROVE_TOPIC, json.dumps(information))
                
            else:
                print("It is likely to be fraud!")
            # append_transaction_details(information)
            
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Approval request')
    }
