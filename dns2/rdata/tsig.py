from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream

class Tsig(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            datastream = ConstBitStream(bin=data)
            self.algorithm_name = datatypes.BitData(datatypes.DomainName,
                                                    datatypes.decode_domain_from_binsting(datastream), str)
            self.time_signed = datatypes.BitData(datatypes.int48, datastream.read('uint:48'), int)
            self.fudge = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.mac_size = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.mac = datatypes.BitData(datatypes.CustomStr,
                                         datastream.read(f'uint:{self.mac_size.value}'), str, length_prefix=False)
            self.original_id = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.error = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.other_len = datatypes.BitData(datatypes.int16, datastream.read('uint:16'), int)
            self.other = datatypes.BitData(datatypes.CustomStr,
                                           datastream.read(f'uint:{self.other_len.value}'), int, length_prefix=False)
        elif isinstance(data, dict):
            self.algorithm_name = datatypes.BitData(datatypes.DomainName, data.get('algorithm_name'), str)
            self.time_signed = datatypes.BitData(datatypes.int48, data.get('time_signed'), int)
            self.fudge = datatypes.BitData(datatypes.int16, data.get('fudge'), int)
            self.mac_size = datatypes.BitData(datatypes.int16, data.get('mac_size'), int)
            self.mac = datatypes.BitData(datatypes.CustomStr, data.get('mac'), str, length_prefix=False)
            self.original_id = datatypes.BitData(datatypes.int16, data.get('original_id'), int)
            self.error = datatypes.BitData(datatypes.int16, data.get('error'), int)
            self.other_len = datatypes.BitData(datatypes.int16, data.get('other_len'), int)
            self.other = datatypes.BitData(datatypes.CustomStr, data.get('other'), int, length_prefix=False)
