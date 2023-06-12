from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
from datetime import datetime, timedelta

# InfluxDB connection settings
url = "http://localhost:8086"  # Replace with the InfluxDB URL
token = "KuOnbHG3IK_4tmmWCJ3SCqeEMgneuiIuuUffHXoq7rBKfviHvVKMmsqYSsJuqcBXrwlr5h2HIDEzR18nySSxKg=="  # Replace with your InfluxDB token
org = "546ce3652d6c4557"  # Replace with your InfluxDB organization
bucket = "d1d7af80ebdedbe8"  # Replace with your InfluxDB bucket

# Create an InfluxDB client
client = InfluxDBClient(url=url, token=token)

# Define the number of data points to generate
num_data_points = 100

# Define the starting time for the data series
start_time = datetime.utcnow()

# Define the interval between data points
interval = timedelta(seconds=10)

# Create a write API instance
write_api = client.write_api(write_options=SYNCHRONOUS)

# Generate and send the dummy time series data
for i in range(num_data_points):
    # Generate a random value
    value = random.uniform(0, 1)

    # Create a data point with a specified measurement
    data_point = Point("dummy_measurement")

    # Add fields and tags to the data point
    data_point.field("value", value)
    data_point.tag("source", "dummy")

    # Add the timestamp to the data point
    timestamp = start_time + i * interval
    data_point.time(timestamp)

    # Write the data point to the InfluxDB bucket
    write_api.write(bucket=bucket, org=org, record=data_point)

# Close the InfluxDB client
client.close()
