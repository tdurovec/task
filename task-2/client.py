import requests
import json

from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config

from typing import List, Dict

import marshmallow as mm


@dataclass
class Ietf_Ip_Ipv4(DataClassJsonMixin):
    ip: str = field(metadata=config(mm_field=mm.fields.Str()), default='')
    netmask: str = field(metadata=config(mm_field=mm.fields.Str()), default='')


@dataclass
class AddressIpv4(DataClassJsonMixin):
    address: List[Ietf_Ip_Ipv4] = field(
        metadata=config(mm_field=mm.fields.List(mm.fields.Nested(Ietf_Ip_Ipv4.schema()))),
        default_factory=list)


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
    ietf_ip_ipv4: AddressIpv4 = field(
        default_factory=AddressIpv4,
        metadata=config(
            mm_field=mm.fields.Nested(
                AddressIpv4.schema(),
                data_key="ietf-ip:ipv4")))

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
