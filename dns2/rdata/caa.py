from . import Rdata
from dns2 import datatypes
from bitstring import ConstBitStream
import typing


class Caa(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.flag = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), int)
            self._tag_length = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), int)
            self.tag = datatypes.BitData(datatypes.CustomStr, datastream.read(f'uint:{8*self._tag_length.value}'), str)
            self.value = datatypes.BitData(datatypes.CustomStr, data[datastream.pos:], str, length_prefix=False)
        elif isinstance(data, dict):
            self.flag = datatypes.BitData(datatypes.int8, data.get('flag'), int)
            # self.tag_length = datatypes.BitData(datatypes.int8, data.get('tag_length'), int)
            self.tag = datatypes.BitData(datatypes.CustomStr, data.get('tag'), str)
            self.value = datatypes.BitData(datatypes.CustomStr, data.get('value'), str, length_prefix=False)

    @property
    def tag_length(self):
        return int(len(self.tag.binary) / 8)
