from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream, BitArray
from ipaddress import IPv4Address


class A(Rdata):

    def __init__(self, data: typing.Union[str, dict]):
        if isinstance(data, str):
            self.address = datatypes.BitData(IPv4Address, data, str,
                                             to_bin_func=lambda x: BitArray(bytes=x.value.packed).bin)
        elif isinstance(data, dict):
            self.address = datatypes.BitData(IPv4Address, data.get('address'), str,
                                             to_bin_func=lambda x: BitArray(bytes=x.value.packed).bin)



