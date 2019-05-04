from . import Rdata
from dns2 import datatypes
import typing
from bitstring import BitArray
from ipaddress import IPv4Address


class Wks(Rdata):
    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.address = datatypes.BitData(IPv4Address, data[:16], str,
                                             to_bin_func=lambda x: BitArray(bytes=x.value.packed).bin)
            self.protocol = datatypes.BitData(datatypes.int8, data[16:24], int)
            self.bit_map = datatypes.BitData(datatypes.BitMap, data[24:], str)
        elif isinstance(data, dict):
            self.address = datatypes.BitData(IPv4Address, data.get('address'), str,
                                             to_bin_func=lambda x: BitArray(bytes=x.value.packed).bin)
            self.protocol = datatypes.BitData(datatypes.int8, data.get('protocol'), int)
            self.bit_map = datatypes.BitData(datatypes.BitMap, data.get('bit_map'), str)

