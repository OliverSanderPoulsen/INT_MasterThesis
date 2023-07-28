#!/usr/bin/env python
import sys
import struct
import binascii
import MySQLdb
import socket
import uuid
import json
from datetime import datetime
import calendar

###
class TelemetryReport:
    def __init__(self, raw_payload):
        self.ver = (raw_payload[0] >> 4) & 0xF
        self.len = raw_payload[0] & 0xF
        self.nProto = (raw_payload[1] >> 5) & 0x7
        self.repMdBits = (raw_payload[1] & 0x3F)
        self.rsvd = (raw_payload[2] >> 2) & 0x3F
        self.d = (raw_payload[2] >> 1) & 0x1
        self.q = raw_payload[2] & 0x1
        self.f = (raw_payload[3] >> 7) & 0x1
        self.hw_id = raw_payload[3] & 0x3F
        self.switch_id = struct.unpack("!I", raw_payload[4:8])[0]
        self.seq_no = struct.unpack("!I", raw_payload[8:12])[0]
        self.ingress_tstamp = struct.unpack("!I", raw_payload[12:16])[0]

# not used
def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

# not used
def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


def extract_ins_00_03(instruction, b):
    if instruction == 0:
        return None
    elif instruction == 10:
        data = {}
        s_id = struct.unpack("!I", b[0:4])[0]
        hop_l = struct.unpack("!I", b[4:8])[0]
        data["switch_id"] = s_id
        data["hop_latency"] = hop_l
        return data
    else:
        return None

def extract_ins_04_07(instruction, b):
    return None

def extract_metadata_stack(b, total_data_len, hop_m_len, instruction_mask_0003, instruction_mask_0407, info):
    numHops = total_data_len // hop_m_len
    info["instruction_mask_0003"] = instruction_mask_0003
    info["instruction_mask_0407"] = instruction_mask_0407
    info["data"] = {}

    i = 0
    for hop in range(numHops, 0, -1):
        offset = i * hop_m_len
        info["data"]["hop_" + str(hop)] = {}
        if instruction_mask_0003 != 0:
            data_0003 = extract_ins_00_03(instruction_mask_0003, b[offset:offset+hop_m_len])
            if data_0003:
                info["data"]["hop_" + str(hop)] = data_0003

        if instruction_mask_0407 != 0:
            data_0407 = extract_ins_04_07(instruction_mask_0407, b[offset:offset+hop_m_len])
            if data_0407:
                info["data"]["hop_" + str(hop)].update(data_0407)

        i += 1

    return info

def get_flow_uuid(conn, info):
    mon_id = ""
    cursor = conn.cursor()

    get_uuid = ("SELECT mon_id "
                "FROM flows "
                "WHERE ip_src=%s AND ip_dst=%s AND ip_proto=%
