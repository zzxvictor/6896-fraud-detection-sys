import json
import base64
import redis
from kafka import KafkaProducer
from constants import CLUSTER_ARN, REQUEST_TOPIC, ZOOKEEPER, BOOTSTRAP_SERVERS, BootstrapBrokerStringTls
import datetime
import boto3


def verify_user(username, location):
    """
    user dynamoDB to verify user transaction simply based on location
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(DYNAMO_DB_NAME)
    response = table.get_item(
        Key={'username': username},
        ConsistentRead=True
    )
    if 'Item' not in response:
        print("no user record shown")
        return False
    db_location = response['Item']['location']
    if location != db_location:
        print("user location does not match db location!")
        return False
    print("user verified")
    return True


def publish_kafka_topics(producer, topic_name, data):
    print('publish to {} topic'.format(topic_name))
    producer.send(topic=topic_name, value=str.encode(data))
    producer.flush()
    print("finished publishing to {} topic".format(topic_name))


def parse_request(header, request) ->dict:
    """
    parse the request to a dictionary object
    sample header:
    ssn|cc_num|first|last|gender|street|city|state|zip|lat|long|city_pop|job|dob|acct_num|profile|trans_num|trans_date|trans_time|unix_time|category|amt|is_fraud|merchant|merch_lat|merch_long
    
    sample request:
    045-74-5650|3573869538621003|Vickie|Walker|F|161 Moyer Locks|Mont Alto|PA|17237|39.8417|-77.5537|1917|Press sub|1948-10-25|355104838454|adults_50up_female_rural.json|857d4af9c18e39c7b0961db6f58cfb07|2013-09-20|22:08:45|1379714925|misc_pos|50.80|1|fraud_Reynolds-Schinner|40.754953|-77.233002
    
    sample response:
    {'ssn': '045-74-5650', 'cc_num': '3573869538621003', 'first': 'Vickie', 'last': 'Walker', 'gender': 'F', 'street': '161 Moyer Locks', 'city': 'Mont Alto', 'state': 'PA', 'zip': '17237', 'lat': '39.8417', 'long': '-77.5537', 'city_pop': '1917', 'job': 'Press sub', 'dob': '1948-10-25', 'acct_num': '355104838454', 'profile': 'adults_50up_female_rural.json', 'trans_num': 'e8432e6b0f236e1a778238f78a29a28e', 'trans_date': '2013-05-26', 'trans_time': '19:58:38', 'unix_time': '1369598318', 'category': 'entertainment', 'amt': '73.07', 'is_fraud': '0', 'merchant': 'fraud_Turcotte, McKenzie and Koss', 'merch_lat': '40.389649', 'merch_long': '-77.677457'}
    """
    ret = {}
    headers = header.split("|")
    requests = request.split("|")
    for key, value in zip(headers, requests):
        ret[key] = value
    return ret


def handler(event, context):
    print(json.dumps(event))
    sample_fraud_request = "045-74-5650|3573869538621003|Vickie|Walker|F|161 Moyer Locks|Mont Alto|PA|17237|39.8417|-77.5537|1917|Press sub|1948-10-25|355104838454|adults_50up_female_rural.json|857d4af9c18e39c7b0961db6f58cfb07|2013-09-20|22:08:45|1379714925|misc_pos|50.80|1|fraud_Reynolds-Schinner|40.754953|-77.233002"
    
    sample_true_request = "045-74-5650|3573869538621003|Vickie|Walker|F|161 Moyer Locks|Mont Alto|PA|17237|39.8417|-77.5537|1917|Press sub|1948-10-25|355104838454|adults_50up_female_rural.json|e8432e6b0f236e1a778238f78a29a28e|2013-05-26|19:58:38|1369598318|entertainment|73.07|0|fraud_Turcotte, McKenzie and Koss|40.389649|-77.677457"
    
    # ssn|cc_num|first|last|gender|street|city|state|zip|lat|long|city_pop|job|dob|acct_num|profile|trans_num|trans_date|trans_time|unix_time|category|amt|is_fraud|merchant|merch_lat|merch_long
    parse = "ssn|cc_num|first|last|gender|street|city|state|zip|lat|long|city_pop|job|dob|acct_num|profile|trans_num|trans_date|trans_time|unix_time|category|amt|is_fraud|merchant|merch_lat|merch_long"
    
    frontend_request = event["transaction"]
    
    fraud_dict_sample = parse_request(parse, frontend_request)
    print(fraud_dict_sample)
    
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    publish_kafka_topics(producer, REQUEST_TOPIC, json.dumps(fraud_dict_sample))
    
    # producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    # msgs = event['records'].values()
    # for lst in msgs:
    #     for record in lst:
    #         print(record['value'], base64.b64decode(record['value']))
    #         information = json.loads(base64.standard_b64decode(record['value']).decode('utf-8'))
    #         username = information['username']
    #         location = information['location']
    #         timestamp = information['timestamp']
    #         print("generated at timestamp", timestamp)
    #         print(username, location)
    #         if verify_user(username, location):
    #             information["status"] = "approved"
    #             print("data is approved", information)
    #         else:
    #             information["status"] = "rejected"
    #             print("data is rejected", information)
    #         publish_kafka_topics(producer, "Status", json.dumps(information))
    #         # producer.flush()
    #         # producer.close()
    # # producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    # # print('publish approved transactions...')
    # # for _ in range(10):
    # #     time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    # #     producer.send(topic="Approved", value=str.encode(time))
    # # producer.flush()
    # # print('finished')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Approval request')
    }
