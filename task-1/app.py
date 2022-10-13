from flask import Flask, jsonify, request
import json
import http

class InterfaceAPI(Flask):

    FILE_NAME = "data.json"
    FILTERED_OPTIONS = ["name", "type", "enabled"]

    def __init__(self, import_name):
        super(InterfaceAPI, self).__init__(import_name)
        self.cache = self.read_json(self.FILE_NAME) 

    def read_json(self, file_name):
        with open(file_name) as f:
            data = json.loads(f.read())
            interfaces = data['ietf-interfaces:interfaces']['interface']
            return {interface['name']: interface for interface in interfaces}

app = InterfaceAPI(__name__)

@app.route('/get-all-interfaces/', methods=["GET"])
def view_all_interfaces():
    interfaces = app.cache.values()
    if interfaces:
        return jsonify(list(interfaces)), http.HTTPStatus.OK
    return http.HTTPStatus.NOT_FOUND

@app.route('/get-all-interfaces/', methods=["HEAD"])
def view_all_interfaces_head():
    interfaces = app.cache.values()
    if interfaces:
        return http.HTTPStatus.OK
    return http.HTTPStatus.NOT_FOUND

@app.route('/get-interface/<path:interface_name>', methods=["GET"])
def view_interface_by_name(interface_name):
    interface = app.cache.get(interface_name)
    if interface:
        return jsonify(interface), http.HTTPStatus.OK
    return jsonify({"info": "interface not found"}), http.HTTPStatus.NOT_FOUND
    
@app.route('/get-interface/<path:interface_name>', methods=["HEAD"])
def view_interface_by_name_head(interface_name):
    interface = app.cache.get(interface_name)
    if interface:
        return http.HTTPStatus.OK
    return http.HTTPStatus.NOT_FOUND

def validation(option, value):
    for item in option:
        key = list(item.keys())[0]
        if not(item[key] == value[key]):
            return False
    return True

@app.route('/get-interfaces/', methods=["POST"])
def view_filtered_interface():
    interfaces = app.cache.values()
    filtered_interfaces_list = []

    if not(request.method == 'POST'):
        return jsonify({"error":"allow only POST request"}), http.HTTPStatus.BAD_REQUEST

    data = request.get_json()

    for key in data:
        interfaces_option = data.get(key, {}).get('interfaces',[])

        if interfaces_option == []:
            return jsonify({"info": "interfaces not found"}), http.HTTPStatus.NOT_FOUND

        for value in interfaces_option:
            current_key = list(value.keys())[0]
            if current_key not in app.FILTERED_OPTIONS:
                return jsonify({"error":"incorrect filtered option"}), http.HTTPStatus.NOT_FOUND

        for interface in interfaces:
            if validation(interfaces_option, interface):
                filtered_interfaces_list.append(interface)

    return jsonify(filtered_interfaces_list), http.HTTPStatus.OK

@app.route('/refresh-interfaces/', methods=["POST"])
def refresh_all_interfaces():
    app.cache = app.read_json(app.FILE_NAME)
    if app.cache:
        return jsonify({"info":"refreshed"}), http.HTTPStatus.OK
    return jsonify({"info":"not refreshed"}), http.HTTPStatus.BAD_REQUEST

@app.route('/delete-interface/<path:interface_name>', methods=["DELETE"])
def delete_interface(interface_name):
    delete_interface = app.cache.pop(interface_name, None)
    if delete_interface:
        return jsonify({"info":f"{interface_name} was deleted"}), http.HTTPStatus.OK
    return jsonify({"info":f"{interface_name} was not found to deleted"}), http.HTTPStatus.NOT_FOUND

