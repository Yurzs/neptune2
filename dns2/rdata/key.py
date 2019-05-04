from . import Rdata
from dns2 import datatypes
import typing


class Key(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.flags = datatypes.BitData(datatypes.int16, data[:16], int)
            self.protocol = datatypes.BitData(datatypes.int8, data[16:24], int)
            self.algorithm = datatypes.BitData(datatypes.int8, data[24:32], int)
            self.public_key = datatypes.BitData(datatypes.CustomStr, data[32:], str)
        elif isinstance(data, dict):
            self.flags = datatypes.BitData(datatypes.int16, data.get('flags'), int)
            self.protocol = datatypes.BitData(datatypes.int8, data.get('protocol'), int)
            self.algorithm = datatypes.BitData(datatypes.int8, data.get('algorithm'), int)
            self.public_key = datatypes.BitData(datatypes.CustomStr, data.get('public_key'), str)
