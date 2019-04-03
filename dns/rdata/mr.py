from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'newname': datatypes.UrlAddress
}

name_length = {
    'newname': 'REST'
}


class MR(RDATA):
    name_length = name_length
    name_datatype = name_datatype
