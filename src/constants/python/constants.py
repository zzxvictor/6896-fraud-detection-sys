DYNAMODB_TABLE = "fraud-detection-sys-transaction-table"

PARTITION_KEY = "user_id"

SORT_KEY = "transaction_id"

CLUSTER_ARN = "arn:aws:kafka:us-east-1:614633518167:cluster/6895-kafka/79b186c0-fe86-4d7e-b50b-d09427fb4c48-14"

ZOOKEEPER = "z-3.6895-kafka.fo3vvt.c14.kafka.us-east-1.amazonaws.com:2181,z-2.6895-kafka.fo3vvt.c14.kafka.us-east-1.amazonaws.com:2181,z-1.6895-kafka.fo3vvt.c14.kafka.us-east-1.amazonaws.com:2181"

BOOTSTRAP_SERVERS = ["b-2.6895-kafka.fo3vvt.c14.kafka.us-east-1.amazonaws.com:9092","b-1.6895-kafka.fo3vvt.c14.kafka.us-east-1.amazonaws.com:9092"]

BootstrapBrokerStringTls = "b-2.6895-kafka.fo3vvt.c14.kafka.us-east-1.amazonaws.com:9094,b-1.6895-kafka.fo3vvt.c14.kafka.us-east-1.amazonaws.com:9094"

APPROVE_TOPIC = "Approve"

REQUEST_TOPIC = "Request"
