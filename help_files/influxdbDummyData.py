import os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from random import randint
from datetime import datetime, timedelta

# Replace the placeholders with your InfluxDB connection details
url = "http://localhost:8086"
token = 'VyLD3TDJ7uhpkQSP-H3xCwrTu0spYCKIQpeXFyZIx7edaMSLurW4PFphFnTcXp7wEkFOA80rAJTJWPyZtHbQPQ=='
org = "DTU"
bucket = 'DummyData'

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def generate_dummy_data():
    point = Point("dummy_measurement") \
        .tag("tag1", "value1") \
        .tag("tag2", "value2") \
        .field("field1", randint(0, 100)) \
        .field("field2", randint(0, 100)) \
        .time(datetime.utcnow(), WritePrecision.NS)

    return point


while True:
    data_point = generate_dummy_data()

    # Write the data point to InfluxDB
    write_api.write(bucket=bucket, record=data_point)

    print(f"Inserted data point: {data_point.to_line_protocol()}")

    time.sleep(1)  # Wait for 1 second before inserting the next data point
