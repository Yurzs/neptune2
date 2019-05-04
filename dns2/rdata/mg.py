from . import Rdata
from dns2 import datatypes
from bitstring import ConstBitStream
import typing


class Mg(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.madname = datatypes.BitData(datatypes.DomainName,
                                             datatypes.decode_domain_from_binsting(datastream), str)
        elif isinstance(data, dict):
            self.madname = datatypes.BitData(datatypes.DomainName, data.get('madname'), str)
