from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream


class Hinfo(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.cpu = datatypes.BitData(datatypes.CustomStr, datatypes.CustomStr.read_prefixed(datastream).value, str)
            self.os = datatypes.BitData(datatypes.CustomStr, datatypes.CustomStr.read_prefixed(datastream).value, str)
        elif isinstance(data, dict):
            self.cpu = datatypes.BitData(datatypes.CustomStr, data.get('cpu'), str)
            self.os = datatypes.BitData(datatypes.CustomStr, data.get('os'), str)
