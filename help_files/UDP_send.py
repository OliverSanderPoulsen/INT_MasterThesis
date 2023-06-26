import socket
import struct

# IP address of target (Collector)
UDP_IP = "127.1.2.3"
# UDP Port of target (Collector)
UDP_PORT = 5353

# Create a UDP socket for internet communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = b'\x54\x68\x69\x73\x20\x69\x73\x20\x61\x20\x74\x65\x73\x74\x2e'

header = 'xxx'
ingress_port = 252
egress_port = 113
timestamp = 12345
queue_occupancy = 5555
hop_by_hop = '4-5-2-1'
ttl = 64

# Pack the fields into a binary format
packet_data = struct.pack("!3sHHIH{}sB".format(len(hop_by_hop)),
                          header.encode(),
                          ingress_port,
                          egress_port,
                          timestamp,
                          queue_occupancy,
                          hop_by_hop.encode(),
                          ttl)


# Send the packet to the specified IP and port
for x in range(10):
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
