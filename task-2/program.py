import json

from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config

from typing import List, Dict

import marshmallow as mm

file_name = "data.json"

with open(file_name) as fp:
    data = json.load(fp)
    interfaces = data['ietf-interfaces:interfaces']['interface']

@dataclass
class Interface(DataClassJsonMixin):
    name: str = ""
    # description: str = ""
    # type: str = ""
    # enabled: bool = False
    # link_up_down_trap_enable: str = field(default="", metadata=config(field_name="link-up-down-trap-enable"))
    # ietf_ip_ipv4: Dict[str, List[Dict[str, str]]] = field(
    #     default_factory=Dict, 
    #                 metadata=config(
    #                         field_name="ietf-ip:ipv4",
    #                         mm_field=mm.fields.Dict(
    #                             key=mm.fields.Str(),
    #                             values=mm.fields.List(
    #                                 mm.fields.Dict(
    #                                     keys=mm.fields.Str(),
    #                                     values=mm.fields.Str()
    #                                 )
    #                             ),
    #                         )
    #                     )
    #                 )

@dataclass
class Interfaces(DataClassJsonMixin):
    interfaces: List[Interface] = field(metadata=config(mm_field=mm.fields.List(mm.fields.Nested(Interface.schema()))))


data = Interfaces.from_json(Interfaces(interfaces).to_json()).interfaces

print(data)




# print(res.interfaces)
# print(type(res.interfaces))

# for i in res:
#     print(i.to_json())
#     print(type(i))