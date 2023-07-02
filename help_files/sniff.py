import socket
import struct
import time

# Create a raw socket
raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

# arbitrary number to signal a following INT header
# This is used in the outer L4 source port
INT_tbd = 12345

# IP protocol type indicators
ICMP_PROTO = 1
TCP_PROTO = 6
UDP_PROTO = 17

# Protocol lengths
# L2
ETHERNET_HEADER_LENGTH = 14
# L3
IP_HEADER_LENGTH = 20
# L4
ICMP_HEADER_LENGTH = 8
UDP_HEADER_LENGTH = 8
TCP_HEADER_LENGTH = 20

# INT and Telemetry protocols
TELEMETRY_REPORT_LENGTH = 16
INT_SHIM_LENGTH = 4
INT_META_LENGTH = 8
INT_TOTAL = TELEMETRY_REPORT_LENGTH     +\
            TELEMETRY_REPORT_LENGTH     +\
            INT_SHIM_LENGTH             +\
            INT_META_LENGTH
#-----------------------------

OUTER_ETHERNET_OFFSET = 0
OUTER_IP_HEADER_OFFSET = OUTER_ETHERNET_OFFSET + ETHERNET_HEADER_LENGTH
OUTER_L4_HEADER_OFFSET = OUTER_IP_HEADER_OFFSET + IP_HEADER_LENGTH


# INT_SHIM_OFFSET = INT_REPORT_HEADER_LENGTH+\
#                   ETHERNET_HEADER_LENGTH+\
#                   IP_HEADER_LENGTH

def TELEMETRY_REPORT_OFFSET(L4_proto):
    if  L4_proto == TCP_PROTO:
        L4_LENGTH = TCP_HEADER_LENGTH
    elif L4_proto == UDP_PROTO:
        L4_LENGTH = UDP_HEADER_LENGTH
    else:
        print("L4 protocol is non of the implemented options.")
    return OUTER_L4_HEADER_OFFSET + L4_LENGTH

while True:
    # Receive a packet - MTU of Ethernet is 1500, hence the packet_data size limit.
    packet_data, addr = raw_socket.recvfrom(1500)

    outer_ip_header = packet_data[OUTER_IP_HEADER_OFFSET:OUTER_L4_HEADER_OFFSET]

    # size of inner IP packet
    outer_ip_len = struct.unpack('!H', outer_ip_header[2:4])[0]

    # The L4 protocol is defined by the protocol field in the IPv4 header
    outer_L4_PROTO = outer_ip_header[9]

    # L4_header_length can be either 20 bytes (tcp) or 8 bytes (udp)
    if outer_L4_PROTO == 6:
        outer_L4_header = packet_data[OUTER_L4_HEADER_OFFSET:OUTER_L4_HEADER_OFFSET+TCP_HEADER_LENGTH]
        # Entire Outer payload size
        outer_payload = outer_ip_len-IP_HEADER_LENGTH-TCP_HEADER_LENGTH
    elif outer_L4_PROTO == 17:
        outer_L4_header = packet_data[OUTER_L4_HEADER_OFFSET:OUTER_L4_HEADER_OFFSET+UDP_HEADER_LENGTH]
        # Entire Outer payload size
        outer_payload = outer_ip_len-IP_HEADER_LENGTH-UDP_HEADER_LENGTH
    else:
        #print('not tcp or udp')
        # Go to next packet
        continue


    # the source and destination port numbers have the same byte field locations
    # for both udp and tcp
    outer_L4_dst = struct.unpack('!H', outer_L4_header[2:4])[0]

    # outer_L4_dst signals INT content, if the port number is equal to INT_tbd
    # Should also check the DSCP value of IP!!!
    if outer_L4_dst != INT_tbd:
        print("Destination Port:", outer_L4_dst)

        # Go to next packet
        continue

    # Calculate the telemetry report offset based on the L4 protocol
    telemetry_report_offset = TELEMETRY_REPORT_OFFSET(outer_L4_PROTO)

    # In case the report needs to be shown
    telemetry_report = packet_data[telemetry_report_offset:telemetry_report_offset+TELEMETRY_REPORT_LENGTH]

    INNER_ETHERNET_OFFSET = telemetry_report_offset+TELEMETRY_REPORT_LENGTH


    # Inner L3
    INNER_L4_HEADER_OFFSET = INNER_ETHERNET_OFFSET+ETHERNET_HEADER_LENGTH
    inner_ip_header = packet_data[INNER_L4_HEADER_OFFSET:INNER_L4_HEADER_OFFSET+IP_HEADER_LENGTH]

    # size of inner IP packet
    inner_ip_len = struct.unpack('!H', inner_ip_header[2:4])[0]

    # Inner L4
    inner_L4_PROTO = inner_ip_header[9]

    # L4_header_length can be either 20 bytes (tcp) or 8 bytes (icmp / udp)
    if inner_L4_PROTO == 6:
        # TCP header
        inner_L4_header = packet_data[INNER_L4_HEADER_OFFSET:INNER_L4_HEADER_OFFSET+TCP_HEADER_LENGTH]
        # original payload size
        inner_payload = inner_ip_len-IP_HEADER_LENGTH-TCP_HEADER_LENGTH

    elif inner_L4_PROTO == 17:
        #UDP header
        inner_L4_header = packet_data[INNER_L4_HEADER_OFFSET:INNER_L4_HEADER_OFFSET+UDP_HEADER_LENGTH]
        # original payload size
        inner_payload = inner_ip_len-IP_HEADER_LENGTH-UDP_HEADER_LENGTH

    elif inner_L4_PROTO == 1:
        #ICMP header
        inner_L4_header = packet_data[INNER_L4_HEADER_OFFSET:INNER_L4_HEADER_OFFSET+ICMP_HEADER_LENGTH]
        # original payload size
        inner_payload = inner_ip_len-IP_HEADER_LENGTH-ICMP_HEADER_LENGTH

    else:
        #print('not tcp, icmp or udp')
        # Go to next packet
        continue



    # int_size includes tel report, int shim, int meta(s)
    outer_payload - inner_payload = int_size

    # the entire int meta space
    int_meta_size = int_size - TELEMETRY_REPORT_LENGTH - INT_SHIM_LENGTH

    # divide int_meta_size with INT_META_LENGTH to find number of int meta payloads.
    number_of_int_meta = int_meta_size / INT_META_LENGTH













