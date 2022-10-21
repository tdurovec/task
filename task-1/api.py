from flask import Flask
import json

class InterfaceAPI(Flask):
    FILE_NAME = "../data.json"

    def __init__(self, import_name):
        super(InterfaceAPI, self).__init__(import_name)
        self.cache = self.read_json(self.FILE_NAME) 

    def read_json(self, file_name):
        with open(file_name) as f:
            data = json.load(f)
            interfaces = data['ietf-interfaces:interfaces']['interface']
            return {interface['name']: interface for interface in interfaces}

app = InterfaceAPI(__name__)
app.config.from_pyfile("configs/flask-app-config.py")


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    debug = True
    app.run(host=host, port=port, debug=debug)