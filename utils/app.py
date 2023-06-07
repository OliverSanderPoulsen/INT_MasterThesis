from flask import Flask, request
from run_exercise import x, ExerciseTopo
import json

app = Flask(__name__)

topo = json.load(open('/home/p4/tutorials/exercises/basic/pod-topo/topology.json','r'))

@app.route('/hello/', methods=['GET'])
def hello_name():
    data = request.get_json()
    return topo


print('')
print('Hello! This is the Flask server starting')
print(x)
print(ExerciseTopo.y)
print(topo)
print('')
print('')

if __name__ == '__main__':
    app.run()
