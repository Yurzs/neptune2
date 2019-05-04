from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream

class Tlsa(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.cert_usage = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), str)
            self.selector = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), str)
            self.matching_type = datatypes.BitData(datatypes.int8, datastream.read('uint:8'), str)
            self.certificate_association_data = datatypes.BitData(datatypes.BitMap,
                                                                  data[datastream.pos:], str)
        elif isinstance(data, dict):
            self.cert_usage = datatypes.BitData(datatypes.int8, data.get('cert_usage'), str)
            self.selector = datatypes.BitData(datatypes.int8, data.get('selector'), str)
            self.matching_type = datatypes.BitData(datatypes.int8, data.get('matching_type'), str)
            self.certificate_association_data = datatypes.BitData(datatypes.BitMap,
                                                                  data.get('certificate_association_data'), str)
