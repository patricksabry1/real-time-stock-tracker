from kafka import KafkaConsumer
import json 
import io
import avro.io
import avro.schema
import base64

with open('config.json', 'r') as f:
    config = json.load(f)

consumer = KafkaConsumer(
    config['KAFKA_TOPIC_NAME'],
    bootstrap_servers=f"{config['KAFKA_SERVER']}:{config['KAFKA_PORT']}",
    api_version=(0, 10, 1)
    )
# Define the Avro schema that corresponds to the encoded data
schema = avro.schema.parse(open('schemas/trades.avsc').read())

# print a constant stream of messages
for message in consumer:
    # Assume 'byte_string' contains the Avro-encoded byte string
    bytes_reader = io.BytesIO(message.value)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    data = reader.read(decoder)
    print(data)
    