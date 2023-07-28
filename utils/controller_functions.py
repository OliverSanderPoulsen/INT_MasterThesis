#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import grpc
import os
import sys
from time import sleep

# set our lib path
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../utils/")
)
# And then we import
import p4runtime_lib.bmv2
import p4runtime_lib.helper
from p4runtime_lib.switch import ShutdownAllSwitchConnections

def writeForwardRules(p4info_helper, ingress_sw, dst_eth_addr, port, dst_ip_addr):
    """
        Install rules:
        Do the work originally in sx-runtime.json
        p4info_helper: the P4Info helper
        ingress_sw: the ingress switch connection
        dst_eth_addr: the destination IP to match in the ingress rule
        port: port of switch
        dst_ip_addr: the destination Ethernet address to write in the egress rule
    """
    # 1. Ingress rule
    table_entry = p4info_helper.buildTableEntry(
        table_name="Basic_ingress.ipv4_lpm",
        match_fields={"hdr.ipv4.dstAddr": (dst_ip_addr, 32)},
        action_name="Basic_ingress.ipv4_forward",
        action_params={"dstAddr": dst_eth_addr, "port": port},
    )
    # write into ingress of target sw
    ingress_sw.WriteTableEntry(table_entry)
    print(f"Installed ingress forward rule on {ingress_sw.name}")

def modifyForwardRules(p4info_helper, ingress_sw, dst_eth_addr, port, dst_ip_addr):
    """
        Modify Rules
    """
    table_entry = p4info_helper.buildTableEntry(
        table_name="Basic_ingress.ipv4_lpm",
        match_fields={"hdr.ipv4.dstAddr": (dst_ip_addr, 32)},
        action_name="Basic_ingress.ipv4_forward",
        action_params={"dstAddr": dst_eth_addr, "port": port},
    )
    ingress_sw.ModifyTableEntry(table_entry)
    print(f"Modified ingress forward rule on {ingress_sw.name}")

def deleteForwardRules(p4info_helper, ingress_sw, dst_eth_addr, port, dst_ip_addr):
    """
        Delete Rules
    """
    table_entry = p4info_helper.buildTableEntry(
        table_name="Basic_ingress.ipv4_lpm",
        match_fields={"hdr.ipv4.dstAddr": (dst_ip_addr, 32)},
        action_name="Basic_ingress.ipv4_forward",
        action_params={"dstAddr": dst_eth_addr, "port": port},
    )
    ingress_sw.DeleteTableEntry(table_entry)
    print(f"Deleted ingress forward rule on {ingress_sw.name}")

def clearAllRules(p4info_helper, sw):
    print(f"\n----- Clear all table rules for {sw.name} -----")
    # fetch all response
    for response in sw.ReadTableEntries():
        for entity in response.entities:
            entry = entity.table_entry
            # delete this entry
            sw.DeleteTableEntry(entry)
            print(f"Delete ingress forward rule on {sw.name}")

def readTableRules(p4info_helper, sw):
    """
        Reads the table entries from all tables on the switch.
        Args:
            p4info_helper: the P4Info helper
            sw: the switch connection
    """
    print(f"\n----- Reading table rules for {sw.name} ------")
    for response in sw.ReadTableEntries():
        for entity in response.entities:
            entry = entity.table_entry
