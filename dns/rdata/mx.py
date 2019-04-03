from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'preference': datatypes.int16,
    'exchange': datatypes.UrlAddress
}

name_length = {
    'preference': 16,
    'exchange': 'REST'
}


class MX(RDATA):
    name_length = name_length
    name_datatype = name_datatype
