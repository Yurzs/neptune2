from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'address': datatypes.Ip6Address
}

name_length = {
    'address': 128
}


class AAAA(RDATA):
    name_length = name_length
    name_datatype = name_datatype
