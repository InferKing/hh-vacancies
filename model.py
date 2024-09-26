import json


class Model:
    def __init__(self):
        self.data = {}

    def load(self, path):
        with open(path, 'r') as f:
            self.data = json.load(f)
    
    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.data, f)