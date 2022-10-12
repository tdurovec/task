from flask import Flask, jsonify, request
import json


class InterfaceAPI(Flask):
    def __init__(self, import_name):
        super(InterfaceAPI, self).__init__(import_name)

app = InterfaceAPI(__name__)

def get_all_interfaces():
    io = open("data.json","r")
    string = io.read()
    dictionary = json.loads(string)
    io.close()
    return dictionary['ietf-interfaces:interfaces']['interface']

FILTERED_OPTIONS = ["name", "type", "enabled"]
interfaces = get_all_interfaces()

@app.route('/get-all-interfaces/', methods=["GET"])
def view_all_interfaces():
    return jsonify(interfaces)

@app.route('/get-all-interfaces/', methods=["HEAD"])
def view_all_interfaces_head():
    if interfaces != []:
        return jsonify({"success":f"{len(interfaces)} interfaces"})
    return jsonify({"error":"empty"})

@app.route('/get-interface', methods=["GET"])
def view_interface_by_name():
    interface_name = request.args.get('name')

    for interface in interfaces:
        if interface['name'] == interface_name:
            return jsonify(interface)

    return jsonify({"error": "interface not found"})

def validation(option, value):
    for key in option:
        if not(value[key] == option[key]):
            return False
    return True

@app.route('/get-interfaces/', methods=["POST"])
def view_filtered_interface():
    filtered_interfaces_list = []

    if not(request.method == 'POST'):
        return jsonify({"error":"allow only POST request"})

    data = request.get_json()

    for key in data:
        try:
            valid = data[key]['interfaces']
            valid = valid[0]
        except:
            return jsonify({"error":"input is incorrect"})

        for value in valid:
            if value not in FILTERED_OPTIONS:
                return jsonify({"error":"incorrect filtered option"})
        
        for interface in interfaces:
            if validation(valid, interface):
                filtered_interfaces_list.append(interface)

    return jsonify(filtered_interfaces_list)

@app.route('/refresh-interfaces/', methods=["POST"])
def refresh_all_interfaces():
    interfaces = get_all_interfaces()
    return jsonify({"success":"refreshed"})

@app.route('/delete-interface', methods=["DELETE"])
def delete_interface(interface_name):
    interface_name = request.args.get('name')
    
    for idx, interface in enumerate(interfaces.copy()):
        if interface['name'] == interface_name:
            interfaces.pop(idx)
            return jsonify({"success":"interface deleted"})

    return jsonify({"error":"interface not found"})
