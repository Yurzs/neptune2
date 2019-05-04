from . import Rdata
from dns2 import datatypes
import typing
from ipaddress import IPv4Address, IPv6Interface


class Ptr(Rdata):

    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.ptrdname = datatypes.BitData(datatypes.DomainName, data, str)
        elif isinstance(data, dict):
            self.ptrdname = datatypes.BitData(datatypes.DomainName, data.get('ptrdname'), str)