## Capture and process packets
# y = 1
# x = 1
# while True:
#     # Receive a packet - MTU of Ethernet is 1500, hence the packet_data size limit.
#     packet_data, addr = raw_socket.recvfrom(1500)
#
#     print("Packet:")
#     print(packet_data)
#
#     # Extract the Ethernet header (14 bytes)
#     ethernet_header = packet_data[:14]
#
#     # Extract and analyze specific fields from the Ethernet header
#     # formatted as a zero-padded two-digit lowercase hexadecimal number {:02x}
#     #destination_mac = ":".join("{:02x}".format(byte) for byte in ethernet_header[0:6])
#     #source_mac = ":".join("{:02x}".format(byte) for byte in ethernet_header[6:12])
#     #ethertype = ethernet_header[12:14].hex()
#
#     # Check if EtherType indicates an IP packet (0x0800)
#     if ethertype == '0800':
#         # Extract the IP header (20 bytes)
#         ip_header = packet_data[14:34]
#
#         # Extract and analyze specific fields from the IP header
#         version = ip_header[0] >> 4
#         ihl = (ip_header[0] & 0x0F) * 4
#         ttl = ip_header[8]
#         protocol = ip_header[9]
#         source_ip = socket.inet_ntoa(ip_header[12:16])
#         destination_ip = socket.inet_ntoa(ip_header[16:20])
#
#         # ICMP
#         # testing only
#         if protocol == ICMP_PROTO and destination_ip == '1.1.1.1':
#                 print(y)
#                 y = y + 1
#
#         if protocol == TCP_PROTO
#
#         # UDP
#         if protocol == UDP_PROTO:
#             # Extract the UDP header (8 bytes)
#             udp_header = packet_data[34:42]
#
#             # Extract and analyze specific fields from the UDP header
#             source_port, destination_port, length, checksum = \
#                 struct.unpack('!HHHH', udp_header)
#
#             # Print the extracted UDP header information
#             # Print the extracted IP header information
#             # print("Destination MAC:", destination_mac)
#             # print("Source MAC:", source_mac)
#             # print("EtherType:", ethertype)
#             # print("Version:", version)
#             # print("IHL:", ihl)
#             # print("TTL:", ttl)
#             # print("Protocol:", protocol)
#             # print("Source IP:", source_ip)
#             # print("Destination IP:", destination_ip)
#             # print("Protocol: UDP")
#             # print("Source Port:", source_port)
#             # if destination_port != INT_tbd:
#             #     print("Destination Port:", destination_port)
#             # else:
#             #     print("INT_tbd detected!", INT_tbd)
#             #     print("INT report included after UDP header")
#             #
#             # print("Length:", length)
#             # print("Checksum:", checksum)
#
#             # Packet counter
#             # print("packet number: "+ str(x))
#             # x=x+1
#             # print("------------------------")
