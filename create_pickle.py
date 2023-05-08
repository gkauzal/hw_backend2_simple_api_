import json
import pickle


def createPickle():

  with open('projects.json') as f:
    data = json.load(f)

  with open('projects.pickle', 'wb') as f:
    pickle.dump(data, f)