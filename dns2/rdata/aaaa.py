from . import Rdata
from dns2 import datatypes
import typing
from bitstring import ConstBitStream, BitArray
from ipaddress import IPv6Address


class Aaaa(Rdata):

    def __init__(self, data: typing.Union[ConstBitStream, dict], **kwargs):
        if isinstance(data, ConstBitStream):
            self.address = datatypes.BitData(IPv6Address, data.read('uint:32'), str,
                                             to_bin_func=lambda x: BitArray(bytes=x.value.packed).bin)
        elif isinstance(data, dict):
            self.address = datatypes.BitData(IPv6Address, data.get('address'), str,
                                             to_bin_func=lambda x: BitArray(bytes=x.value.packed).bin)

