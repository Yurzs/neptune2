from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'address': datatypes.IpAddress,
    'protocol': datatypes.int8,
    'bitmap': datatypes.UrlAddress
}

name_length = {
    'address': 4,
    'protocol': 8,
    'bitmap': 'REST'
}


class WKS(RDATA):
    name_length = name_length
    name_datatype = name_datatype
