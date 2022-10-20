import requests
import json

from dataclasses import dataclass, field, asdict
from dataclasses_json import DataClassJsonMixin, config

from typing import List, Dict

import marshmallow as mm


@dataclass
class Interface(DataClassJsonMixin):
    name: str = ""
    description: str = ""
    type: str = ""
    enabled: bool = False
    link_up_down_trap_enable: str = field(default="", metadata=config(field_name="link-up-down-trap-enable"))
    ietf_ip_ipv4: Dict[str, List[Dict[str, str]]] = field(default_factory=Dict, 
                    metadata=config(
                            field_name="ietf-ip:ipv4",
                            mm_field=mm.fields.Dict(
                                key=mm.fields.Str(),
                                values=mm.fields.List(
                                    mm.fields.Dict(
                                        keys=mm.fields.Str(),
                                        values=mm.fields.Str()
                                    )
                                ),
                            )
                        )
                    )

    def dict(self):
        dct = {}
        for k, v in asdict(self).items():
            if (k=="description" and v == ""):
                continue
            dct[k] = v

        return dct

@dataclass
class Interfaces(DataClassJsonMixin):
    interfaces: List[Interface] = field(metadata=config(mm_field=mm.fields.List(mm.fields.Nested(Interface.schema()))))

class InterfaceManager:
    API = "http://127.0.0.1:5000"

    def __init__(self):
        self.AllInterfacesURL = self.API + "/get-all-interfaces/"

    def get_all_interfaces(self):
        data = requests.get(self.AllInterfacesURL)
        return data.json()

    def write_all_interfaces(self, class_data: List):
        # dict is in data_class interface
        data = [i.dict() for i in class_data]
        with open("client_data.json", "w") as fp:
            json.dump(data, fp, indent=2)

def main():
    interface_manager = InterfaceManager()
    interfaces = interface_manager.get_all_interfaces()

    # interfaces to dataclass and write in separate file

    list_of_dataclass_interface = Interfaces.from_json(Interfaces(interfaces).to_json()).interfaces
    interface_manager.write_all_interfaces(list_of_dataclass_interface)



if __name__ == "__main__":
    main()

