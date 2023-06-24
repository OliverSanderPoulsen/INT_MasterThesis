#
from flask import Flask, render_template, request
import requests

import argparse
import json
import os
import sys

import controller_functions
from p4runtime_lib import bmv2, helper, switch, simple_controller
from p4runtime_switch import P4RuntimeSwitch

app = Flask(__name__)

# Define port
flask_Portnumber = 5555
# Define address
flask_Address = '127.0.0.1'

# For testing
topo = json.load(open('/home/p4/tutorials/exercises/basic/pod-topo/topology.json','r'))
hosts = topo['hosts']
switches = topo['switches']

behavioral_exe = 'simple_switch_grpc'
log_dir = '/home/p4/tutorials/INT_MasterThesis/p4-app/logs'
pcap_dir='/home/p4/tutorials/INT_MasterThesis/p4-app/pcaps'
quiet=False
switch_json='build/switch-int.json'
#topo='pod-topo/topology.json'

# grpc ports
s1_grpc_port = P4RuntimeSwitch.next_grpc_port
s2_grpc_port = s1_grpc_port + 1
s3_grpc_port = s2_grpc_port + 1

class Rules():
    sw_conf_file = '/home/p4/tutorials/INT_MasterThesis/p4-app/pod-topo/s1-runtime.json'
    sw_conf = json.load(open((sw_conf_file)))

    workdir = '/home/p4/tutorials/INT_MasterThesis/p4-app'

    p4info_fpath = os.path.join(workdir, sw_conf['p4info'])
    p4info_helper = helper.P4InfoHelper(p4info_fpath)

    proto_dump_fpath = '/home/p4/tutorials/INT_MasterThesis/p4-app/logs/s1-p4runtime-requests.txt'
    address = '127.0.0.1:50051'
    device_id = 0


    s1 = bmv2.Bmv2SwitchConnection('s1', address, device_id, proto_dump_fpath)

    s1.MasterArbitrationUpdate()


    bmv2_json_fpath = os.path.join(workdir, sw_conf['bmv2_json'])

    #print(bmv2_json_fpath)

    s1.SetForwardingPipelineConfig(p4info=p4info_helper.p4info, bmv2_json_file_path=bmv2_json_fpath)
    print('Installed P4 program using SetForwardingPipelineConfig on s1')
    print('------------------')
    print('')
    
    controller_functions.clearAllRules(p4info_helper, s1)


# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle button clicks
@app.route('/modify-flows', methods=['POST'])
def modify_flows():
    # Retrieve data from the POST request
    button_id = request.form.get('button_id')

    # Retrieve data from the POST request
    text_field = request.form.get(button_id+'_text')

    # Buttons should be:
        # Add
            # What type of rules should be possible
        # Remove/Delete
        # Modify

    #/------------------------------------------------------/
    # Forward the request to the Python controller
    # Uncomment when controller API is set up
    #controller_url = 'http://1.2.3.4:9876/modify'
    #payload = {'button_id': button_id}
    #response = requests.post(controller_url, json=payload)

    # Process the response from the controller
    #result = response.json()
    #/------------------------------------------------------/

    # Return the result as a response to the webpage
    return 'Success when pressing '+str(button_id)+'!'+str(text_field)# result

if __name__ == '__main__':
    #print('Server running on '+address+':'+str(portnumber))
    app.run(host=flask_Address, port=flask_Portnumber)
