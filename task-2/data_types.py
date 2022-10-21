from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config
import marshmallow as mm

from typing import List

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