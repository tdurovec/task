from email.policy import default
import json

from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config

from typing import List, Dict, Tuple

import marshmallow as mm

file_name = "data.json"

with open(file_name) as fp:
    data = json.load(fp)
    interfaces = data['ietf-interfaces:interfaces']['interface']

#https://app.quicktype.io/
# @dataclass
# class IETFIPIpv6Address(DataClassJsonMixin):
#     ip: str
#     prefix_length: int


# @dataclass
# class IETFIPIpv6(DataClassJsonMixin):
#     address: List[IETFIPIpv6Address]



@dataclass
class IETFIPIpv4Address(DataClassJsonMixin):
    ip: str = ""
    netmask: str = ""


@dataclass
class IETFIPIpv4(DataClassJsonMixin):
    address: str = ""


@dataclass
class Interface(DataClassJsonMixin):
    name: str 
    # description: str = ""
    # type: str = ""
    # enabled: bool = False
    link_up_down_trap_enable: str = field(metadata=config(field_name="link-up-down-trap-enable"))


    ietf_ip_ipv4: Dict[str, List[Dict[str, str]]] = field(metadata=config(
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

    ietf_ip_ipv6: Dict[str, List[Dict[str, str]]] = field(metadata=config(
                            field_name="ietf-ip:ipv6",
                            mm_field=mm.fields.Dict(
                                key=mm.fields.Str(),
                                values=mm.fields.List(
                                    mm.fields.Dict(
                                        keys=mm.fields.Str(),
                                        values=mm.fields.Str()
                                    ),
                                ),
                            )
                        )
                    )

@dataclass
class Interfaces(DataClassJsonMixin):
    interfaces: List[Interface] = field(metadata=config(mm_field=mm.fields.List(mm.fields.Nested(Interface.schema()))))

data = Interfaces(interfaces=interfaces)

res = Interfaces.from_json(data.to_json())

print(res)

