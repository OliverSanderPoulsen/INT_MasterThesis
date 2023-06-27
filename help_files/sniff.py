import socket
import struct

# Create a raw socket
raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

# Capture and process packets
x = 1
while True:
    # Receive a packet
    packet_data, addr = raw_socket.recvfrom(65535)

    # Extract the Ethernet header (14 bytes)
    ethernet_header = packet_data[:14]

    # Extract and analyze specific fields from the Ethernet header
    destination_mac = ":".join("{:02x}".format(byte) for byte in ethernet_header[0:6])
    source_mac = ":".join("{:02x}".format(byte) for byte in ethernet_header[6:12])
    ethertype = ethernet_header[12:14].hex()

    # Check if EtherType indicates an IP packet (0x0800)
    if ethertype == '0800':
        # Extract the IP header (20 bytes)
        ip_header = packet_data[14:34]

        # Extract and analyze specific fields from the IP header
        version = ip_header[0] >> 4
        ihl = (ip_header[0] & 0x0F) * 4
        ttl = ip_header[8]
        protocol = ip_header[9]
        source_ip = socket.inet_ntoa(ip_header[12:16])
        destination_ip = socket.inet_ntoa(ip_header[16:20])

        if protocol == 17:  # UDP
            # Extract the UDP header (8 bytes)
            udp_header = packet_data[34:42]

            # Extract and analyze specific fields from the UDP header
            source_port, destination_port, length, checksum = \
                struct.unpack('!HHHH', udp_header)

            # Print the extracted UDP header information
            # Print the extracted IP header information
            print("Destination MAC:", destination_mac)
            print("Source MAC:", source_mac)
            print("EtherType:", ethertype)
            print("Version:", version)
            print("IHL:", ihl)
            print("TTL:", ttl)
            print("Protocol:", protocol)
            print("Source IP:", source_ip)
            print("Destination IP:", destination_ip)
            print("Protocol: UDP")
            print("Source Port:", source_port)
            print("Destination Port:", destination_port)
            print("Length:", length)
            print("Checksum:", checksum)

            print("packet number: "+ str(x))
            x=x+1
            print("------------------------")
