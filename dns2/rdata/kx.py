from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream


class Kx(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.preference = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.exchanger = datatypes.BitData(datatypes.DomainName,
                                                datatypes.decode_domain_from_binsting(datastream), str)
        elif isinstance(data, dict):
            self.preference = datatypes.BitData(datatypes.int16, data.get('preference'), int)
            self.exchanger = datatypes.BitData(datatypes.DomainName, data.get('exchanger'), str)
