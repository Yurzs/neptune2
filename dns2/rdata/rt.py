from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream

class Rt(Rdata):

    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.preference = datatypes.BitData(datatypes.int16, data[:16], int)
            datastream = ConstBitStream(bin=data[16:])
            self.intermediate_host = datatypes.BitData(datatypes.DomainName,
                                                       datatypes.decode_domain_from_binsting(datastream),
                                                       str)
        elif isinstance(data, dict):
            self.preference = datatypes.BitData(datatypes.int16, data.get('preference'), int)
            self.intermediate_host = datatypes.BitData(datatypes.DomainName,
                                                       data.get('intermediate_host'),
                                                       str)

