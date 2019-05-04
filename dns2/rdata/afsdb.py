from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream


class Afsdb(Rdata):

    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.subtype = datatypes.BitData(datatypes.int16,
                                             data[:16], int)
            datastream = ConstBitStream(bin=data[16:])
            self.hostname = datatypes.BitData(datatypes.DomainName,
                                              datatypes.decode_domain_from_binsting(datastream), str)
        elif isinstance(data, dict):
            self.subtype = datatypes.BitData(datatypes.int16,
                                             data.get('subtype'), int)
            self.hostname = datatypes.BitData(datatypes.DomainName,
                                              data.get('hostname'), str)
