from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream

class Mr(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.newname = datatypes.BitData(datatypes.DomainName,
                                             datatypes.decode_domain_from_binsting(datastream), str)
        elif isinstance(data, dict):
            self.newname = datatypes.BitData(datatypes.DomainName, data.get('newname'), str)
