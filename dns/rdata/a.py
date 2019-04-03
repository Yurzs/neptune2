from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'address': datatypes.IpAddress
}

name_length = {
    'address': 32
}


class A(RDATA):
    name_length = name_length
    name_datatype = name_datatype

