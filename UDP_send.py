import socket
import struct

UDP_IP = "127.1.2.3"  # Replace with the desired IP address
UDP_PORT = 5353  # Replace with the desired port number

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
sock.sendto(packet_data, (UDP_IP, UDP_PORT))

print("Header:", header)
print("Ingress Port:", ingress_port)
print("Egress Port:", egress_port)
print("Timestamp:", timestamp)
print("Queue Occupancy:", queue_occupancy)
print("Hop-by-Hop:", hop_by_hop)
print("TTL:", ttl)

# Close the socket
sock.close()
