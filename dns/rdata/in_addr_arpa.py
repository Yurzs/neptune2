from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'address': datatypes.local_str,
}

name_length = {
    'address': 'REST',
}


class IN_ADDR_ARPA(RDATA):
    name_length = name_length
    name_datatype = name_datatype
