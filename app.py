from flask import Flask, render_template, jsonify, request
import pickle
from create_pickle import createPickle
import os
import uuid

app = Flask(__name__)

#projects = [{
#    'name': 'my first project',
#    'tasks': [{
#        'name': 'my first task',
#        'completed': False
#    }]
#}]

if os.path.isfile('projects.pickle'):
  with open('projects.pickle', 'rb') as f:
    projects = pickle.load(f)
else:
  createPickle()
  with open('projects.pickle', 'rb') as f:
    projects = pickle.load(f)


@app.route("/")
def home():
  return render_template("index.html.j2", name="Gabor")


@app.route("/projects")
def get_projects():
  return jsonify({'projects': projects}), 200, {
      # add Access-Control-Allow-Origin header
      'Access-Control-Allow-Origin': 'http://127.0.0.1:8080'
  }


@app.route("/project", methods=['POST'])
def create_project():
  request_data = request.get_json()
  new_project_id = uuid.uuid4().hex[:24]
  new_task_id = uuid.uuid4().hex[:24]
  new_checklist_id = uuid.uuid4().hex[:24]
  new_project = {
      'completed':
      request_data['completed'],
      'creation_date':
      request_data['creation_date'],
      'name':
      request_data['name'],
      'project_id':
      new_project_id,
      'tasks': [{
          'checklist': [{
              'checklist_id': new_checklist_id,
              'completed': request_data['completed'],
              'name': request_data['name'],
          }],
          'completed':
          request_data['completed'],
          'name':
          request_data['name'],
          'task_id':
          new_task_id,
      }]
  }
  projects['projects'].append(
      new_project)  # Append to the list instead of the dictionary
  save_data(projects)
  return jsonify({'message':
                  f'project created with id: {new_project_id}'}), 201


def save_data(data):
  with open('projects.pickle', 'wb') as f:
    pickle.dump(data, f)


@app.route("/project/<string:id>")
def get_project(id):
  print(id)
  for project in projects['projects']:
    if project['project_id'] == id:
      return jsonify(project)
  return jsonify({'message': 'project not found'}), 40


@app.route("/project/<string:name>/tasks")
def get_project_tasks(name):
  for project in projects:
    if project['name'] == name:
      return jsonify({'tasks': project['tasks']})
  return jsonify({'message': 'project not found'}), 404


@app.route("/project/<string:name>/task", methods=['POST'])
def add_task_to_project(name):
  request_data = request.get_json()
  for project in projects:
    if 'name' in project and project['name'] == name:
      if 'completed' not in request_data or type(
          request_data['completed']) is not bool:
        return jsonify(
            {'message': 'completed is required and must be a boolean'}), 400
      new_task = {
          'name': request_data['name'],
          'completed': request_data['completed']
      }
      project['tasks'].append(new_task)
      return jsonify(new_task), 201
  return jsonify({'message': 'project not found'}), 404
