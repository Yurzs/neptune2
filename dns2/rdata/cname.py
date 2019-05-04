from . import Rdata
from dns2 import datatypes
import typing
# from bitstring import ConstBitStream, BitArray


class Cname(Rdata):
    def __init__(self, data: typing.Union[dict, dict]):
        if isinstance(data, dict):
            self.cname = datatypes.BitData(datatypes.DomainName, data.get('cname'), str, shortening_allowed=False)
        elif isinstance(data, str):
            self.cname = datatypes.BitData(datatypes.DomainName, data, str, shortening_allowed=False)

