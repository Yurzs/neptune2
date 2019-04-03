from dns import datatypes
from .rdata import RDATA

name_datatype = {
    # TODO HELP
    'flags': datatypes.int16,
    'protocol': datatypes.int8,
    'algorithm': datatypes.int8,
    'public_key': datatypes.local_str_without_prefix
}

name_length = {
    'flags': 16,
    'protocol': 8,
    'algorithm': 8,
    'public_key': 'REST'
}


class DNSKEY(RDATA):
    name_length = name_length
    name_datatype = name_datatype
