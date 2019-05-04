from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream


class Ds(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.key_tag = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.algorithm = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), int)
            self.digest_type = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), int)
            self.digest = datatypes.BitData(datatypes.CustomStr, data[datastream.pos:], str, length_prefix=False)
        elif isinstance(data, dict):
            self.key_tag = datatypes.BitData(datatypes.int16, data.get('key_tag'), int)
            self.algorithm = datatypes.BitData(datatypes.int8, data.get('algorithm'), int)
            self.digest_type = datatypes.BitData(datatypes.int8, data.get('digest_type'), int)
            self.digest = datatypes.BitData(datatypes.CustomStr, data.get('digest'), str, length_prefix=False)
