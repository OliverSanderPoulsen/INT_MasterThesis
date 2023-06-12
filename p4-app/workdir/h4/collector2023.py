# import socket
#
# UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
# UDP_PORT = 5353  # Choose a suitable port number
#
# # Create a UDP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# # Bind the socket to the IP address and port
# sock.bind((UDP_IP, UDP_PORT))
#
# print(f"UDP collector listening on {UDP_IP}:{UDP_PORT}")
#
# # Receive and process incoming packets
# while True:
#     data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes, adjust as needed
#     print(f"Received packet from {addr[0]}:{addr[1]}")
#     print(f"Data: {data()}")  # Assuming data is in string format, modify decoding accordingly
#     # Process the received data as per your requirements

# Receive data
import socket
import struct

# Forward to InfluxDB
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
from datetime import datetime, timedelta

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
bucket = "d1d7af80ebdedbe8"  # Replace with your InfluxDB bucket

# Create an InfluxDB client
client = InfluxDBClient(url=url, token=token)

# Create a write API instance
write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    # Receive data and address from the socket
    data, addr = sock.recvfrom(1024)  # Adjust the buffer size as needed

    # Unpack the received data as a struct
    unpacked_data = struct.unpack("!3sHHIH7sB", data)

    # Process the unpacked data
    header = unpacked_data[0].decode()
    ingress_port = unpacked_data[1]
    egress_port = unpacked_data[2]
    timestamp = unpacked_data[3]
    queue_occupancy = unpacked_data[4]
    hop_by_hop = unpacked_data[5].decode()
    ttl = unpacked_data[6]

    # Print or process the unpacked data as needed
    print("Header:", header)
    print("Ingress Port:", ingress_port)
    print("Egress Port:", egress_port)
    print("Timestamp:", timestamp)
    print("Queue Occupancy:", queue_occupancy)
    print("Hop-by-Hop:", hop_by_hop)
    print("TTL:", ttl)

    # Define time stamp for current data point
    timestamp = datetime.utcnow()

    

# Close the socket (this part is never reached in the infinite loop)
sock.close()
