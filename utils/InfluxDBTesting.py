# Here, we initialize the token, organization info, and server url that are needed to set up the initial connection to InfluxDB.
# The client connection is then established with the InfluxDBClient initialization.
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

  token = os.environ.get("INFLUXDB_TOKEN")
  org = "DTU"
  url = "http://localhost:8086"

  write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


# we define five data points and write each one to InfluxDB. Each of the 5 points we write has a field and a tag.
  bucket="TestBucket"

  write_api = client.write_api(write_options=SYNCHRONOUS)

  for value in range(5):
    point = (
      Point("measurement1")
      .tag("tagname1", "tagvalue1")
      .field("field1", value)
    )
    write_api.write(bucket=bucket, org="DTU", record=point)
    time.sleep(1) # separate points by 1 second

    query_api = client.query_api()

    query = """from(bucket: "TestBucket")
     |> range(start: -10m)
     |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org="DTU")

    for table in tables:
      for record in table.records:
        print(record)


# Flux query
query_api = client.query_api()

query = """from(bucket: "TestBucket")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="DTU")

for table in tables:
  for record in table.records:
    print(record)


# we use the mean() function to calculate the average value of data points in the last 10 minutes.
query_api = client.query_api()

query = """from(bucket: "TestBucket")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="DTU")

for table in tables:
    for record in table.records:
        print(record)
