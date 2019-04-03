from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'txt_data': datatypes.local_str
}

name_length = {
    'txt_data': 'REST'
}


class TXT(RDATA):
    name_length = name_length
    name_datatype = name_datatype
