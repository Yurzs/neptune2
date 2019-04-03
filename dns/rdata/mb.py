from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'madname': datatypes.UrlAddress
}

name_length = {
    'madname': 'REST'
}


class MB(RDATA):
    name_length = name_length
    name_datatype = name_datatype
