import requests
import json

from data_types import Interface, mm
from typing import List
from typing import Dict

class InterfaceManager:
    API = "http://127.0.0.1:5000"

    def __init__(self):
        self.AllInterfacesURL = self.API + "/get-all-interfaces/"

    def get_all_interfaces(self) -> List[Dict]:
        data = requests.get(self.AllInterfacesURL)
        return data.json()

    def write_all_interfaces(self, data: List[Dict]) -> None:
        with open("client_data.json", "w") as fp:
            json.dump(data, fp, indent=2)


def main():
    interface_manager = InterfaceManager()
    interfaces = interface_manager.get_all_interfaces()

    interfaces = Interface.schema().load(interfaces, many=True, unknown=mm.EXCLUDE)
    json_interfaces = Interface.schema().dump(interfaces, many=True)
    interface_manager.write_all_interfaces(json_interfaces)


if __name__ == "__main__":
    main()
