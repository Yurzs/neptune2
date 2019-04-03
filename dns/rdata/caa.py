from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'flag': datatypes.int8,
    'tag_length': datatypes.int8,
    'tag': datatypes.local_str_without_prefix,
    'value': datatypes.local_str_without_prefix
}

name_length = {
    'flag': 8,
    'tag_length': 8,
    'tag': ['tag_legth', ],
    'value': 'REST',
}



class CAA(RDATA):
    name_length = name_length
    name_datatype = name_datatype
