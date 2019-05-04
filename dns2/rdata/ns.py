from . import Rdata
from dns2 import datatypes
import typing


class Ns(Rdata):
    def __init__(self, data: typing.Union[dict, dict]):
        if isinstance(data, dict):
            self.nsdname = datatypes.BitData(datatypes.DomainName, data.get('nsdname'), str, shortening_allowed=False)
        elif isinstance(data, str):
            self.nsdname = datatypes.BitData(datatypes.DomainName, data, str, shortening_allowed=False)

