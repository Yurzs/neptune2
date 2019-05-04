from . import Rdata
from dns2 import datatypes
import typing


class Mx(Rdata):
    def __init__(self, data: typing.Union[dict, dict]):
        if isinstance(data, dict):
            self.preference = datatypes.BitData(datatypes.int16, data.get('preference'), int)
            self.exchange = datatypes.BitData(datatypes.DomainName, data.get('exchange'), str, shortening_allowed=False)
        elif isinstance(data, str):
            self.preference = datatypes.BitData(datatypes.int16, data[:16], int)
            self.exchange = datatypes.BitData(datatypes.DomainName, data[16:], str, shortening_allowed=False)

