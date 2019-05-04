from . import Rdata
from dns2 import datatypes
from bitstring import ConstBitStream
import typing


class Loc(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.version = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), int)
            self.size = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), int)
            self.horiz_pre = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), int)
            self.vert_pre = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), int)
            self.lattitude = datatypes.BitData(datatypes.int32, datastream.read('int:32'), int)
            self.longtitude = datatypes.BitData(datatypes.int32, datastream.read('int:32'), int)
            self.altitude = datatypes.BitData(datatypes.int32, datastream.read('int:32'), int)
        elif isinstance(data, dict):
            self.version = datatypes.BitData(datatypes.int8, data.get('version'), int)
            self.size = datatypes.BitData(datatypes.int8, data.get('size'), int)
            self.horiz_pre = datatypes.BitData(datatypes.int8, data.get('horiz_pre'), int)
            self.vert_pre = datatypes.BitData(datatypes.int8, data.get('vert_pre'), int)
            self.latitude = datatypes.BitData(datatypes.int32, data.get('latitude'), int)
            self.longitude = datatypes.BitData(datatypes.int32, data.get('longitude'), int)
            self.altitude = datatypes.BitData(datatypes.int32, data.get('altitude'), int)
