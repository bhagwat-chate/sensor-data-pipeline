import argparse
from uuid import uuid4
from src.kafka_config import sasl_conf, schema_config
from six.moves import input
from src.kafka_logger import logging
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka import Producer
import pandas as pd
from typing import List
from src.entity.generic import Generic, instance_to_dict


FILE_PATH = "sample_data/kafka-sensor-data/aps_failure_training_set.csv"


def car_to_dict(car: Generic, ctx):
    return car.record


def delivery_report(err, msg):
    if err is not None:
        logging.info("Delivery faild for user record {} : {}".format(msg.key(), err))
        return
    logging.info("user record {} successfully produced to {} [{}] at offset {}".format(msg.key(), msg.topic(), msg.partition(), msg.offset()))


def product_data_using_file(topic, file_path):
    logging.info(f"Topic: {topic} file_path: {file_path}")
    schema_str = Generic.get_schema_to_produce_consume_data(file_path=file_path)
    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    string_serializer = StringSerializer('utf_8')
    json_serializer = JSONSerializer(schema_str, schema_registry_client, instance_to_dict)
    producer = Producer(sasl_conf())

    print("Producing user records to topic {}. ^C to exit.".format(topic))

    producer.poll(0.0)

    try:
        for instance in Generic.get_object(file_path=file_path):
            print(instance)

            logging.info(f"Topic: {topic} file_path: {instance.to_dict()}")
            producer.produce(topic=topic,
                             key=string_serializer(str(uuid4()), instance.to_dict()),
                             value = json_serializer(instance, SerializationContext(topic, MessageField.VALUE)),
                             on_delivery=delivery_report)
            print("\n Flushing records...")
            producer.flush()
    except KeyboardInterrupt:
        pass
    except ValueError:
        print("Invalid input, discarding record...")
        pass