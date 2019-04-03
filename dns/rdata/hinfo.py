from dns import datatypes
from .rdata import RDATA

name_datatype = {
    # TODO how?
    'cpu': datatypes.local_str,
    'os': datatypes.local_str
}

name_length = {
    'cpu': 'DYNAMIC',
    'os': 'REST'
}


class HINFO(RDATA):
    name_length = name_length
    name_datatype = name_datatype
