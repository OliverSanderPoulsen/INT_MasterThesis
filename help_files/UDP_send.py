import socket
import struct
import netifaces

# Get a list of network interfaces
interfaces = netifaces.interfaces()

# Print the interface names
for interface in interfaces:
    print(interface)


# IP address of target (Collector)
UDP_IP = "127.1.2.3"
# UDP Port of target (Collector)
UDP_PORT = 5353

# Create a UDP socket for internet communication
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = b''

# Send the packet to the specified IP and port
for x in range(1):
    byte_val = x.to_bytes(10, 'big')
    print(byte_val)
    sock.sendto(byte_val, (UDP_IP, UDP_PORT))

    # Print message as string
    int_val = int.from_bytes(byte_val, "big")
    print(int_val)

print("Header:", header)
print("Ingress Port:", ingress_port)
print("Egress Port:", egress_port)
print("Timestamp:", timestamp)
print("Queue Occupancy:", queue_occupancy)
print("Hop-by-Hop:", hop_by_hop)
print("TTL:", ttl)

# Close the socket
sock.close()
