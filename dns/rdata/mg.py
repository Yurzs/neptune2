from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'mgname': datatypes.UrlAddress,
}

name_length = {
    'mgname': 'REST',
}


class MG(RDATA):
    name_length = name_length
    name_datatype = name_datatype
