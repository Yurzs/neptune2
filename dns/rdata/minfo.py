from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'rmailbx': datatypes.UrlAddress,
    'emailbx': datatypes.UrlAddress
}

name_length = {
    'rmailbx': 'DYNAMIC',
    'emailbx': 'REST'
}


class MINFO(RDATA):
    name_length = name_length
    name_datatype = name_datatype
