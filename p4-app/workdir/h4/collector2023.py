# Receive data
import socket
import struct
import time
# Forward to InfluxDB
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta

# Dummy data
import random

UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 5353  # Replace with the desired port number

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the IP address and port
sock.bind((UDP_IP, UDP_PORT))


# InfluxDB connection settings
url = "http://localhost:8086"  # Replace with the InfluxDB URL
token = "KuOnbHG3IK_4tmmWCJ3SCqeEMgneuiIuuUffHXoq7rBKfviHvVKMmsqYSsJuqcBXrwlr5h2HIDEzR18nySSxKg=="  # Replace with your InfluxDB token
org = "546ce3652d6c4557"  # Replace with your InfluxDB organization
bucket = "b2cebaef043b65f4"  # Replace with your InfluxDB bucket

# Create an InfluxDB client
#client = InfluxDBClient(url=url, token=token)

# Create a write API instance
#write_api = client.write_api(write_options=SYNCHRONOUS)


def send_data(queue_size, delay, bit_size, packet_efficiency_ratio):
    point = Point("Meta_data").tag("device_id", "12345")  # Add any additional tags as needed

    # Add fields to the data point
    point = point.field("queue_size", queue_size)
    point = point.field("delay", delay)
    point = point.field("bit_size", bit_size)
    point = point.field("packet_efficiency_ratio", packet_efficiency_ratio)

    # Add timestamp to the data point
    point = point.time(datetime.utcnow())

    # Write the data point to the InfluxDB bucket
    #write_api.write(bucket=bucket, org=org, record=point)

while True:
    # Receive data and address from the socket
    data, addr = sock.recvfrom(1024)  # Adjust the buffer size as needed

    print(data.decode('utf-8'))

    # Unpack the received data as a struct
    #unpacked_data = struct.unpack("!3sHHIH7sB", data)

    # Process the unpacked data
    #header = unpacked_data[0].decode()
    #ingress_port = unpacked_data[1]
    #egress_port = unpacked_data[2]
    #timestamp = unpacked_data[3]
    #queue_occupancy = unpacked_data[4]
    #hop_by_hop = unpacked_data[5].decode()
    #ttl = unpacked_data[6]

    # Print or process the unpacked data as needed
    #print("Header:", header)
    #print("Ingress Port:", ingress_port)
    #print("Egress Port:", egress_port)
    # print("Timestamp:", timestamp)
    # print("Queue Occupancy:", queue_occupancy)
    # print("Hop-by-Hop:", hop_by_hop)
    # print("TTL:", ttl)

    # queue_size = random.uniform(0.0, 10.0)
    # delay = random.uniform(0.0, 100.0)
    # bit_size = random.uniform(0.0, 1000.0)
    # packet_efficiency_ratio = random.uniform(0.0, 1.0)

    #send_data(queue_size, delay, bit_size, packet_efficiency_ratio)

    # Might not be necessary
    #time.sleep(1)

# Close the InfluxDB client (this part is never reached in the infinite loop)
#client.close()

# Close the socket (this part is never reached in the infinite loop)
sock.close()
