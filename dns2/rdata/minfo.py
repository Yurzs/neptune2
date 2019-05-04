from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream


class Minfo(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.rmailbx = datatypes.BitData(datatypes.DomainName,
                                             datatypes.decode_domain_from_binsting(datastream), str)
            self.emailbx = datatypes.BitData(datatypes.DomainName,
                                             datatypes.decode_domain_from_binsting(datastream), str)
        elif isinstance(data, dict):
            self.rmailbx = datatypes.BitData(datatypes.DomainName, data.get('rmailbx'), str)
            self.emailbx = datatypes.BitData(datatypes.DomainName, data.get('emailbx'), str)
