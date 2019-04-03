from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'nsdname': datatypes.UrlAddress
}

name_length = {
    'nsdname': 'REST'
}


class NS(RDATA):
    name_length = name_length
    name_datatype = name_datatype
