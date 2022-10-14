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
            data = json.load(f)
            interfaces = data['ietf-interfaces:interfaces']['interface']
            return {interface['name']: interface for interface in interfaces}

app = InterfaceAPI(__name__)

@app.route('/get-all-interfaces/', methods=["GET"])
def view_all_interfaces():
    if interfaces := app.cache.values():
        return jsonify(list(interfaces)), http.HTTPStatus.OK
    return http.HTTPStatus.NOT_FOUND

@app.route('/get-all-interfaces/', methods=["HEAD"])
def view_all_interfaces_head():
    if interfaces := app.cache.values():
        return http.HTTPStatus.OK
    return http.HTTPStatus.NOT_FOUND

@app.route('/get-interface/<path:interface_name>', methods=["GET"])
def view_interface_by_name(interface_name):
    if interface := app.cache.get(interface_name):
        return jsonify(interface), http.HTTPStatus.OK
    return jsonify({"info": "interface not found"}), http.HTTPStatus.NOT_FOUND
    
@app.route('/get-interface/<path:interface_name>', methods=["HEAD"])
def view_interface_by_name_head(interface_name):
    if interface := app.cache.get(interface_name):
        return http.HTTPStatus.OK
    return http.HTTPStatus.NOT_FOUND

@app.route('/get-interfaces/', methods=["POST"])
def view_filtered_interface():
    interfaces = app.cache
    filtered_interfaces_list = []

    data = request.get_json()
    interfaces_option = data.get('input', {}).get('interfaces', [])[0]

    option_name = interfaces_option.get('name')
    option_type = interfaces_option.get('type')
    option_enabled = interfaces_option.get('enabled')

    if (interface_by_name := interfaces.get(option_name)is not None) and \
        (interface_by_name.get('type') == option_type or option_type is None) and \
        (interface_by_name.get('enabled') == option_enabled or option_enabled is None):
            filtered_interfaces_list.append(interface_by_name)
    else:
        for interface in interfaces.values():
            if (option_name is None or option_name == interface.get('name')) and \
                (option_enabled is None or option_enabled == interface.get('enabled')) and \
                (option_type is None or option_type == interface.get('type')):
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
    if delete_interface := app.cache.pop(interface_name, None):
        return jsonify({"info":f"{interface_name} was deleted"}), http.HTTPStatus.OK
    return jsonify({"info":f"{interface_name} was not found to deleted"}), http.HTTPStatus.NOT_FOUND
