def writeForwardRules(p4info_helper,ingress_sw,
    dst_eth_addr,port,dst_ip_addr):
    """
        Install rules:

        做到原本 sx-runtime.json 的工作
            p4info_helper:  the P4Info helper
            ingress_sw:     the ingress switch connection
            dst_eth_addr:   the destination IP to match in the ingress rule
            port:           port of switch
            dst_ip_addr:    the destination Ethernet address to write in the egress rule
    """

    # 1. Ingress rule
    table_entry = p4info_helper.buildTableEntry(
        table_name="Basic_ingress.ipv4_lpm",
        match_fields={
            "hdr.ipv4.dstAddr": (dst_ip_addr,32)
        },
        action_name="Basic_ingress.ipv4_forward",
        action_params={
            "dstAddr": dst_eth_addr,
            "port": port
        })
    # write into ingress of target sw
    ingress_sw.WriteTableEntry(table_entry)
    print "Installed ingress forward rule on %s" % ingress_sw.name

def modifyForwardRules(p4info_helper, ingress_sw,
    dst_eth_addr, port, dst_ip_addr):
    """
        Modify Rules
    """
    table_entry = p4info_helper.buildTableEntry(
        table_name="Basic_ingress.ipv4_lpm",
        match_fields={
            "hdr.ipv4.dstAddr": (dst_ip_addr, 32)
        },
        action_name="Basic_ingress.ipv4_forward",
        action_params={
            "dstAddr": dst_eth_addr,
            "port": port
        })
    ingress_sw.ModifyTableEntry(table_entry)
    print "Modified ingress forward rule on %s" % ingress_sw.name

def deleteForwardRules(p4info_helper, ingress_sw,
    dst_eth_addr, port, dst_ip_addr):
    """
        Delete Rules
    """
    table_entry = p4info_helper.buildTableEntry(
        table_name="Basic_ingress.ipv4_lpm",
        match_fields={
            "hdr.ipv4.dstAddr": (dst_ip_addr, 32)
        },
        action_name="Basic_ingress.ipv4_forward",
        action_params={
            "dstAddr": dst_eth_addr,
            "port": port
        })
    ingress_sw.DeleteTableEntry(table_entry)
    print "Deleted ingress forward rule on %s" % ingress_sw.name

def clearAllRules(p4info_helper, sw):
    print '\n----- Clear all table rules for %s -----' % sw.name
    # fetch all response
    for response in sw.ReadTableEntries():
        for entity in response.entities:
            entry = entity.table_entry
            # delete this entry
            sw.DeleteTableEntry(entry)
            print "Delete ingress forward rule on %s" % sw.name

def readTableRules(p4info_helper, sw):
    """
        Reads the table entries from all tables on the switch.
        Args:
            p4info_helper:  the P4Info helper
            sw:             the switch connection
    """
    print '\n----- Reading table rules for %s ------' % sw.name
    for response in sw.ReadTableEntries():
        for entity in response.entities:
            entry = entity.table_entry
            # TOOD:
            # use the p4info_helper to translate the IDs in the entry to names
            table_name = p4info_helper.get_tables_name(entry.table_id)
            print '%s: ' % table_name,
            for m in entry.match:
                print p4info_helper.get_match_field_name(table_name, m.field_id)
                print '%r' % (p4info_helper.get_match_field_value(m),),
            action = entry.action.action
            action_name = p4info_helper.get_actions_name(action.action_id)
            print '->', action_name,
            for p in action.params:
                print p4info_helper.get_action_param_name(action_name, p.param_id),
                print '%r' % p.value
            print
