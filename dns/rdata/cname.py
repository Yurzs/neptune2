from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'cname': datatypes.UrlAddress
}

name_length = {
    'cname': 'REST'
}


class CNAME(RDATA):
    name_length = name_length
    name_datatype = name_datatype
