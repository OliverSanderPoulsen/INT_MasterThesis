import socket
import struct
import time

# Create a raw socket
raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

#Bind to the eth0 interface
interface = 'eth0'
raw_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, bytes(interface, 'utf-8'))

# arbitrary number to signal a following INT header

# This is used in the outer L4 source port
# Only in telemetry report 2.0
#INT_tbd = 12345

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
#-----------------------------

OUTER_ETHERNET_OFFSET = 0
OUTER_IP_HEADER_OFFSET = OUTER_ETHERNET_OFFSET + ETHERNET_HEADER_LENGTH
OUTER_L4_HEADER_OFFSET = OUTER_IP_HEADER_OFFSET + IP_HEADER_LENGTH


def L4_VARIABLE_LEN(L4_proto):
    if  L4_proto == ICMP_PROTO:
        L4_LENGTH = TCP_HEADER_LENGTH
    elif  L4_proto == TCP_PROTO:
        L4_LENGTH = TCP_HEADER_LENGTH
    elif L4_proto == UDP_PROTO:
        L4_LENGTH = UDP_HEADER_LENGTH
    else:
        print("L4 protocol is non of the implemented options.")
    return L4_LENGTH

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
        continue
        outer_L4_header = packet_data[OUTER_L4_HEADER_OFFSET:OUTER_L4_HEADER_OFFSET+TCP_HEADER_LENGTH]
        # Entire Outer payload size
        outer_payload = outer_ip_len - IP_HEADER_LENGTH-TCP_HEADER_LENGTH - TELEMETRY_REPORT_LENGTH

    elif outer_L4_PROTO == 17:
        outer_L4_header = packet_data[OUTER_L4_HEADER_OFFSET:OUTER_L4_HEADER_OFFSET+UDP_HEADER_LENGTH]


        # Entire Outer payload size
        outer_payload = outer_ip_len - IP_HEADER_LENGTH - UDP_HEADER_LENGTH
    else:
        #print('not tcp or udp')
        # Go to next packet
        continue

    # Only a INT 2.0 mechanism
    # outer_L4_dst signals INT content, if the port number is equal to INT_tbd
    # if outer_L4_dst != INT_tbd:
    #     #print("Destination Port:", outer_L4_dst)
    #
    #     # Go to next packet
    #     continue

    # Calculate the telemetry report offset based on the L4 protocol
    telemetry_report_offset = OUTER_L4_HEADER_OFFSET + L4_VARIABLE_LEN(outer_L4_PROTO)

    # In case the report needs to be shown
    telemetry_report = packet_data[telemetry_report_offset:telemetry_report_offset+TELEMETRY_REPORT_LENGTH]

    INNER_ETHERNET_OFFSET = telemetry_report_offset+TELEMETRY_REPORT_LENGTH


    # Inner L3
    INNER_IP_HEADER_OFFSET = INNER_ETHERNET_OFFSET+ETHERNET_HEADER_LENGTH
    inner_ip_header = packet_data[INNER_IP_HEADER_OFFSET:INNER_IP_HEADER_OFFSET+IP_HEADER_LENGTH]

    # size of inner IP packet
    inner_ip_len = struct.unpack('!H', inner_ip_header[2:4])[0]

    # Perform bitwise operations to extract the DSCP field from the inner ip header
    dscp = (inner_ip_header[1] & 0xFC) >> 2
    #print("dscp: ", dscp)

    # Check if the inner packet contains int data
    if dscp != 0x17:
        continue

    # Inner L4
    inner_L4_PROTO = inner_ip_header[9]
    INNER_L4_HEADER_OFFSET = INNER_IP_HEADER_OFFSET + IP_HEADER_LENGTH

    # L4_header_length can be either 20 bytes (tcp) or 8 bytes (icmp / udp)
    if inner_L4_PROTO == 6:
        # TCP header
        inner_L4_header = packet_data[INNER_L4_HEADER_OFFSET:INNER_L4_HEADER_OFFSET+TCP_HEADER_LENGTH]
        # original payload size
        inner_payload = inner_ip_len-IP_HEADER_LENGTH-TCP_HEADER_LENGTH

        # INT payload
        INT_payload =   outer_payload-\
                        TELEMETRY_REPORT_LENGTH-\
                        ETHERNET_HEADER_LENGTH-\
                        IP_HEADER_LENGTH-\
                        TCP_HEADER_LENGTH -\
                        inner_payload

    elif inner_L4_PROTO == 17:
        #UDP header
        inner_L4_header = packet_data[INNER_L4_HEADER_OFFSET:INNER_L4_HEADER_OFFSET+UDP_HEADER_LENGTH]
        # original payload size
        inner_payload = inner_ip_len-IP_HEADER_LENGTH-UDP_HEADER_LENGTH

        # INT payload
        INT_payload =   outer_payload-\
                        TELEMETRY_REPORT_LENGTH-\
                        ETHERNET_HEADER_LENGTH-\
                        IP_HEADER_LENGTH-\
                        UDP_HEADER_LENGTH -\
                        inner_payload

    elif inner_L4_PROTO == 1:
        #ICMP header
        inner_L4_header = packet_data[INNER_L4_HEADER_OFFSET:INNER_L4_HEADER_OFFSET+ICMP_HEADER_LENGTH]
        # original payload size
        inner_payload = inner_ip_len-IP_HEADER_LENGTH-ICMP_HEADER_LENGTH

        # INT payload
        INT_payload =   outer_payload-\
                        TELEMETRY_REPORT_LENGTH-\
                        ETHERNET_HEADER_LENGTH-\
                        IP_HEADER_LENGTH-\
                        ICMP_HEADER_LENGTH -\
                        inner_payload

    else:
        #print('not tcp, icmp or udp')
        # Go to next packet
        continue

    # Check if mininet pings shows up
    #print('destination_port: ', outer_L4_dst)
    #print('telemetry report: ', telemetry_report)
    #print('-----------')

    # INT SHIM
    #print(inner_L4_PROTO)
    INT_SHIM_OFFSET = INNER_L4_HEADER_OFFSET + L4_VARIABLE_LEN(inner_L4_PROTO)
    int_shim = packet_data[INT_SHIM_OFFSET:INT_SHIM_OFFSET+INT_SHIM_LENGTH]

    #INT META HEADER
    INT_META_OFFSET = INT_SHIM_OFFSET + INT_SHIM_LENGTH
    int_meta_header =  packet_data[INT_META_OFFSET: INT_META_OFFSET+INT_META_LENGTH]


    INT_META_DATA_OFFSET = INT_META_OFFSET+INT_META_LENGTH

    # INT meta header variables
    # done with chatgpt
    int_ver = (struct.unpack('!B', int_meta_header[0:1])[0] >> 4)
    int_rep = (struct.unpack('!B', int_meta_header[0:1])[0] >> 2) & 0b11
    int_c = (struct.unpack('!B', int_meta_header[0:1])[0] >> 1) & 0b1
    int_e = struct.unpack('!B', int_meta_header[0:1])[0] & 0b1
    int_m = (struct.unpack('!B', int_meta_header[1:2])[0] >> 7) & 0b1
    int_reserved = (struct.unpack('!H', int_meta_header[1:3])[0] >> 6) & 0b1111111111
    int_hop_ml = (struct.unpack('!B', int_meta_header[3:4])[0] >> 3) & 0b00011111
    int_remaining_hop_cnt = struct.unpack('!B', int_meta_header[4:5])[0]
    int_instruction_mask_0003 = (struct.unpack('!B', int_meta_header[5:6])[0] >> 4) & 0b00001111
    int_instruction_mask_0407 = struct.unpack('!B', int_meta_header[5:6])[0] & 0b00001111
    int_instruction_mask_0811 = (struct.unpack('!B', int_meta_header[6:7])[0] >> 4) & 0b00001111
    int_instruction_mask_1215 = struct.unpack('!B', int_meta_header[6:7])[0] & 0b00001111
    #int_reserved2 = struct.unpack('!H', int_meta_header[7:9])[0]

    # int_data_size includes tel report, int shim, int meta header, int meta data
    int_size = outer_payload - inner_payload

    int_meta = packet_data[INT_META_DATA_OFFSET:INT_META_DATA_OFFSET+int_size+500]
    print('-------------------------------------')
    print(int_size)
    print(int_meta)

    # the entire int meta space
    int_meta_size = int_size - TELEMETRY_REPORT_LENGTH - INT_SHIM_LENGTH - INT_META_LENGTH



    # divide int_meta_size with INT_META_LENGTH to find number of int meta payloads.
    #number_of_int_meta =



    print('Packet:')
    print('')
    print("--Outer--")
    outer_ip_header_src = socket.inet_ntoa(outer_ip_header[12:16])
    outer_ip_header_dst = socket.inet_ntoa(outer_ip_header[16:20])
    print('IP4 src address: ', outer_ip_header_src)
    print('IP4 dst address: ', outer_ip_header_dst)

    outer_L4_src = struct.unpack('!H', outer_L4_header[0:2])[0]
    outer_L4_dst = struct.unpack('!H', outer_L4_header[2:4])[0]
    print("L4 src port:", outer_L4_src)
    print("L4 dst port:", outer_L4_dst)
    print('')

    print("--Telemetry Report--")
    telemetry_report_sw_id = struct.unpack('!i', telemetry_report[4:8])[0]
    telemetry_report_sq_number = struct.unpack('!i', telemetry_report[8:12])[0]
    telemetry_report_ing_time = struct.unpack('!i', telemetry_report[12:16])[0]
    print("sw id: ", telemetry_report_sw_id)
    print("sequence number: ", telemetry_report_sq_number)
    print("Ingress timestamp: ", telemetry_report_ing_time)
    print('')

    print("--Inner--")
    inner_ip_header_src = socket.inet_ntoa(inner_ip_header[12:16])
    inner_ip_header_dst = socket.inet_ntoa(inner_ip_header[16:20])
    print('inner IP4 src address: ', inner_ip_header_src)
    print('inner IP4 dst address: ', inner_ip_header_dst)

    inner_L4_src = struct.unpack('!H', inner_L4_header[0:2])[0]
    inner_L4_dst = struct.unpack('!H', inner_L4_header[2:4])[0]
    print("inner L4 src port:", inner_L4_src)
    print("inner L4 dst port:", inner_L4_dst)
    print('')

    print('--INT SHIM--')
    # Not working..
    #int_shim_type = struct.unpack('!H', bytes([int_shim[0], 0][0]))
    #print('int shim type:', int_shim_type)
    print('')

    print('--INT Meta Header--')
    print("Ver:", int_ver)
    print("Rep:", int_rep)
    print("C:", int_c)
    print("E:", int_e)
    print("M:", int_m)
    print("Reserved:", int_reserved)
    print("Hop ML:", int_hop_ml)
    print("RemainingHopCnt:", int_remaining_hop_cnt)
    print("Instruction bits:")
    print('0003: ', int_instruction_mask_0003)
    print('0407: ', int_instruction_mask_0407)
    print('0811: ', int_instruction_mask_0811)
    print('1215: ', int_instruction_mask_1215)
    #print("Reserved:", int_reserved2)
    print('------------')
    print('')
    print('')













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
