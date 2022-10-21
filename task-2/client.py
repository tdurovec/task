import requests
import json

from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config

from typing import List, Dict

import marshmallow as mm


@dataclass
class Ietf_Ip_Ipv4(DataClassJsonMixin):
    address: List[Dict[str, str]] = field(
        metadata=config(
            mm_field=mm.fields.List(
                mm.fields.Dict(
                    keys=mm.fields.Str(),
                    values=mm.fields.Str()
            ))),
        default_factory=dict)


@dataclass
class Interface(DataClassJsonMixin):
    name: str = field(metadata=config(mm_field=mm.fields.Str()), default='')
    description: str = field(
        metadata=config(
            mm_field=mm.fields.Str()),
        default='')
    type: str = field(metadata=config(mm_field=mm.fields.Str()), default='')
    enabled: bool = field(
        metadata=config(
            mm_field=mm.fields.Bool()),
        default=False)
    link_up_down_trap_enable: str = field(
        default="", metadata=config(
            field_name="link-up-down-trap-enable"))
    ietf_ip_ipv4: Ietf_Ip_Ipv4 = field(
        default_factory=Ietf_Ip_Ipv4,
        metadata=config(
            field_name="ietf-ip:ipv4",
            mm_field=mm.fields.Nested(
                Ietf_Ip_Ipv4.schema())))


@dataclass
class Interfaces(DataClassJsonMixin):
    interfaces: List[Interface] = field(
        metadata=config(
            mm_field=mm.fields.List(
                mm.fields.Nested(
                    Interface.schema()))))


class InterfaceManager:
    API = "http://127.0.0.1:5000"

    def __init__(self):
        self.AllInterfacesURL = self.API + "/get-all-interfaces/"

    def get_all_interfaces(self) -> List[Dict]:
        data = requests.get(self.AllInterfacesURL)
        return data.json()

    def write_all_interfaces(self, classes_list: List[Interface]) -> None:
        data = list(map(lambda x: x.to_dict(), classes_list))
        with open("client_data.json", "w") as fp:
            json.dump(data, fp, indent=2)


def main():
    interface_manager = InterfaceManager()
    interfaces = interface_manager.get_all_interfaces()

    list_of_dataclass_interface = Interfaces.from_json(
        Interfaces(interfaces).to_json()).interfaces
    interface_manager.write_all_interfaces(list_of_dataclass_interface)


if __name__ == "__main__":
    main()
