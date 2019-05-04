from . import Rdata
from dns2 import datatypes
import typing



class Dname(Rdata):
    def __init__(self, data: typing.Union[dict, dict]):
        if isinstance(data, dict):
            self.target = datatypes.BitData(datatypes.DomainName, data.get('dname'), str)
        elif isinstance(data, str):
            self.target = datatypes.BitData(datatypes.DomainName, data, str)
