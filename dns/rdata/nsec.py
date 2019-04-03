from dns import datatypes
from .rdata import RDATA

name_datatype = {
    # TODO HELP
    'next_domain_name': datatypes.UrlAddress,
    'type_bit_maps': 'REST'
}

name_length = {
    'next_domain_name': 'DYNAMIC',
    'type_bit_maps': 'REST'
}


class NSEC(RDATA):
    name_length = name_length
    name_datatype = name_datatype