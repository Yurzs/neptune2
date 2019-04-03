from dns import datatypes
from .rdata import RDATA

name_datatype = {
    'mname': datatypes.UrlAddress,
    'rname': datatypes.UrlAddress,
    'serial': datatypes.int32,
    'refresh': datatypes.int32,
    'retry': datatypes.int32,
    'expire': datatypes.int32,
    'minimum': datatypes.int32
}

name_length = {
    'mname': 'DYNAMIC',
    'rname': 'DYNAMIC',
    'serial': 32,
    'refresh': 32,
    'retry': 32,
    'expire': 32,
    'minimum': 32
}


class SOA(RDATA):
    name_length = name_length
    name_datatype = name_datatype
