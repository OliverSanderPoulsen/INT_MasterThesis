import socket
import struct
import time

# Create a raw socket
raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

# arbitrary number to signal a following INT header
INT_tbd = 12345

#
ICMP_PROTO = 1
TCP_PROTO = 6
UDP_PROTO = 17

ETHERNET_HEADER_LENGTH = 14
IP_HEADER_LENGTH = 20
ICMP_HEADER_LENGTH = 8
UDP_HEADER_LENGTH = 8
TCP_HEADER_LENGTH = 20

INT_REPORT_HEADER_LENGTH = 16
INT_SHIM_LENGTH = 4
INT_SHIM_WORD_LENGTH = 1
INT_META_LENGTH = 8
INT_META_WORD_LENGTH = 2

OUTER_ETHERNET_OFFSET = 0
OUTER_IP_HEADER = OUTER_ETHERNET_OFFSET + ETHERNET_HEADER_LENGTH
OUTER_L4_HEADER_OFFSET = OUTER_IP_HEADER + IP_HEADER_LENGTH


INNER_ETHERNET_OFFSET = INT_REPORT_HEADER_LENGTH
INNER_IP_HEADER_OFFSET = INNER_ETHERNET_OFFSET + ETHERNET_HEADER_LENGTH
INNER_L4_HEADER_OFFSET = INNER_IP_HEADER_OFFSET + IP_HEADER_LENGTH

INT_SHIM_OFFSET = INT_REPORT_HEADER_LENGTH+\
                  ETHERNET_HEADER_LENGTH+\
                  IP_HEADER_LENGTH


def eth_report(pkt):
    return pkt[0:ETHERNET_HEADER_LENGTH]


def ip_report(pkt):
    return pkt[OUTER_IP_HEADER:OUTER_IP_HEADER+IP_HEADER_LENGTH]

def udp_report(pkt):
    return pkt[OUTER_L4_HEADER_OFFSET:OUTER_L4_HEADER_OFFSET+UDP_HEADER_LENGTH]

raw_payload = bytes(packet[Raw]) # to get payload

telemetry_report = TelemetryReport(raw_payload[0:INT_REPORT_HEADER_LENGTH])
#telemetry_report.show()

inner_eth = Ether(raw_payload[INNER_ETHERNET_OFFSET:INNER_ETHERNET_OFFSET+ETHERNET_HEADER_LENGTH])
#inner_eth.show()

inner_ip = IP(raw_payload[INNER_IP_HEADER_OFFSET : INNER_IP_HEADER_OFFSET+IP_HEADER_LENGTH])

# Capture and process packets
y = 1
x = 1
while True:
    # Receive a packet
    packet_data, addr = raw_socket.recvfrom(1500)

    # Extract the Ethernet header (14 bytes)
    ethernet_header = packet_data[:14]

    # Extract and analyze specific fields from the Ethernet header
    # formatted as a zero-padded two-digit lowercase hexadecimal number {:02x}
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

        # ICMP
        if protocol == 1 and destination_ip == '1.1.1.1':
                print(y)
                y = y + 1

        if protocol == 17:  # UDP
            # Extract the UDP header (8 bytes)
            udp_header = packet_data[34:42]

            # Extract and analyze specific fields from the UDP header
            source_port, destination_port, length, checksum = \
                struct.unpack('!HHHH', udp_header)

            # Print the extracted UDP header information
            # Print the extracted IP header information
            # print("Destination MAC:", destination_mac)
            # print("Source MAC:", source_mac)
            # print("EtherType:", ethertype)
            # print("Version:", version)
            # print("IHL:", ihl)
            # print("TTL:", ttl)
            # print("Protocol:", protocol)
            # print("Source IP:", source_ip)
            # print("Destination IP:", destination_ip)
            # print("Protocol: UDP")
            # print("Source Port:", source_port)
            # if destination_port != INT_tbd:
            #     print("Destination Port:", destination_port)
            # else:
            #     print("INT_tbd detected!", INT_tbd)
            #     print("INT report included after UDP header")
            #
            # print("Length:", length)
            # print("Checksum:", checksum)

            # Packet counter
            # print("packet number: "+ str(x))
            # x=x+1
            # print("------------------------")
