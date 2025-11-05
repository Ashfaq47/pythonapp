from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
# Allow our frontend to talk to our backend
CORS(app)

# Connect to our MongoDB container. 
# We use the service name 'db' from our docker-compose file.
client = MongoClient('mongodb://db:27017/')
db = client.tododb # Create a database named 'tododb'

# This is the endpoint for getting all tasks and adding a new one
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        # Add a new task
        task = request.json
        db.tasks.insert_one({'description': task['description']})
        return jsonify({'status': 'Task added!'})
    else:
        # Get all tasks
        tasks = []
        for task in db.tasks.find():
            tasks.append({'description': task['description']})
        return jsonify(tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
