#
from flask import Flask, render_template, request
import requests
import json
from run_exercise import x, ExerciseTopo

app = Flask(__name__)

# Define port
portnumber = 5555
# Define address
address = '127.0.0.1'


# For testing
topo = json.load(open('/home/p4/tutorials/exercises/basic/pod-topo/topology.json','r'))


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
    print('Server running on '+address+':'+str(portnumber))
    app.run(host=address, port=portnumber)
