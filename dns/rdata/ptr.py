from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'ptrname': datatypes.UrlAddress
}

name_length = {
    'ptrname': 'REST'
}


class PRT(RDATA):
    name_length = name_length
    name_datatype = name_datatype
