from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream


class Tkey(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.algorithm = datatypes.BitData(datatypes.DomainName,
                                               datatypes.decode_domain_from_binsting(datastream), str)
            self.inception = datatypes.BitData(datatypes.int32, datastream.read('uint:32'), int)
            self.expiration = datatypes.BitData(datatypes.int32, datastream.read('uint:32'), int)
            self.mode = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.error = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.key_size = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.key_data = datatypes.BitData(datatypes.CustomStr,
                                              datatypes.CustomStr.read_prefixed(datastream.read('uint:16')).value, int,
                                              length_prefix=False)
            self.other_size = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.other_data = datatypes.BitData(datatypes.CustomStr,
                                                datatypes.CustomStr.read_prefixed(datastream).value, int,
                                                length_prefix=False)
        elif isinstance(data, dict):
            self.algorithm = datatypes.BitData(datatypes.DomainName, data.get('algorithm'), str)
            self.inception = datatypes.BitData(datatypes.int32, data.get('inception'), int)
            self.expiration = datatypes.BitData(datatypes.int32, data.get('expiration'), int)
            self.mode = datatypes.BitData(datatypes.int16, data.get('mode'), int)
            self.error = datatypes.BitData(datatypes.int16, data.get('error'), int)
            self.key_size = datatypes.BitData(datatypes.int16, data.get('key_size'), int)
            self.key_data = datatypes.BitData(datatypes.CustomStr, data.get('key_data'), int, length_prefix=False)
            self.other_size = datatypes.BitData(datatypes.int16, data.get('other_size'), int)
            self.other_data = datatypes.BitData(datatypes.CustomStr, data.get('other_data'), int, length_prefix=False)

