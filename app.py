from flask import Flask, render_template, jsonify, request
import pickle
from create_pickle import createPickle
import os
import uuid
from filter import filter_list_of_dicts

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
  try:
    request_data = request.get_json()
    return jsonify({
        'projects':
        filter_list_of_dicts(projects['projects'], request_data['fields'])
    }), 200
  except:
    return jsonify(projects), 200


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


@app.route("/project/<string:id>/complete")
def set_project_complete(id):
  print(id)
  for project in projects['projects']:
    if project['project_id'] == id:
      if project['completed'] == True:
        return jsonify(''), 200
      else:
        project['completed'] = True
        return jsonify(project)
  return jsonify({'message': 'project not found'}), 404


@app.route("/project/<string:name>/tasks")
def get_project_tasks(name):
  try:
    request_data = request.get_json()
    for project in projects['projects']:
      if project['name'] == name:
        return jsonify({
            'tasks':
            filter_list_of_dicts(project['tasks'], request_data['fields'])
        })

    return jsonify({'message': 'project not found'}), 404
  except:
    for project in projects['projects']:
      if project['name'] == name:
        return jsonify({'tasks': project['tasks']})
    return jsonify({'message': 'project not found'}), 404


@app.route("/project/<string:id>/task", methods=['POST'])
def add_task_to_project(id):
  request_data = request.get_json()
  new_task_id = uuid.uuid4().hex[:24]
  new_checklist_id = uuid.uuid4().hex[:24]
  for project in projects['projects']:
    if project['project_id'] == id:
      if type(request_data['completed']) is not bool:
        return jsonify(
            {'message': 'completed is required and must be a boolean'}), 400
      new_task = {
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
      }
      project['tasks'].append(new_task)
      save_data(projects)
      return jsonify({'message': f'task created with id: {new_task_id}'}), 201
  return jsonify({'message': 'project not found'}), 404
